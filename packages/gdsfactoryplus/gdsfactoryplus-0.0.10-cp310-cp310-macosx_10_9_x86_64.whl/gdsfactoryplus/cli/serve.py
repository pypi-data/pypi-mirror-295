from typing import Literal

import uvicorn
from fastapi import Body, FastAPI
from fastapi.responses import PlainTextResponse

from ..pdk import PDK_CELL_NAMES
from ..shared import DOCODE_PDK, import_pdk
from .app import app
from .patch_netlist import _patch_netlist_post
from .tree import _tree


@app.command()
def serve(pdk: str = DOCODE_PDK, port: int = 8787, host: str = "127.0.0.1"):
    app = FastAPI()
    pdk = str(pdk).lower().strip()
    _pdk = import_pdk(pdk)
    for name in _pdk.cells:
        PDK_CELL_NAMES.add(name)
    _pdk.activate()

    @app.post("/patch-netlist")
    def patch_netlist_post(
        path: str, body: str = Body(...), outpath: str = "", schemapath: str = ""
    ):
        content = _patch_netlist_post(path, body, outpath, schemapath, pdk)
        return PlainTextResponse(content)

    @app.get("/patch-netlist")
    def patch_netlist_get(path: str, outpath: str = "", schemapath: str = ""):
        return patch_netlist_post(path, "", outpath, schemapath)

    @app.get("/tree")
    def tree(
        path: str,
        pdk: str = DOCODE_PDK,
        by: Literal["cell", "file"] = "cell",
        key: str = "",
        none_str: str | None = None,
    ):
        return PlainTextResponse(
            _tree(
                path,
                pdk,
                by,
                key,
                none_str,
                PDK_CELL_NAMES,
            )
        )

    uvicorn.run(app, host=host, port=int(port))
