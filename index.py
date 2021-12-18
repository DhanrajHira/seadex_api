from thefuzz import process
from asyncio import Event

class Index(object):
    def __init__(self, index_list):
        self.__list = index_list
        self.__name_to_series_dict = dict()
        self.__is_ready_event = Event()
        self.__build_name_to_series_dict()
        self.__is_ready_event.set()

    def __build_name_to_series_dict(self):
        for s in self.__list:
            self.__name_to_series_dict[s["title"]] = s
    
    async def update(self, index_list):
        self.__is_ready_event.clear()
        self.__list = index_list
        self.__build_name_to_series_dict()
        self.__is_ready_event.set()


    async def search(self, query, limit):
        await self.__is_ready_event.wait()
        fuzz_results = process.extract(query, self.__series_name_generator(self.__list), limit=limit)
        results = []
        for fr in fuzz_results:
            results.append(self.__name_to_series_dict[fr[0]])
        return results
    
    async def get_one(self, query):
        await self.__is_ready_event.wait()
        fuzz_result = process.extractOne(query, self.__series_name_generator(self.__list))
        return self.__name_to_series_dict[fuzz_result[0]]

    async def clear(self):
        async with self.__is_ready_event:
            self.__list.clear()
            self.__name_to_series_dict.clear() 

    @staticmethod
    def __series_name_generator(index):
        for series in index:
            yield series["title"]