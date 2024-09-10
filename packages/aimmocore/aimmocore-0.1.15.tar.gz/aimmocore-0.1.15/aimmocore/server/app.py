""" Home for AIMMOCore Viewer Server"""

import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse, Response
from starlette.routing import Route, Mount
from aimmocore.server.routers import datasets as asrd
from aimmocore.server.routers import systems as asrs
from aimmocore.server.services.datasets import update_curation_status
from aimmocore import config as conf

base_dir = os.path.dirname(__file__)
static_dir_path = os.path.join(base_dir, "static")
index_file_path = os.path.join(static_dir_path, "index.html")


async def catch_all(request):
    """Catch all handler"""
    return HTMLResponse(open(index_file_path, encoding="utf8").read())


async def echarts_file_handler(request):
    """Handler for echarts files"""
    file_id = request.path_params["tail"]
    filename = f"echarts-{file_id}.js"
    file_path = os.path.join(static_dir_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return Response("File not found", status_code=404)


routes = [
    Route("/api/v1/version", asrs.VersionRouter),
    Route("/api/v1/datasets", asrd.DatasetRouter),
    Route("/api/v1/datasets/cluster", asrd.ClusterRouter),
    Route("/api/v1/datasets/export", asrd.DatasetExportRouter),
    Route("/api/v1/datasets/file", asrd.DatasetFileRouter),
    Route("/api/v1/datasets/files", asrd.DatasetFileListRouter),
    Route("/api/v1/datasets/metas/aggregation", asrd.MetaAggregationRouter),
    Route("/api/v1/datasets/embeddings", asrd.EmbeddingRouter),
    Mount("/thumbnails", StaticFiles(directory=conf.THUMBNAIL_DIR), name="thumbnails"),
    Mount("/samples", StaticFiles(directory=conf.SAMPLES_DIR), name="samples"),
    Route("/dataset/{path:path}", endpoint=catch_all),
    Route("/", endpoint=catch_all),
    Mount("/", StaticFiles(directory=static_dir_path), name="static"),
    Route("/{path:path}", endpoint=catch_all),
]
app = Starlette(routes=routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    """Startup event for AIMMOCore Viewer Server"""
    await update_curation_status()
    scheduler.start()
    scheduler.add_job(update_curation_status, "interval", seconds=180)
