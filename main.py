import os
import datetime

import requests
import fake_useragent
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from create_excel_file_1 import writer_1
from yandex import create_folder
from yandex import upload_file


load_dotenv()

def generate_date() -> list:
    """Generate start and end date"""
    
    date_start = datetime.datetime.today()

    date_end = date_start + datetime.timedelta (days = -14)

    date_end = str(date_end)

    new_date_end = date_end[8]+date_end[9]+'/'+date_end[5]+date_end[6]+'/'+date_end[0]+date_end[1]+date_end[2]+date_end[3]

    date_start = date_start.strftime('%d/%m/%Y')
    
    return [date_start,new_date_end]



session = requests.Session()

link = 'http://www.tsnbase.ru/login'

user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

data = {
    'login': os.getenv('login'),
    'password': os.getenv('password')
}


def get_links() -> list:

    response = session.post(link,data = data, headers = header)

    soup = BeautifulSoup(response.text, 'lxml')

    main_data = soup.find('table', class_= 'toprow')

    tbody = main_data.find('tr')

    tr = tbody.find('td', class_ = 'leftcolomn')

    div_menu = tr.find('div',class_ = 'menu')

    div_submenu = div_menu.find_all('div',class_ = 'submenu')

    array_links: list = []

    for i in range(len(div_submenu)):
        
        all_a: str = div_submenu[i].find_all('a')
        
        for j in range(len(all_a)):
            
            array_links.append('http://www.tsnbase.ru' + all_a[j].get('href'))

    return array_links


def parser_flats(): #Парсим Жилая недвижимость(продажа)->Квартиры
    
    array_date_start_end: list = generate_date()

    date_start: str = array_date_start_end[0]

    date_end: str = array_date_start_end[1]
    
    flag_header: bool = True #Для проверки, что уже спарсили оглавление
    
    array_number_page: list = [] 
    
    url: str = 'http://www.tsnbase.ru/result_flats'
    
    array_text: list = [] #Массив, в который будем помещать текст из таблицы
    
    
    response = session.get(url,headers = header)
    soup = BeautifulSoup(response.text, 'lxml')
    body = soup.find('body')
    table = body.find('table', class_ = 'toprow')
    td = table.find('td', valign = 'top')
    div = td.find('div', class_ = 'container')
    div_1 = div.find('div',class_ = 'newsright')
    form = div_1.find('form', id = 'submitForm')
    table_1 = form.find('table', class_ = 'results')
    p = form.find('p')
    all_a = p.find_all('a')
    all_tr = table_1.find_all('tr')
    
    
    
    for i in range(len(all_a) - 1):
        array_number_page.append(all_a[i].text)
    amount_page = int(array_number_page[len(array_number_page) - 1])
    
    #Все что выше, нужно для получение инфы о количестве страниц найденных
    
    for n in range(1,amount_page + 1):
        
        data: dict = {
            'ad_form_type': 0,
            'start': n,
            'sort': 0,
            'sort_ord': 1,
            'ad_form_type':0,
            'sorttype': 0,
            'sortordtype': 1,
            'date_from': date_end,
            'date_to': date_start 
        }
        
        response = session.post(url,data = data,headers = header)
        soup = BeautifulSoup(response.text, 'lxml')
        body = soup.find('body')
        table = body.find('table', class_ = 'toprow')
        td = table.find('td', valign = 'top')
        div = td.find('div', class_ = 'container')
        div_1 = div.find('div',class_ = 'newsright')
        form = div_1.find('form', id = 'submitForm')
        table_1 = form.find('table', class_ = 'results')
        p = form.find('p')
        all_a = p.find_all('a')
        all_tr = table_1.find_all('tr')
        
        for i in range(len(all_tr)):
            
            all_td = all_tr[i].find_all('td')
            
            flag_if: bool = True
            
            if(len(all_td) > 4):
                 
                for j in range(3,len(all_td)):
                    
                    if(all_td[j].text == 'Обн.' and flag_header):
                            
                        array_text.append(all_td[j].text)
                        
                    elif (all_td[j].text == 'Обн.' and (not flag_header)):
                        
                        flag_if: bool = False
                        break
                    else:
                        array_text.append(all_td[j].text)
                        
                    #Объявление переменных, чтобы по ним построить таблицу(Название столбцов/ содержимое столбцов)
                    
                if(flag_if):
                    flag_header = False
                    date_update = array_text[0]
                    number_of_rooms = array_text[1]
                    adress = array_text[2]
                    subway = array_text[3]
                    floor = array_text[4]
                    house = array_text[5]
                    S_all = array_text[6]
                    S_living = array_text[7]
                    S_room = array_text[8]
                    tv = array_text[9]
                    s_u = array_text[10]
                    sd = array_text[11]
                    price = array_text[12]
                    credit = array_text[13]
                    agent = array_text[14]
                    phone = array_text[15]
                    comment = array_text[16]
                    array_text = []
                    
                    yield date_update,number_of_rooms,adress,subway,floor,house,S_all,S_living,S_room,tv,s_u,sd,price,credit,agent,phone,comment
            else:
                continue

def main() -> None:
    
    array_date_start_end: list = generate_date()

    date_start: str = array_date_start_end[0]
    
    array_links: str = get_links()

    for i in range(len(array_links)):
        
        if(array_links[i] == 'http://www.tsnbase.ru/search_flats'):
            
            writer_1(parser_flats,'Продажа-Квартиры')
            
            path: str = '7.Для IT BackUP/BackUp Bitrix24/Квартирник/'
            
            date_start: str = date_start.replace('/','.')
            
            create_folder(f'{path}{date_start}')
            
            path: str = path + date_start + '/'
            
            upload_file(path)
            
        elif(array_links[i] == 'http://www.tsnbase.ru/search_rooms'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/search_flats?type[3]=3'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/result_flats1'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/result_rooms1'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/search_rent'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/search_daily'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/search_lease'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/dispatch'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.rusearch_of'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.rusearch_sk'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.rusearch_uch.php'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.rusearch_osz.php'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/search_cotts'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/list'):
            pass
        elif(array_links[i] == 'http://www.tsnbase.ru/save_request'):
            pass


if __name__ == '__main__':
    main()