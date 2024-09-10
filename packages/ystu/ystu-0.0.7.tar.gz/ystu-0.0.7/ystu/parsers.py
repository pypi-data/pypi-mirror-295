# import requests
import json
from bs4 import BeautifulSoup

class profile:
    def __init__(self, html):
        self.html = html
        # self.soup = BeautifulSoup(html, 'lxml')
        self.soup = BeautifulSoup(html, 'html.parser')

    def p_name(self):
        name = self.soup.h1.text
        return name
    def group(self):
        text = str(self.soup.find_all('td'))
        text = text.replace('<b>Группа: </b></td><td>', 'group_ystu')
        text = text.replace('</td></tr>', 'group_ystu')
        text = text.split('group_ystu')
        return text[4]

    def address(self):  # получение адреса со страницы аккаунта
        text = str(self.soup.find_all('td'))
        text = text.replace('<td><font size="-1">', 'address_ystu')
        text = text.replace('</font></td>', 'address_ystu')
        text = text.split('address_ystu')
        return text[1]

    def emails(self):  # электронная почта
        text = str(self.soup.find_all('td'))
        text = text.replace('<td><font size="-1">', 'address_ystu')
        text = text.replace('</font></td>', 'address_ystu')
        text = text.split('address_ystu')
        return text[3]

    def phone(self):  # номер телефона
        text = str(self.soup.find_all('td'))
        text = text.replace('<td><font size="-1">', 'address_ystu')
        text = text.replace('</font></td>', 'address_ystu')
        text = text.split('address_ystu')
        return text[5]

    def birthday(self):
        text = str(self.soup.find_all('td'))
        text = text.replace('</td>, <td>', 'ystu_birth')
        text = text.replace('</td>, <td><font size="-1">', 'ystu_birth')
        text = text.split('ystu_birth')
        return text[-8]

    def numlib(self):
        text = str(self.soup.find_all('font'))
        text = text.replace('<font size="-1">Читательский билет №:<br/>login:</font>, <font size="-1">', 'ystu_numlib')
        text = text.replace(' <br/>', 'ystu_numlib')
        text = text.split('ystu_numlib')
        return text[1]

    def full_info(self):
        info = {
            "full_name": self.p_name(),  # ФИО
            'group': self.group(),  # номер группы
            'address': self.address(),  # адрес регистрации
            'emails': self.emails(),  # электронная почта вуза и обычная
            'phone': self.phone(),  # номер телефона
            'birthday': self.birthday(),  # дата рождения
            'numlib': self.numlib(),  # номер читательского билета
        }
        return json.dumps(info, ensure_ascii=False)