import asyncio
from typing import List

import aiohttp
from core.client import CoreClient
from core.entry import SpotEntry
from publisher.types import PublisherInterfaceT
from publisher.types import PublisherFetchError


class PublisherClient(CoreClient):
    fetchers: List[PublisherInterfaceT] = []

    @staticmethod
    def convert_to_publisher(client: CoreClient):
        client.__class__ = CoreClient
        return client

    def add_fetchers(self, fetchers: List[PublisherInterfaceT]):
        self.fetchers.extend(fetchers)

    def add_fetcher(self, fetcher: PublisherInterfaceT):
        self.fetchers.append(fetcher)

    async def fetch(self, filter_exceptions=True) -> List[SpotEntry]:
        tasks = []
        timeout = aiohttp.ClientTimeout(total=10)  # 10 seconds per request
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for fetcher in self.fetchers:
                data = fetcher.fetch(session)
                tasks.append(data)
            result = await asyncio.gather(*tasks, return_exceptions=True)
            if filter_exceptions:
                result = [subl for subl in result if not isinstance(subl, Exception)]
            return [val for subl in result for val in subl]

    def fetch_sync(self) -> List[SpotEntry]:
        results = []
        for fetcher in self.fetchers:
            data = fetcher.fetch_sync()
            results.extend(data)
        return self.remove_fetch_error(results)

    def remove_fetch_error(self, data: List[SpotEntry]) -> List[SpotEntry]:
        timestamp = self.get_timestamp()
        results = []
        for entry in data:
            if type(entry) != PublisherFetchError:
                entry.base.timestamp = timestamp
                results.append(entry)

        return results
