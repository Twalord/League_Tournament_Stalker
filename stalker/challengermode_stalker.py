"""
Handles Challangermode stalking
:author: Jonathan Decker
"""
from utils.webmanager import open_session, quit_session
import logging
import time
import bs4
from models import Player, Team, TeamList

logger = logging.getLogger('scrap_logger')


def stalk(url: str):

    # edit url
    url = url.lower()
    url = url.replace("/show/", "/participants/")

    # open a websession
    driver = open_session(headless=True)
    driver.get(url)

    all_links = []
    # scroll down one page until end of page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # snapshot source and collect all hrefs from container
        soup = bs4.BeautifulSoup(driver.page_source, features="html.parser")
        team_conainter = soup.find('div', class_="cm-arena-wrap")

        links = [link["href"] for link in team_conainter.find_all("a", href=True)]
        all_links = all_links + links
        all_links = list(dict.fromkeys(all_links))

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # TODO finish challengermode stalker, still needs a good solution

    return


def quick_stalk(url):
    """
    Stalk all players in a match, requires a direct link to the match on challengermode
    :param url: Str, a link that shows a single match on challengermode
    :return: TeamList, containing both teams in the match
    """

    logger.debug("Beginning challengermode quick stalk for " + url)
    driver = open_session()
    driver.get(url)

    time.sleep(3)
    challenger_soup = bs4.BeautifulSoup(driver.page_source, features="html.parser")
    quit_session(driver)

    team_containers = challenger_soup.find_all('div', class_="col-6--sm")
    title = challenger_soup.select("#arena-wrap > div > div > div.p-b--medium > div:nth-child(1) > div.pos--rel.z--99.cm-text-shadow > div > div.dis--flx.flx-dir--col.ali-ite--center > div.ta--center > div > span > span")[0].text
    title = title.strip()

    teams = []
    for team_container in team_containers:
        team_name_block = team_container.find('a', class_="link-white")
        team_name_raw = team_name_block.text
        team_name = team_name_raw.strip()

        player_opggs_htmls = team_container.find_all('a', class_="link-white-dark")
        player_opggs = []
        for player_opggs_html in player_opggs_htmls:
            player_opggs.append(player_opggs_html['href'])
        players = []
        for player_opgg in player_opggs:
            rest, sum_name = player_opgg.split("=")
            players.append(Player(sum_name.replace("+", " ")))
        teams.append(Team(team_name, players))

    return TeamList(title, teams)
