# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pydantic",
#     "rich",
#     "selenium",
# ]
# ///
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pydantic import BaseModel
from pathlib import Path


class Resultat(BaseModel):
    url: str
    code: str


driver = webdriver.Firefox()

driver.get("https://www.idpoisson.fr")
driver.implicitly_wait(5.0)

resultat = Resultat(url=driver.current_url, code=driver.page_source)
chemin = Path(".") / "backup.json"
chemin.write_text(resultat.model_dump_json())

# recherche = driver.find_element(by=By.CSS_SELECTOR, value="input")
# recherche.send_keys("Vincent Perrollaz")
# recherche.send_keys(Keys.RETURN)

# article = driver.find_element(by=By.CSS_SELECTOR, value="article")
# print(article)
driver.quit()
