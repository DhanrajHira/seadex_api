from asyncio import Event
from index import Index

index = Index([])
exit_event = Event()
update_index_task = None
