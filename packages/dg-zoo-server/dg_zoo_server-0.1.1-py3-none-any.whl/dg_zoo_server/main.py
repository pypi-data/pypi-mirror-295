#
# main.py - DeGirum Zoo Server main module
# Copyright DeGirum Corp. 2024
#
# Contains DeGirum Zoo Server main module implementation
#

import pathlib
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
import uvicorn
from typing import Optional
from contextlib import asynccontextmanager
from .public_router import router as public_router
from .internals import general_exception_handler, GeneralError, tokenManager, zooManager
from .args import get_args
from .dev_list import dev_list


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init
    args = get_args()
    zoo_root = pathlib.Path(args.zoo)

    if not zoo_root.exists():
        zoo_root.mkdir(parents=True)

    await tokenManager.load(zoo_root)
    await zooManager.load(zoo_root)

    print(f"Zoo server started at port {args.port} serving zoo {args.zoo}")
    yield
    # cleanup


# API version
api_version = "v1"

# initialize the FastAPI app
app = FastAPI(
    exception_handlers={Exception: general_exception_handler},
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": GeneralError},
        status.HTTP_401_UNAUTHORIZED: {"model": GeneralError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": GeneralError},
    },
    lifespan=lifespan,
)
app.include_router(public_router, prefix=f"/zoo/{api_version}/public")


@app.get("/", response_class=HTMLResponse)
def root():
    """Root endpoint"""
    return """
    <!DOCTYPE html>
    <html>
    <body>
    <h2>DeGirum Zoo Server</h2>
    <a href="docs">API Description</a>
    </body>
    </html>
    """


@app.get("/zoo/version")
def version():
    """Get the zoo API version"""
    return {"version": api_version}


@app.get(f"/devices/api/{api_version}/public/system-info")
def system_info():
    """Get system information"""

    return {"Devices": {dev: [{"@Index": 0}] for dev in dev_list}}


def serverStart(args_str: Optional[str] = None):

    args = get_args(args_str)

    # Start the server with the specified port
    if args.reload:
        uvicorn.run("dg_zoo_server:app", host="0.0.0.0", port=args.port, reload=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=args.port)
