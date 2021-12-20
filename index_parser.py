from math import isnan
import re

class SubLineParseFailed(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Parser(object):
    def __init__(self, panda_csv) -> None:
        self.__csv = panda_csv
        
    @classmethod
    def __parse_simple_text(cls, raw_text):
        if isinstance(raw_text, float) and isnan(raw_text):
            return ""
        elif not isinstance(raw_text, str):
            return str(raw_text)
        else:
            return raw_text.strip()
    
    @classmethod
    def __parse_best_releases(cls, raw_text):
        parsed = dict()
        raw_text = cls.__parse_simple_text(raw_text)
        
        if raw_text == "":
            return parsed

        current_season = 1
        for line in raw_text.split("\n"):
            if ":" in line:
                for sub_line in line.split("|"):
                    try:
                        parsed_line = cls.__parse_release_list(sub_line)
                        parsed.update(parsed_line)
                        current_season+=len(parsed_line)
                    except SubLineParseFailed:
                        return parsed
            else:
                parsed[str(current_season)] = line
                current_season+=1
        return parsed

    @classmethod
    def __parse_release_list(cls, line):
        parsed_sub_line = dict()
        try:
            (season_list, releases) = line.split(":")
        except ValueError as e:
            raise SubLineParseFailed
        season_list = re.split(",|, ", season_list)

        for season in season_list:
            season = season.strip()
            if season == "":
                continue
            if season[0] == "S" and season[1].isdigit():
                parsed_sub_line[season[1:]] = releases.strip()
            else:
                parsed_sub_line[season] = releases.strip()
        
        return parsed_sub_line 

    def parse(self):
        parsed_list = []
        for row in self.__csv.iterrows():
            series = row[1]
            parsed = dict()
            parsed["title"] = self.__parse_simple_text(series.get("Title"))
            parsed["alt_title"] = self.__parse_simple_text(series.get("Alternate Title"))
            parsed["best_release"] = self.__parse_best_releases(series.get("Best Release"))
            parsed["alt_release"] = self.__parse_best_releases(series.get("Alternate Release"))
            parsed["notes"] = self.__parse_simple_text(series.get("Notes"))
            parsed["comparison"] = self.__parse_simple_text(series.get("Comparisons"))
            parsed_list.append(parsed)
        
        return parsed_list
