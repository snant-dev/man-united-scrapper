from urllib.request import urlopen
from bs4 import BeautifulSoup
from csv import DictWriter


def get_html_doc(url: str) -> BeautifulSoup:
    """Gets the Beautifulsoup representation for the url entered."""
    html_bytes = urlopen(url)
    return BeautifulSoup(html_bytes, "html.parser")


def get_match_data(url: str) -> dict[str, str]:
    """Gets a team's match from the espn website. example: https://www.espn.com.ar/futbol/equipo/resultados/_/id/360/eng.man_utd"""
    soup = get_html_doc(url)
    common_selector = "#fittPageContainer > div.StickyContainer > div.page-container.cf > div > div.layout__column.layout__column--1 > section > div > section > div:nth-child(3) > div:nth-child(1) > div.flex > div > div.Table__Scroller > table > tbody > tr:nth-child(1) >"
    match_date = soup.select(f"{common_selector} td:nth-child(1) > div")[
        0
    ].text.replace(",", "")
    home_team = soup.select(f"{common_selector} td:nth-child(2) > div > a")[0].text
    match_result = soup.select(
        f"{common_selector} td:nth-child(3) > span > a:nth-child(2)"
    )[0].text
    visitor_team = soup.select(f"{common_selector} td:nth-child(4) > div > a")[0].text
    competition = soup.select(f"{common_selector} td:nth-child(6) > span")[0].text
    return {
        "match_date": match_date,
        "home_team": home_team,
        "match_result": match_result,
        "visitor_team": visitor_team,
        "competition": competition,
    }


def convert_data_to_csv(data: list[dict[str, str]]) -> None:
    """Convert a list of data_matches into csv."""
    fieldnames = list(data[0].keys())
    with open("data.csv", "w") as csv_file:
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data_match in data:
            writer.writerow(data_match)


data = [
    get_match_data(
        "https://www.espn.com.ar/futbol/equipo/resultados/_/id/360/eng.man_utd"
    ),
    get_match_data(
        "https://www.espn.com.ar/futbol/equipo/calendario/_/id/360/eng.man_utd"
    ),
]

print(data)
convert_data_to_csv(data)
