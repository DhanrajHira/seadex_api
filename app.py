import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import orjson

from shared_resources import TV_INDEX_FILENAME, TV_INDEX_URL, index, exit_event, update_index_task, INDEX_REBUILD_FREQ, MOVIES_INDEX_FILENAME, MOVIES_INDEX_URL
from index_builder import build_index, ensure_index_csv, update_index


class OrJsonResponse(JSONResponse):
    def render(self, content):
        return orjson.dumps(content)


async def search(request):
    global index

    if not (query := request.query_params.get("q", None)):
        return OrJsonResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    limit = request.query_params.get("limit", None)
    try:
        limit = int(limit)
    except:
        limit = None
    results = index.search(query, limit=limit if limit else 5)
    return OrJsonResponse({"results": results})


async def get_one(request):
    global index

    if not (query := request.query_params.get("q", None)):
        return OrJsonResponse({"error": "Missing required parameter 'q'"}, status_code=400)
    result = index.get_one(query)
    return OrJsonResponse(result)


async def get_all(request):
    global index
    all_series = index.get_all()
    return OrJsonResponse({"results": all_series})


async def base(request):
    return OrJsonResponse({"endpoints": ["search", "get", "getall"]})


async def on_start_up():
    global index
    await ensure_index_csv(TV_INDEX_FILENAME, TV_INDEX_URL)
    await ensure_index_csv(MOVIES_INDEX_FILENAME, MOVIES_INDEX_URL)
    await build_index(TV_INDEX_FILENAME, MOVIES_INDEX_FILENAME, index)

    global update_index_task
    update_index_task = asyncio.create_task(
        update_index(INDEX_REBUILD_FREQ, TV_INDEX_URL, MOVIES_INDEX_URL, TV_INDEX_FILENAME, MOVIES_INDEX_FILENAME, index, exit_event))


async def on_shutdown():
    global update_index_task
    global index
    exit_event.set()
    index.clear()
    await update_index_task

routes = [
    Route("/search", search),
    Route("/get", get_one),
    Route("/getall", get_all),
    Route("/", base)
]

app = Starlette(debug=False, routes=routes, on_startup=[
                on_start_up], on_shutdown=[on_shutdown])
