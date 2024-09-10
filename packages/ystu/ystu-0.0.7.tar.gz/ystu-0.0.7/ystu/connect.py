import requests
from bs4 import BeautifulSoup

class auth:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.h = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Host': 'www.ystu.ru',
            'Origin': 'https://www.ystu.ru',
            'Referer': 'www.ystu.ru'
        }
    def auth(self):
        url_login = 'https://www.ystu.ru/WPROG/auth.php'
        h = self.h
        s = requests.Session()
        html = s.get(url_login, headers=h)
        # soup = BeautifulSoup(html.text, 'lxml')
        soup = BeautifulSoup(html.text, 'html.parser')
        codeYSTU = soup.find('input', dict(name='codeYSTU'))['value']
        jsonp = {
            'codeYSTU': codeYSTU,
            'login': self.login,
            'password': self.password,
            'login1': '%C2%F5%EE%E4+%BB'
        }
        h['Referer'] = 'https://www.ystu.ru/WPROG/auth.php'
        s.post('https://www.ystu.ru/WPROG/auth1.php', data=jsonp, headers=h)
        return s

    def get_profile(self):
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
        info = session.get('https://www.ystu.ru/WPROG/lk/lkstud.php', headers=h)
        return info.content.decode('windows-1251')

    def get_marks(self):
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
        info = session.get('https://www.ystu.ru/WPROG/lk/lkstud_oc.php', headers=h)
        return info.content.decode('windows-1251')

    def get_statements(self):
        session = self.auth()
        h = self.h
        h['Referer'] = 'https://www.ystu.ru/WPROG/main.php'
        info = session.get('https://www.ystu.ru/WPROG/lk/lkorder.php', headers=h)
        return info.content.decode('windows-1251')