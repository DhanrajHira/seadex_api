import asyncio
from asyncio.tasks import FIRST_COMPLETED
import aiohttp
from aiofile import async_open
from index_parser import Parser
import pandas as pd
import os


async def update_index(frequency, tv_url, movies_url, tv_filename, movies_filename, parsed_index, exit_event):
    client = aiohttp.ClientSession()
    while not exit_event.is_set():
        _, pending = await asyncio.wait((asyncio.sleep(frequency), exit_event.wait()), return_when=FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        if exit_event.is_set():
            continue

        tv_csv_file = await fetch_csv(client, tv_url)
        await write_csv_to_disk(tv_filename, tv_csv_file)
        
        movies_csv_file = await fetch_csv(client, movies_url)
        await write_csv_to_disk(movies_filename, movies_csv_file)
        
        await build_index(tv_filename, movies_filename, parsed_index)
        print("Rebuilt Index")
        
    await client.close()

async def build_index(tv_index_filename, movies_index_filename, index):
    raw_tv_csv_file = pd.read_csv(tv_index_filename, header=1, index_col=[0])
    parsed_list = Parser(raw_tv_csv_file).parse()
    raw_movies_csv_file = pd.read_csv(movies_index_filename, header=1, index_col=[0])
    parsed_list.extend(Parser(raw_movies_csv_file).parse())
    await index.update(parsed_list)


async def ensure_index_csv(filename, url):
    if not os.path.exists(filename):
        async with aiohttp.ClientSession() as cl:
            csv_file = await fetch_csv(cl, url)
            await write_csv_to_disk(filename, csv_file)


async def fetch_csv(client, url):
    resp = await client.get(url)
    csv_file = await resp.read()
    return csv_file


async def write_csv_to_disk(filename, csv_file):
    async with async_open(filename, "wb") as file:
        await file.write(csv_file)
