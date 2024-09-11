import json
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

LOCAL_PATH = "/data/userdata/share/kaggle_competition_descriptions"

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

service = Service("/usr/local/bin/chromedriver")


def crawl_descriptions(competition: str, wait: float = 3.0, force: bool = False) -> dict[str, str]:
    if (fp := Path(f"{LOCAL_PATH}/{competition}.json")).exists() and not force:
        print(f"Found {competition}.json, loading from local file.")
        with fp.open("r") as f:
            return json.load(f)

    driver = webdriver.Chrome(options=options, service=service)
    overview_url = f"https://www.kaggle.com/competitions/{competition}/overview"
    driver.get(overview_url)
    time.sleep(wait)
    site_body = driver.find_element(By.ID, "site-content")
    descriptions = {}

    # Get the subtitles
    elements = site_body.find_elements(By.CSS_SELECTOR, f"a[href^='/competitions/{competition}/overview/']")
    subtitles = []
    for e in elements:
        inner_text = ""
        for child in e.find_elements(By.XPATH, ".//*"):
            inner_text += child.get_attribute("innerHTML").strip()
        subtitles.append(inner_text)

    # Get main contents
    contents = []
    elements = site_body.find_elements(By.CSS_SELECTOR, ".sc-iWlrxG.cMAZdc")
    for e in elements:
        content = e.get_attribute("innerHTML")
        contents.append(content)

    assert len(subtitles) == len(contents) + 1 and subtitles[-1] == "Citation"
    for i in range(len(subtitles) - 1):
        descriptions[subtitles[i]] = contents[i]

    # Get the citation
    element = site_body.find_element(By.CSS_SELECTOR, ".sc-ifyrTC.sc-fyziuY")
    citation = element.get_attribute("innerHTML")
    descriptions[subtitles[-1]] = citation

    data_url = f"https://www.kaggle.com/competitions/{competition}/data"
    driver.get(data_url)
    time.sleep(wait)
    data_element = driver.find_element(By.CSS_SELECTOR, ".sc-iWlrxG.cMAZdc")
    descriptions["Data Description"] = data_element.get_attribute("innerHTML")

    driver.quit()
    with open(f"{LOCAL_PATH}/{competition}.json", "w") as f:
        json.dump(descriptions, f)
    return descriptions


if __name__ == "__main__":
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    cs = api.competitions_list()
    for c in cs:
        name = c.ref.split("/")[-1]
        crawl_descriptions(name)
