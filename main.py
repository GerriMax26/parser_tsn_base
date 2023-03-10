import requests
import fake_useragent
from bs4 import BeautifulSoup
from create_excel_file_1 import writer_1
import datetime
from yandex import create_folder
from yandex import upload_file
import os
from dotenv import load_dotenv

#Определяем текущую дату и текущаяя дата минус 14 дней

load_dotenv()

dl = datetime.datetime.today()

dl2 = dl + datetime.timedelta (days = -14)

dl2 = str(dl2)

new_dl2 = dl2[8]+dl2[9]+'/'+dl2[5]+dl2[6]+'/'+dl2[0]+dl2[1]+dl2[2]+dl2[3]

dl = dl.strftime('%d/%m/%Y')


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
#Все что выше для авторизации и создании сесии, чтобы не пришлось авторизовываться каждый раз при новом запросе
response = session.post(link,data = data, headers = header)

soup = BeautifulSoup(response.text, 'lxml')

main_data = soup.find('table', class_= 'toprow')

tbody = main_data.find('tr')

tr = tbody.find('td', class_ = 'leftcolomn')

div_menu = tr.find('div',class_ = 'menu')

#Все что выше, получаем доступ к левой менюшке, чтобы достать оттуда ссылки на определенные категории

div_submenu = div_menu.find_all('div',class_ = 'submenu')

array_link = []

for i in range(len(div_submenu)):
    
    all_a = div_submenu[i].find_all('a')
    
    for j in range(len(all_a)):
        
        array_link.append('http://www.tsnbase.ru' + all_a[j].get('href'))


def parser_flats(): #Парсим Жилая недвижимость(продажа)->Квартиры
    
    flag_header = True #Для проверки, что уже спарсили оглавление
    
    array_number_page = [] #Массив для номеров страниц
    
    url = 'http://www.tsnbase.ru/result_flats'
    
    array_text = [] #Массив, в который будем помещать текст из таблицы
    
    
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
        data = {
            'ad_form_type': 0,
            'start': n,
            'sort': 0,
            'sort_ord': 1,
            'ad_form_type':0,
            'sorttype': 0,
            'sortordtype': 1,
            'date_from': new_dl2,
            'date_to': dl   
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
            flag_if = True
            
            if(len(all_td) > 4): 
                for j in range(3,len(all_td)):
                    if(all_td[j].text == 'Обн.' and flag_header):    
                        array_text.append(all_td[j].text)
                    elif (all_td[j].text == 'Обн.' and (not flag_header)):
                        flag_if = False
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
        
for i in range(len(array_link)):
    if(array_link[i] == 'http://www.tsnbase.ru/search_flats'):
        writer_1(parser_flats,'Продажа-Квартиры')
        
        path = '7.Для IT BackUP/BackUp Bitrix24/Квартирник/'
        dl = dl.replace('/','.')
        create_folder(f'{path}{dl}')
        path = path+dl+'/'
        upload_file(path)
        
    elif(array_link[i] == 'http://www.tsnbase.ru/search_rooms'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/search_flats?type[3]=3'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/result_flats1'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/result_rooms1'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/search_rent'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/search_daily'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/search_lease'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/dispatch'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.rusearch_of'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.rusearch_sk'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.rusearch_uch.php'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.rusearch_osz.php'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/search_cotts'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/list'):
        pass
    elif(array_link[i] == 'http://www.tsnbase.ru/save_request'):
        pass



 