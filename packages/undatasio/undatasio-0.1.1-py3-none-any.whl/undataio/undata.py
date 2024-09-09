import os
from typing import List, Dict

import requests
from requests_toolbelt import MultipartEncoder

ip = '192.168.8.21'


def test_pip():
    print('Test Success')


def upload(token: str, file_lir_path: str, task_name: str = '') -> Dict:
    for file_path in os.listdir(file_lir_path):
        file_read_path = os.path.join(file_lir_path, file_path)
        with open(file_read_path, 'rb') as file:

            fields = {
                'user_id': token,
                'task_name': task_name,
                'file': (file.name, file, 'application/octet-stream')
            }
            m = MultipartEncoder(fields=fields)

            # 发送 POST 请求
            headers = {'Content-Type': m.content_type}
            response = requests.post(f'http://{ip}:8087/api/api/upload', data=m, headers=headers)
            if response.status_code != 200:
                return {'error': '服务暂未开启，请联系管理员'}
    return '上传成功'


def parser(token: str, file_name_list: List, task_name: str = '') -> Dict:
    API_ENDPOINT = f"http://{ip}:8087/api/api/task_return_list"
    data = {
        'user_id': token,
        'task_name': task_name,
        'fileName': file_name_list  # 根据你的接口定义，文件名参数应该是 fileName
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code != 200:
            return {'error': '服务暂未开启，请联系管理员'}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}


def download(token: str, vision: str, task_name: str = '') -> Dict:
    API_ENDPOINT = f"http://{ip}:8087/api/api/download"
    data = {
        'user_id': token,
        'task_name': task_name,
        'vision': vision  # 根据你的接口定义，文件名参数应该是 fileName
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code != 200:
            return {'error': '服务暂未开启，请联系管理员'}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}


def show_vision(token: str, task_name: str = '') -> Dict:
    API_ENDPOINT = f"http://{ip}:8087/api/api/vision_info"
    data = {
        'user_id': token,
        'task_name': task_name,
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code != 200:
            return {'error': '服务暂未开启，请联系管理员'}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}


def show_upload(token: str, task_name: str = '') -> Dict:
    API_ENDPOINT = f"http://{ip}:8087/api/api/view_upload_file"
    data = {
        'user_id': token,
        'task_name': task_name,
    }

    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code != 200:
            return {'error': '服务暂未开启，请联系管理员'}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}


def download_type_info(token: str, type_info: List, file_name: str, vision: str, task_name: str = ''):
    """
    :param token: 用户ID
    :param type_info: 请在title, table, text, title, interline_equation中选择
    :param file_name: 文件名称
    :param vision: 版本
    :param task_name: 任务名称，若不填写，默认使用用户自带的任务id
    :return:
    """
    API_ENDPOINT = f"http://{ip}:8087/api/api/get_type_info"
    data = {
        'user_id': token,
        'type_info': type_info,
        'file_name': file_name,
        'vision': vision,
        'task_name': task_name,
    }
    try:
        response = requests.post(API_ENDPOINT, data=data)
        if response.status_code != 200:
            return {'error': '服务暂未开启，请联系管理员'}
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"请求失败: {e}"}


