import requests
import yadisk
import os
from dotenv import load_dotenv

load_dotenv()

URL = 'https://cloud-api.yandex.net/v1/disk/resources'

TOKEN = os.getenv('TOKEN_YANDEX')

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

y = yadisk.YaDisk(token=TOKEN)


def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    requests.put(f'{URL}?path={path}', headers=headers)
    
def upload_file(path):
    
    y.upload('C:/Users/admin/Desktop/parser_tsn_base/prodaja_kvartiri.xlsx', f'{path}prodaja_kvartiri.xlsx')
