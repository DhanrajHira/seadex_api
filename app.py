import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import thefuzz

from shared_resources import index, is_index_ready, exit_event, update_index_task
from index_builder import build_index, ensure_index_csv, update_index

async def search(request):
    global is_index_ready
    global index
    if not (query:=request.query_params.get("q", None)):
        return JSONResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    await is_index_ready.wait()

    return JSONResponse({"echo": [index[0]]})

async def get_one(request):
    if not (query:=request.query_params.get("q", None)):
        return JSONResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    await is_index_ready.wait()
    return JSONResponse({"echo": [index[0]]})

async def on_start_up():
    url = "https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM/export?format=csv&gid=0"
    await ensure_index_csv(url)
    await build_index(index)
    
    global is_index_ready
    is_index_ready.set()
    
    global update_index_task
    update_index_task = asyncio.create_task(update_index(5, url, index, is_index_ready, exit_event))

async def on_shutdown():
    global update_index_task
    await is_index_ready.wait()
    exit_event.set()
    await update_index_task
    

app = Starlette(debug=True, routes=[Route("/search", search)], on_startup=[on_start_up], on_shutdown=[on_shutdown])

