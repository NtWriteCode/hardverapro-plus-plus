import os
import re
import requests
import hashlib
from hardverapro_pp.utils.config import Config

class HardveraproQuery:
    def _url_parser(self, url: str) -> str:
        rex = re.search(r'(?:https)?(?::\/\/)?(?:hardverapro\.hu)?(?:\/)?(?:aprok)?(?:\/)?(.*)', url)
        half_url = rex[1]
        half_url = half_url if not half_url.endswith('/index.html') else half_url[0:half_url.rfind('/index.html')]

        return f'https://hardverapro.hu/aprok/{half_url}/keres.php'

    def _query_param_from_yml(self, query_key: str, config: Config, config_key: str) -> None:
        config_value = config.key(config_key).str('')
        if config_value:
            self._query_params[query_key] = config_value

    def _generate_sesssion(self) -> requests.Session:
        session = requests.session()
        sessiontext_path = os.environ.get('HA_SESSION_PATH', 'cfg/session.txt')
        sessiontext_value = os.environ.get('HA_SESSION_VALUE', '')
        
        if not sessiontext_value:
            try:
                with open(sessiontext_path) as sess_file:
                    sessiontext_value = sess_file.read()
            except:
                print(f'Session file was not found as environment value HA_SESSION_VALUE, neither at the path specified: "{sessiontext_path}"')
                return None

        for header in sessiontext_value.split('-H '):
            if 'cookie' in header[0:20].lower():
                header = header[header.find(':')+1:-1].strip()

                for match in re.findall(r'(.*?)=(.*?)(?:;|(?:\'$))\s*', header):
                    session.cookies.set(match[0], match[1], domain='hardverapro.hu')

        return session
    
    @staticmethod
    def _make_id(url: str):
        hashlib.sha1(url).hexdigest().lower()

    def get_id(self) -> str:
        return self._id

    def __init__(self, config: Config, user_agent: str = None) -> None:
        self._base_url = self._url_parser(config.key('url').str())
        self._id = HardveraproQuery._make_id(self._base_url.encode())
        self._query_params = {}
        self._session = self._generate_sesssion()
        
        if user_agent:
            self._session.headers.update({'User-Agent': user_agent})

        self._query_param_from_yml('stext', config, 'text')
        self._query_param_from_yml('stext_none', config, 'text-exclude')
        self._query_param_from_yml('stcid_text', config, 'county')
        self._query_param_from_yml('stmid_text', config, 'city')
        self._query_param_from_yml('minprice', config, 'min-price')
        self._query_param_from_yml('maxprice', config, 'max-price')
        self._query_param_from_yml('noiced', config, 'no-iced')
        self._query_param_from_yml('search_exac', config, 'search-exact-only')
        self._query_param_from_yml('search_title', config, 'search-title-only')
        self._query_param_from_yml('cmpid_text', config, 'brand')
        self._query_param_from_yml('shipping', config, 'shipping-only')

        config_buying = config.key('buying').int(2)
        match config_buying:
            case 0:
                self._query_params['buying'] = '0'
            case 1:
                self._query_params['buying'] = '1'
            case 2:
                self._query_params['__buying'] = '1'
            case _:
                pass

    def _send_search_modification_request(self) -> bool:
        req = self._session.post('https://hardverapro.hu/muvelet/beallitasok/modosit.php?mode=uad&url=/index.html', data={
                                    'order': 'time',
                                    'dir': 'd',
                                    'block': '200'
                                })
        return req.status_code == 200

    def make_query(self) -> str:
        self._send_search_modification_request()
        out = self._session.get(self._base_url, params=self._query_params)
        return out.content.decode('utf-8')
