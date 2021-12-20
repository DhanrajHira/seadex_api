from asyncio import Event
from index import Index
from starlette.config import Config

config = Config(".env")

index = Index([])
exit_event = Event()
update_index_task = None

TV_INDEX_URL = config("TV_INDEX_URL", cast=str)
MOVIES_INDEX_URL = config("MOVIES_INDEX_URL", cast=str)
TV_INDEX_FILENAME = config("TV_INDEX_FILENAME", cast=str)
MOVIES_INDEX_FILENAME = config("MOVIES_INDEX_FILENAME", cast=str)
INDEX_REBUILD_FREQ = config("INDEX_REBUILD_FREQ", cast=int)

