# seadex_api
[A Certain Smoke's Index](https://releases.moe) exposed as a REST API. The API uses fuzzy matching so the query only needs to be close enough to the original title to get appropriate results.

Hosted instance: http://seadex.dbhira.com or
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/DhanrajHira/seadex_api)

## Endpoints:
-  `/search?q=<title>&limit=<limit>`
    - To search for "title" in the index, and limit the returned results to "limit". The parameter limit is optional and defaults to 5.
    - The response looks something like this:
    ``` 
    {
        "results": [
            {
                "title": Title,
                "alt_title": Alternate title,
                "best_release": {
                    "season number/name": Release name
                    ...
                }
                "alt_release": {
                    "season number/name": Release name
                    ...
                }
                "notes": Notes,
                "comparison": [
                    Comparison url possible with the season number/name.
                    ...
                ]
            }
            ...
        ]
    }
    ```
    - For example sending a get request to `/search?q=attack%20on%20titan?limit=2` has the following response:
    ```
    {
        "results": [
            {
                "title": "Attack on Titan",
                "alt_title": "Shingeki no Kyojin",
                "best_release": {
                    "1": "SCY",
                    "2": "Arid",
                    "3": "SCY",
                    "4": "OZR",
                    "OVA": "Baws"
                },
                "alt_release": {
                    "3": "neko-kBaraka",
                    "4": "LostYears (WEB)"
                },
                "notes": "Arid is SCY with kBaraka subs added.\nScyrous will release his BD batch when the USBD of S4 releases. <The notes shown in this response are truncated to save space>.",
                "comparison": [
                    "S3: https://slow.pics/c/zZ2w9wmp",
                    "S4: https://slow.pics/c/PslbxDSG"
                ]
            },
            {
                "title": "K-On!",
                "alt_title": "",
                "best_release": {},
                "alt_release": {
                    "1": "Crow"
                },
                "notes": "Crow is Henshin+CJ-Tsundere",
                "comparison": [
                    ""
                ]
            }
        ]
    }
    ```
-  `/get?q=<title>` Instead of returning a list of results, this endpoint only returned the info about a single show. The response has the following structure.
    ```
    {
        "title": Title,
        "alt_title": Alternate title,
        "best_release": {
            "season number/name": Release name
            ...
        }
        "alt_release": {
            "season number/name": Release name
            ...
        }
        "notes": Notes,
        "comparison": [
            Comparison url possible with the season number/name.
            ...
        ]
    }
    ```
