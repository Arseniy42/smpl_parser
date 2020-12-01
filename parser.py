import os
import urllib
import requests

from bs4 import BeautifulSoup as bs
from db import Database

site_url = 'https://www.edimdoma.ru'
page_no = 1

db = Database()
if not os.path.exists('img'):
    os.mkdir('img')

while True:

    url = '{site_url}/retsepty?page={page_no}'.format(site_url=site_url, page_no=page_no)
    page = requests.get(url)
    html = bs(page.content, 'html.parser')

    for card in html.select('.card'):

        try:
            card_url = card.find('a').attrs['href']
            recipe_url = site_url + card_url
        except:
            continue

        card_page = requests.get(recipe_url)
        card_html = bs(card_page.content, 'html.parser')

        imgs = card_html.findAll("div", {"class": "thumb-slider__image-container"})
        if imgs:
            uid = card_url.replace('/retsepty/', '')
            if not os.path.exists('img/' + uid):
                os.mkdir('img/' + uid)

            for img in imgs:
                try:
                    img_url = img.contents[1].attrs['src']
                    urllib.request.urlretrieve(img_url, 'img/' + uid + '/' + os.path.basename(img_url))
                except:
                    pass

        recipe_name = card_html.select('.recipe-header__name')[0].text
        person_name = card_html.select('.recipe-author-block .person__name')[0].text
        person_id = int(card_html.select('.person.person_h.person_lh-big')[0].attrs['href'].replace('/users/', ''))
        recipe_description =\
            card_html.select('.recipe_description')[0].text if len(card_html.select('.recipe_description')) else None
        kkal_value = int(card_html.select('.kkal-meter__value')[0].text)
        kkal_unit = card_html.select('.kkal-meter__unit')[0].text
        kkal_percent = card_html.select('.kkal-meter__percent')[0].text

        list_data = [
            recipe_name,
            recipe_url,
            person_name,
            person_id,
            recipe_description,
            kkal_value,
            kkal_unit,
            kkal_percent,
        ]
        db.insert(list_data)
        print(recipe_name)

    page_no += 1