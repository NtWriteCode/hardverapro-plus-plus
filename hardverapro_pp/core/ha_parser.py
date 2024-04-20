import requests
from datetime import datetime
from bs4 import BeautifulSoup, element
from hardverapro_pp.core.ha_item import HardveraproItem


class HardveraproParser():
    def __init__(self, content: str) -> None:
        self.content = content
        self.soup = BeautifulSoup(content, 'html.parser')

    def get_price(self, li: element.Tag) -> str:
        try:
            media_body = li.find('div', class_='media-body')
            uad_info = media_body.find('div', class_='uad-info')
            uad_price = uad_info.find('div', class_='uad-price')
            return uad_price.getText()
        except Exception as e:
            print(f'Exception happened while parsing the price of an item. Defaulting to unknown value. Message: {str(e)}')
            return '? Ft'

    def get_title(self, li: element.Tag) -> str:
        try:
            media_body = li.find('div', class_='media-body')
            uad_info = media_body.find('div', class_='uad-title')
            link = uad_info.find('a')
            return link.getText()
        except Exception as e:
            print(f'Exception happened while parsing the title of an item. Defaulting to unknown value. Message: {str(e)}')
            return 'Ismeretlen termék'
        
    def get_url(self, li: element.Tag) -> str:
        try:
            media_body = li.find('div', class_='media-body')
            uad_info = media_body.find('div', class_='uad-title')
            link = uad_info.find('a')
            return link['href']
        except Exception as e:
            print(f'Exception happened while parsing the url of an item. Defaulting to unknown value. Message: {str(e)}')
            return 'https://hardverapro.hu/index.html'
        
    def get_thumbnail(self, li: element.Tag) -> str:
        try:
            img = li.find('img')
            url: str = img['data-retina-url']
            url = f'https:{url}' if url.startswith('/') else url
            return url
        except Exception as e:
            print(f'Exception happened while parsing the thumbnail of an item. Defaulting to unknown value. Message: {str(e)}')
            return 'https://cdn.rios.hu/dl/uad/noimage.png'

    def get_author(self, li: element.Tag) -> str:
        try:
            media_body = li.find('div', class_='media-body')
            uad_misc = media_body.find('div', class_='uad-misc')
            link = uad_misc.find('a')
            return link.getText()
        except Exception as e:
            print(f'Exception happened while parsing the author of an item. Defaulting to unknown value. Message: {str(e)}')
            return 'Ismeretlen feltöltő'

    def get_date(self, url: str) -> str:
        try:
            content = requests.get(url).content.decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            span = soup.find('span', title='Feladás időpontja')

            return span.getText().strip()
        except Exception as e:
            print(f'Exception happened while parsing the date of an item. Defaulting to unknown value. Message: {str(e)}')
            return datetime.now().strftime(r'%Y-%m-%d %H:%M')

    def get_reputation(self, li: element.Tag) -> str:
        try:
            media_body = li.find('div', class_='media-body')
            uad_misc = media_body.find('div', class_='uad-misc')
            uad_rating = uad_misc.find('span', class_='uad-rating')

            return uad_rating.getText()
        except Exception as e:
            print(f'Exception happened while parsing the reputation of an item. Defaulting to unknown value. Message: {str(e)}')
            return '0'


    def get_items(self):
        if 'Sajnos a megadott keresési feltételekkel nincs egy találat sem.' in self.content:
            return []
        
        try:
            uad_list_div = self.soup.find('div', class_='uad-list')
            ul_list = uad_list_div.find('ul', class_='list-unstyled')
            li_elements = ul_list.find_all('li', class_='media')
        except Exception as e:
            print(f'Exception happened while parsing the retrieved page. Message: {str(e)}')
            return []

        items = []
        for li in li_elements:
            item = HardveraproItem(self.get_title(li), self.get_price(li), self.get_url(li), self.get_thumbnail(li), self.get_author(li), None, self.get_reputation(li))
            item.upload_date = self.get_date(item.url)

            items.append(item)
        return items
