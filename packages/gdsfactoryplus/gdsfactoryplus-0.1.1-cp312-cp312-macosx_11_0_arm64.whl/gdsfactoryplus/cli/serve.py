import os
import pathlib
import re
from typing import Literal

import gdsfactory as gf
import uvicorn
from fastapi import Body, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from ..pdk import PDK_CELL_NAMES
from ..shared import import_pdk
from .app import app as cli
from .patch_netlist import _patch_netlist_post
from .tree import _tree

try:
    from doweb.api.viewer import FileView, file_view_static
    from doweb.browser import get_app
except ImportError:
    from kweb.api.viewer import FileView, file_view_static
    from kweb.browser import get_app

PDK = ""
BASE_DIR = os.environ.get("BASE_DIR", "/tmp/kweb")
app = get_app(fileslocation=BASE_DIR, editable=False)


def needs_to_be_removed(path):
    if path.startswith("/file"):
        return True
    elif path.startswith("/gds"):
        return True


app.router.routes = [r for r in app.routes if not needs_to_be_removed(r.path)]  # type: ignore


@cli.command()
def serve(
    pdk: str = "generic",
    port: int = 8787,
    host: str = "127.0.0.1",
):
    global PDK
    PDK = str(pdk).lower().strip()
    import_pdk(PDK).activate()
    for name in gf.get_active_pdk().cells:
        PDK_CELL_NAMES.add(name)
    uvicorn.run(app, host=host, port=int(port))


@app.post("/patch-netlist")
def patch_netlist_post(path: str, body: str = Body(...), schemapath: str = ""):
    content = _patch_netlist_post(path, body, schemapath, PDK)
    return PlainTextResponse(content)


@app.get("/patch-netlist")
def patch_netlist_get(path: str, outpath: str = "", schemapath: str = ""):
    content = _patch_netlist_post(path, "", schemapath, PDK)
    return PlainTextResponse(content)


@app.get("/tree")
def tree(
    path: str,
    by: Literal["cell", "file"] = "cell",
    key: str = "",
    none_str: str | None = None,
):
    return PlainTextResponse(
        _tree(
            path,
            PDK,
            by,
            key,
            none_str,
            PDK_CELL_NAMES,
        )
    )


@app.get("/view2")
async def view2(
    request: Request,
    file: str,
    pdk: str | None = None,
    cell: str | None = None,
    rdb: str | None = None,
    theme: Literal["light", "dark"] = "dark",
):
    if pdk:
        layer_props = os.path.join(BASE_DIR, "build", "lyp", f"{pdk}.lyp")
        _pdk = import_pdk(pdk)
        layer_views = _pdk.layer_views
        assert layer_views is not None
        layer_views.to_lyp(filepath=layer_props)
    else:
        layer_props = None
    try:
        fv = FileView(
            file=pathlib.Path(file), cell=cell, layer_props=layer_props, rdb=rdb
        )
        resp = await file_view_static(request, fv)
    except HTTPException as e:
        print(e)
        color = "#f5f5f5" if theme == "light" else "#121317"
        return HTMLResponse(f'<body style="background-color: {color}"></body>')
    body = resp.body.decode()
    if theme == "light":
        body = body.replace('data-bs-theme="dark"', 'data-bs-theme="light"')
    body = body.replace(
        "</head>",
        """<style>
     [data-bs-theme=light] {
       --bs-body-bg: #f5f5f5;
     }
     [data-bs-theme=dark] {
       --bs-body-bg: #121317;
     }
   </style>
   </head>""",
    )
    body = body.replace(
        "</body>",
        """<script>
            function checkChanged() {
                fetch("/changed/%path%")
                .then((resp) => resp.json())
                .then((data) => {
                    if (data.changed) {
                        if (socket.readyState > 1) {
                            window.location.reload();
                        } else {
                            document.getElementById("reload").click();
                        }
                    }
                });
                setTimeout(checkChanged, 1000);
            }
            window.onload = checkChanged
            window.addEventListener("message", (event) => {
              const message = JSON.parse(event.data);

              let reload = message.reload;
              if (reload) {
                document.getElementById("reload").click();
                return
              }

              let category = message.category;
              let cell = message.cell;
              let itemIdxs = message.itemIdxs;

              document.getElementById("rdb-tab").click();
              console.log("IFRAME: ", message);
              document.getElementById("rdb-tab").click();
              //const event = new Event('change');
              let categoryOptionsEl = document.getElementById("rdbCategoryOptions");
              let cellOptionsEl = document.getElementById("rdbCellOptions");
              let rdbItemsEl = document.getElementById("rdbItems");
              let categoryOptions = Array.from(categoryOptionsEl.children)
                .map((c)=>[c.innerHTML, c.value])
                .reduce((acc, [key, value]) => {acc[key] = value; return acc;}, {});
              let cellOptions = Array.from(cellOptionsEl.children)
                .map((c)=>[c.innerHTML, c.value])
                .reduce((acc, [key, value]) => {acc[key] = value; return acc;}, {});
              console.log(categoryOptions)
              console.log(cellOptions)
              let cellIndex = cellOptions[cell];
              let categoryIndex = categoryOptions[category];
              console.log(`cellIndex: ${cellIndex}`);
              console.log(`categoryIndex: ${categoryIndex}`);
              categoryOptionsEl.value = categoryIndex;
              cellOptionsEl.value = cellIndex;
              let ev = new Event("change");
              categoryOptionsEl.dispatchEvent(ev);
              cellOptionsEl.dispatchEvent(ev);
              setTimeout(() => {
                for (itemIndex of itemIdxs) {
                    let idx = `${itemIndex}`;
                    let o = rdbItemsEl.options[idx];
                    if (o) {
                        o.selected = true;
                    }
                    requestItemDrawings();
                }
              }, 200);
            });
        </script>
        </body>
        """.replace(
            "%path%", file
        ),
    )
    body = body.replace(" shadow ", " shadow-none ")
    return HTMLResponse(body)


@app.get("/changed/{file_name:path}")
async def changed(file_name: str):
    path = f"{BASE_DIR}/{file_name}"
    txtpath = f"/tmp/layoutserver/{re.sub('.gds$', '.txt', file_name)}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.makedirs(os.path.dirname(txtpath), exist_ok=True)
    if os.path.exists(txtpath):
        prevts = int(open(txtpath, "r").read().strip())
    else:
        prevts = 0
    if os.path.exists(path):
        ts = int(os.path.getmtime(path))
    else:
        ts = 0
    changed = ts != prevts
    if changed:
        with open(txtpath, "w") as file:
            file.write(f"{ts}")
    return {"changed": changed, "ts": ts, "prevts": prevts, "path": path}
