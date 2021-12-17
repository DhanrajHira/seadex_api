import asyncio
from asyncio.tasks import FIRST_COMPLETED, wait_for
import aiohttp
from aiofile import async_open
from index_parser import Parser
import pandas as pd
import os


async def update_index(frequency, url, parsed_index, is_index_ready, exit_event):
    client = aiohttp.ClientSession()
    while not exit_event.is_set():
        _, pending = await asyncio.wait((asyncio.sleep(frequency), exit_event.wait()), return_when=FIRST_COMPLETED)
        for task in pending:
            task.cancel()

        if exit_event.is_set():
            continue

        csv_file = await fetch_csv(client, url)
        is_index_ready.clear()

        #await write_csv_to_disk(csv_file)
        await build_index(parsed_index)
        print("Rebuilt Index")

        is_index_ready.set()
    await client.close()

async def build_index(parsed_index):
    raw_csv_file = pd.read_csv("index.csv", header=1, index_col=[0])
    parsed_index.clear()
    parsed_index.extend(Parser(raw_csv_file).parse())


async def ensure_index_csv(url):
    if not os.path.exists("index.csv"):
        async with aiohttp.ClientSession() as cl:
            csv_file = await fetch_csv(cl, url)
            await write_csv_to_disk(csv_file)


async def fetch_csv(client, url):
    resp = await client.get(url)
    csv_file = await resp.read()
    return csv_file


async def write_csv_to_disk(csv_file):
    async with async_open("index.csv", "wb") as file:
        await file.write(csv_file)
