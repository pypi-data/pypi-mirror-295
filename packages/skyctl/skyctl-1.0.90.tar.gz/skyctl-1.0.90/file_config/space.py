import click
import requests
from tabulate import tabulate
from datetime import datetime


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')


def get_list(url, pat):
    headers = {
        "Authorization": "Bearer " + pat,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    # 获取 HTTP 响应状态码
    http_code = response.status_code
    if http_code == 401:
        click.echo("{code: 401, res: Unauthorized}")
        return
    res = response.json()
    space_list = res['data']

    for item in space_list:
        item['createTime'] = convert_timestamp(item['createTime'])
        item['updateTime'] = convert_timestamp(item['updateTime'])

    data_upper = [{k.upper(): v for k, v in item.items()} for item in space_list]
    click.echo(tabulate(data_upper, headers='keys', tablefmt="pipe", stralign="center", numalign="center"))


def create(url, pat, space_name: str):
    headers = {
        "Authorization": "Bearer " + pat,
        "Content-Type": "application/json"
    }
    params = {"namespace": space_name}

    response = requests.post(url, headers=headers, params=params)
    # 获取 HTTP 响应状态码
    http_code = response.status_code
    if http_code == 401:
        click.echo("{code: 401, res: Unauthorized}")
        return

    res = response.json()
    if res['code'] == 1101000004:
        click.echo('The namespace already exists')
    else:
        click.echo('The namespace create successful')


def space_help():
    print('Usage:  COMMAND  [Option]')
    print('Common Commands: \n'
          'list                  Display namespace list\n'
          'create [namespace]    Create a namespace and  The [namespace] represents the name you need to create\n'
          'upload [namespace]    Upload the configuration file to the specified namespace. If the [namespace] is \n'
          '                      empty,upload it to the default namespace\n'
          'exit                  Exit Skyctl terminal')
