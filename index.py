from rapidfuzz import process
from asyncio import Event


class Index(object):
    def __init__(self, index_list):
        self.__list = index_list
        self.__name_to_series_dict = dict()
        self.__series_title_list = []
        self.__build_name_to_series_dict()

    def __build_name_to_series_dict(self):
        self.__series_title_list.clear()
        for s in self.__list:
            self.__name_to_series_dict[s["title"]] = s
            self.__series_title_list.append(s["title"])

    def update(self, index_list):
        self.__list = index_list
        self.__build_name_to_series_dict()

    def search(self, query, limit):
        fuzz_results = process.extract(
            query, self.__series_title_list, limit=limit)
        results = []
        for fr in fuzz_results:
            results.append(self.__name_to_series_dict[fr[0]])
        return results

    def get_one(self, query):
        fuzz_result = process.extractOne(
            query, self.__series_title_list)
        return self.__name_to_series_dict[fuzz_result[0]]

    def get_all(self):
        return self.__list

    def clear(self):
        self.__list.clear()
        self.__series_title_list.clear()
        self.__name_to_series_dict.clear()

    def __len__(self):
        return len(self.__list)
