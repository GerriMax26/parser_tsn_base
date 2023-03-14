import os

import requests
import yadisk
from dotenv import load_dotenv

load_dotenv()

URL: str = 'https://cloud-api.yandex.net/v1/disk/resources'

TOKEN: str = os.getenv('TOKEN_YANDEX')


def create_folder(path) -> None:
    """Creating a folder. \n path: Path to the folder being created."""
    
    headers: dict = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}
    requests.put(f'{URL}?path={path}', headers=headers)


def upload_file(path) -> None:
    """Uploading a file to disk"""
    
    y = yadisk.YaDisk(token=TOKEN)
    y.upload('C:/Users/admin/Desktop/parser_tsn_base/prodaja_kvartiri.xlsx', f'{path}prodaja_kvartiri.xlsx')
