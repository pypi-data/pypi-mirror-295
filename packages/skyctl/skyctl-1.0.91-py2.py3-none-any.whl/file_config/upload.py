#!/usr/bin/env python3
import os
import tarfile

import click
import requests
import configparser

home = os.path.expanduser('~').replace('\\', '/')
# 当前脚本的绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
upload_config = configparser.ConfigParser()
upload_config.read(current_path + '/file.ini')

# skypilot配置文件
aws = home + upload_config['file_path']['aws']
lam = home + upload_config['file_path']['lambda']
azure = home + upload_config['file_path']['azure']
# gcp = home + upload_config['file_path']['gcp']
ibm = home + upload_config['file_path']['ibm']
kube = home + upload_config['file_path']['kube']
oci = home + upload_config['file_path']['oci']
scp = home + upload_config['file_path']['scp']
# 指定要打包的目录
dirs_to_tar = [aws, lam, azure, ibm, kube, oci, scp]
# 配置文件名
config_file = upload_config['file']['file_name']


def execute(pat, upload_url, namespace):
    headers = {
        "Authorization": "Bearer " + pat
    }
    up_success_file = []
    target_path = home + config_file
    # 创建tar文件对象
    with tarfile.open(target_path, 'w') as tar:
        # 遍历要打包的目录列表
        for dir_name in dirs_to_tar:
            # 判断文件夹是否为空
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                # 获取当前目录下的所有文件和子目录名称
                items = os.listdir(dir_name)
                # 将每个文件或子目录打包到tar文件中
                for item in items:
                    # 获取文件的完整路径
                    file_path = os.path.join(dir_name, item)
                    # 将文件添加到tar文件中
                    tar.add(file_path)
            else:
                up_success_file.append(dir_name)
    # 判断用户是否存在配置文件
    if len(up_success_file) == len(dirs_to_tar):
        click.echo('Configuration file does not exist, upload failed')
        return

    data = {'nameSpace': namespace}
    files = {'file': open(target_path, 'rb')}
    response = requests.post(upload_url, headers=headers, files=files, data=data)
    # 获取 HTTP 响应状态码
    http_code = response.status_code
    if http_code == 401:
        click.echo("{code: 401, res: Unauthorized}")
        return

    res = response.json()

    if res['code'] == 0:
        click.echo(f'File upload to "{namespace}" successful')
    elif res['code'] == 1101000003:
        click.echo(f'The "{namespace}" namespace does not exist, please check')
    else:
        click.echo('File upload failed')
