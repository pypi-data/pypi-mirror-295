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
app.include_router(public_router, prefix="/zoo/v1/public")


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
    return {"version": "v1"}


@app.get("/devices/api/v1/public/system-info")
def system_info():
    """Get system information"""

    dev_list = [
        "DUMMY/DUMMY",
        "N2X/CPU",
        "N2X/ORCA",
        "N2X/ORCA1",
        "ONNX/CPU",
        "ONNX/VITIS_NPU",
        "OPENVINO/CPU",
        "OPENVINO/GPU",
        "OPENVINO/NPU",
        "RKNN/RK3566",
        "RKNN/RK3568",
        "RKNN/RK3588",
        "TENSORRT/DLA_FALLBACK",
        "TENSORRT/DLA_ONLY",
        "TENSORRT/GPU",
        "TFLITE/AM68PA",
        "TFLITE/ARMNN",
        "TFLITE/CPU",
        "TFLITE/EDGETPU",
        "TFLITE/NXP_ETHOSU",
        "TFLITE/NXP_VX",
    ]
    return {"Devices": {dev: [{"@Index": 0}] for dev in dev_list}}


def serverStart(args_str: Optional[str] = None):

    args = get_args(args_str)

    # Start the server with the specified port
    if args.reload:
        uvicorn.run("dg_zoo_server:app", host="0.0.0.0", port=args.port, reload=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=args.port)
