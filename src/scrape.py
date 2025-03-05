import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin
import rich
import os
import asyncio
import ssl

context = ssl._create_unverified_context()

BASE_URL = "https://issasports.com/results/"
PATH = "pages/"


async def get_links(year: str, client) -> dict[str, str]:
    """Get page event links"""
    links = {}
    substring = "last"

    try:
        url = f"champs{year}/evtindex.htm"
        resp = await client.get(urljoin(BASE_URL, url))
        html = HTMLParser(resp.text)
        tags = html.css("a")

        for tag in tags:
            href = tag.attributes["href"]
            if substring not in href:  # type: ignore
                links[href] = tag.text()
    except:
        print("error getting page")

    return links


async def get_pages(link: str, year: str, name: str, client) -> None:
    """Get and save result pages"""

    # create folder if not exist
    path = f"pages/{year}"
    if not os.path.exists(path):
        os.mkdir(path)

    # download and save page in folder
    url = f"champs{year}/{link}"
    resp = await client.get(urljoin(BASE_URL, url))
    filepath = os.path.join(path, f"{name.replace(':','')}.html")

    with open(filepath, "w") as page:
        page.write(resp.text)


async def main() -> None:
    """Main Function"""

    async with httpx.AsyncClient(verify=False) as client:
        # get data
        year = 0  # Set at run

        while year <= 24:
            links = await get_links(year=str(year), client=client)

            if links:
                for key, value in links.items():
                    rich.print(f"Getting {value}")
                    await get_pages(link=key, year=str(year), name=value, client=client)

            year += 1


if __name__ == "__main__":
    """main starts here"""

    asyncio.run(main())
