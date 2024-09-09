import asyncio

from nyaascraper.enums import SITE, QualityFilter, FunCategory, SortBy
from nyaascraper.models import NyaaRSSFeed, NyaaRSSTorrent, SearchResult
from nyaascraper import NyaaRSSClient

client = NyaaRSSClient(site=SITE.FUN)

async def main() -> None:
    result: SearchResult = await client.get_feed(term="Suki Mega")
    print(result)
    return
    
    torrent_info: TorrentInfo = await client.get_torrent_info(result.torrents[0].view_id)

    print(torrent_info)

asyncio.run(main())