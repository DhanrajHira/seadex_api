import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from shared_resources import index, exit_event, update_index_task
from index_builder import build_index, ensure_index_csv, update_index

async def search(request):
    global index

    if not (query:=request.query_params.get("q", None)):
        return JSONResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    limit = request.query_params.get("limit", None)
    try:
        limit = int(limit)
    except:
        limit = None
    results = await index.search(query, limit = limit if limit else 5)
    return JSONResponse({"echo": results})

async def get_one(request):
    global index
    
    if not (query:=request.query_params.get("q", None)):
        return JSONResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    result = index.get_one(query)
    return JSONResponse({"echo": result})

async def on_start_up():
    url = "https://docs.google.com/spreadsheets/d/1emW2Zsb0gEtEHiub_YHpazvBd4lL4saxCwyPhbtxXYM/export?format=csv&gid=0"
    await ensure_index_csv(url)
    await build_index(index)
    
    global update_index_task
    update_index_task = asyncio.create_task(update_index(900, url, index, exit_event))

async def on_shutdown():
    global update_index_task
    global index
    exit_event.set()
    await index.clear()
    await update_index_task
    

app = Starlette(debug=False, routes=[Route("/search", search)], on_startup=[on_start_up], on_shutdown=[on_shutdown])

