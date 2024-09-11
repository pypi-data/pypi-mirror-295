import traceback
from typing import Optional, Any
from types import FunctionType
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from boson import (
    BaseProvider,
    DatasetInfoRequest,
    PixelsRequest,
    SearchRequest,
)

__all__ = ["serve"]


class BosonProvider(BaseProvider):
    def __init__(
        self,
        name: str = "remote",
        alias: str = "Remote Boson Provider",
        description: str = "a remote Boson provider",
        license: str = "(unknown)",
        extent: Optional[dict] = None,
        search_func: Optional[FunctionType] = None,
        pixels_func: Optional[FunctionType] = None,
        queryables_func: Optional[FunctionType] = None,
        dataset_info_func: Optional[FunctionType] = None,
    ) -> None:
        super().__init__(
            name=name,
            alias=alias,
            description=description,
            license=license,
            extent=extent,
            search_func=search_func,
            pixels_func=pixels_func,
            queryables_func=queryables_func,
            dataset_info_func=dataset_info_func,
        )

        self.router = APIRouter()
        self.router.add_api_route("/dataset_info", self.dataset_info, methods=["POST"])
        self.router.add_api_route("/search", self.search, methods=["POST"])
        self.router.add_api_route("/pixels", self.pixels, methods=["POST"])
        # deprecated
        self.router.add_api_route("/warp", self.pixels, methods=["POST"])

    async def dataset_info(self, request: Request):
        body = await request.body()

        req = DatasetInfoRequest()
        req.ParseFromString(body)

        try:
            resp = super().dataset_info(req)
        except Exception:
            msg = traceback.format_exc()
            raise HTTPException(
                status_code=500, detail=f"unable to run dataset_info function: {msg}"
            )
        return self.proto_response(resp)

    async def pixels(self, request: Request):
        body = await request.body()

        req = PixelsRequest()
        req.ParseFromString(body)

        try:
            resp = super().pixels(req)
        except Exception:
            msg = traceback.format_exc()
            raise HTTPException(status_code=500, detail=f"unable to run pixels function: {msg}")
        return self.proto_response(resp)

    async def search(self, request: Request):
        body = await request.body()

        req = SearchRequest()
        req.ParseFromString(body)

        try:
            resp = super().search(req)
        except Exception:
            msg = traceback.format_exc()
            raise HTTPException(status_code=500, detail=f"unable to run search function: {msg}")

        return self.proto_response(resp)

    def proto_response(self, resp: Any) -> Response:
        return Response(content=resp.SerializeToString(), media_type="application/x-protobuf")


def serve(
    search_func: Optional[FunctionType] = None, pixels_func: Optional[FunctionType] = None, **kwargs
):
    app = FastAPI()
    server = BosonProvider(pixels_func=pixels_func, search_func=search_func, **kwargs)
    app.include_router(server.router)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    return app
