import re
import requests
import hashlib


class HardveraproQuery:
    def _url_parser(self, url: str) -> str:
        rex = re.search(r'(?:https)?(?::\/\/)?(?:hardverapro\.hu)?(?:\/)?(?:aprok)?(?:\/)?(.*)', url)
        half_url = rex[1]
        half_url = half_url if not half_url.endswith('/index.html') else half_url[0:half_url.rfind('/index.html')]

        return f'https://hardverapro.hu/aprok/{half_url}/keres.php'

    def _query_param_from_yml(self, query_name: str, yml: dict, yml_name: str) -> None:
        if yml_name in yml and yml[yml_name]:
            self.query_params[query_name] = yml[yml_name]

    def _generate_sesssion(self) -> requests.Session:
        session = requests.session()
        with open('session.txt') as sess_file:
            raw_session = sess_file.read()
            for header in raw_session.split('-H '):
                if 'cookie' in header[0:20].lower():
                    header = header[header.find(':')+1:-1].strip()

                    for match in re.findall(r'(.*?)=(.*?)(?:;|(?:\'$))\s*', header):
                        session.cookies.set(match[0], match[1], domain="hardverapro.hu")

        return session

    def __init__(self, item_urls: object) -> None:
        self.base_url = self._url_parser(item_urls['url'])
        self.id = hashlib.sha1(self.base_url.encode()).hexdigest().lower()
        self.query_params = {}
        self.session = self._generate_sesssion()

        self._query_param_from_yml('stext', item_urls, 'text')
        self._query_param_from_yml('stext_none', item_urls, 'text-exclude')
        self._query_param_from_yml('stcid_text', item_urls, 'county')
        self._query_param_from_yml('stmid_text', item_urls, 'city')
        self._query_param_from_yml('minprice', item_urls, 'min-price')
        self._query_param_from_yml('maxprice', item_urls, 'max-price')
        self._query_param_from_yml('noiced', item_urls, 'no-iced')
        self._query_param_from_yml('search_exac', item_urls, 'search-exact-only')
        self._query_param_from_yml('search_title', item_urls, 'search-title-only')
        self._query_param_from_yml('cmpid_text', item_urls, 'brand')
        self._query_param_from_yml('shipping', item_urls, 'shipping-only')

        if 'buying' in item_urls and item_urls['buying']:
            match item_urls['buying']:
                case 0:
                    self.query_params['buying'] = 0
                case 1:
                    self.query_params['buying'] = 1
                case 2:
                    self.query_params['__buying'] = 1
                case _:
                    pass

    def send_search_modification_request(self) -> bool:
        req = self.session.post('https://hardverapro.hu/muvelet/beallitasok/modosit.php?mode=uad&url=/index.html', data={
                                    'order': 'time',
                                    'dir': 'd',
                                    'block': '200'
                                })
        return req.status_code == 200

    def make_query(self) -> bytes:
        self.send_search_modification_request()
        out = self.session.get(self.base_url, params=self.query_params)
        return out.content
