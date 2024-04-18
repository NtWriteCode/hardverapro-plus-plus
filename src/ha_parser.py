import requests
from bs4 import BeautifulSoup, element
from ha_item import HardveraproItem


class HardveraproParser():
    def __init__(self, content: str) -> None:
        self.content = content
        self.soup = BeautifulSoup(content, 'html.parser')

    def get_price(self, li: element.Tag) -> str:
        media_body = li.find('div', class_='media-body')
        uad_info = media_body.find('div', class_='uad-info')
        uad_price = uad_info.find('div', class_='uad-price')

        return uad_price.getText()

    def get_title(self, li: element.Tag) -> str:
        media_body = li.find('div', class_='media-body')
        uad_info = media_body.find('div', class_='uad-title')
        link = uad_info.find('a')

        return link.getText()

    def get_url(self, li: element.Tag) -> str:
        media_body = li.find('div', class_='media-body')
        uad_info = media_body.find('div', class_='uad-title')
        link = uad_info.find('a')

        return link['href']

    def get_thumbnail(self, li: element.Tag) -> str:
        img = li.find('img')
        url: str = img['data-retina-url']
        url = f'https:{url}' if url.startswith('/') else url
        return url

    def get_author(self, li: element.Tag) -> str:
        media_body = li.find('div', class_='media-body')
        uad_misc = media_body.find('div', class_='uad-misc')
        link = uad_misc.find('a')

        return link.getText()

    def get_date(self, url: str) -> str:
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        span = soup.find('span', title='Feladás időpontja')

        return span.getText().strip()

    def get_reputation(self, li: element.Tag) -> str:
        media_body = li.find('div', class_='media-body')
        uad_misc = media_body.find('div', class_='uad-misc')
        uad_rating = uad_misc.find('span', class_='uad-rating')

        return uad_rating.getText()

    def get_items(self):
        uad_list_div = self.soup.find('div', class_='uad-list')
        ul_list = uad_list_div.find('ul', class_='list-unstyled')
        li_elements = ul_list.find_all('li', class_='media')

        items = []
        for li in li_elements:
            item = HardveraproItem(self.get_title(li), self.get_price(li), self.get_url(li), self.get_thumbnail(li), self.get_author(li), None, self.get_reputation(li))
            item.upload_date = self.get_date(item.url)

            items.append(item)
        return items
