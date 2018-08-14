import json
from jsonschema import validate
import asyncio
import aiohttp
from datetime import datetime

async def fetch_data(source):
    print(f"{datetime.now()} - Fetching data for {source['name']}")
    async with aiohttp.ClientSession() as session:
        async with session.get(source['url']) as response:
            return source['name'], await response.json()

async def main():
    sources = [
        {
            'name': 'GSA',
            'url': 'https://open.gsa.gov/code.json'
        },
        {
            'name': 'USDA',
            'url': 'https://usda.gov/code.json'
        }
    ]

    with open('./schema-2.0.0.json', 'r') as schema_file:
        schema = json.load(schema_file)


    for result in asyncio.as_completed(map(fetch_data, sources)):
        source_name, json_data = await result
        print(f"{datetime.now()} - Validating {source_name} JSON")
        for repo in json_data['releases']:
            try:
                validate(repo, schema)
            except:
                print(f"{datetime.now()} - Encountered validation errors for {source_name} - {repo['name']}")

loop = asyncio.get_event_loop()
print(f"{datetime.now()} - Let's do this")
loop.run_until_complete(main())
print(f"{datetime.now()} - Let's end this")
