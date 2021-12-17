from asyncio import Event
index = []
is_index_ready = Event()
exit_event = Event()
update_index_task = None