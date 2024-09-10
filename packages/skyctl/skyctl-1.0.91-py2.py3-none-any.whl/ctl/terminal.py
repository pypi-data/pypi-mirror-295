# !/usr/bin/env python3
import base64
import configparser
import os
from typing import Optional
import click
import requests
from cryptography.fernet import Fernet
import file_config.upload as upload_file
import file_config.space as name_space


class User:
    def __init__(self, uid, username, password):
        self.uid = uid
        self.username = username
        self.password = password


_CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class _CustomClickCommand(click.Command):
    def get_help(self, ctx):
        help_str = ctx.command.help
        ctx.command.help = help_str.replace('.. code-block:: bash\n', '\b')
        return super().get_help(ctx)


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


url_config = configparser.ConfigParser()
home = os.path.expanduser('~').replace('\\', '/')
# 指定要检查的目录路径
dir_path = home + '/.uc'
# 脚本当前的绝对路径
current_path = os.path.abspath(os.path.dirname(__file__))
url_config.read(current_path + '/server_config.ini')
login_url = url_config['server']['login_url']
upload_url = url_config['server']['upload_url']
list_url = url_config['server']['list_url']
create_url = url_config['server']['create_url']
check_url = url_config['server']['check_url']


@click.group()
def login():
    """SkyCtl Login CLI."""
    pass


# @login.command('login', help='Login Skyctl', context_settings=_CONTEXT_SETTINGS)
# @click.option('--username',
#               '-u',
#               prompt=True,
#               help='Username for login')
# @click.option('--password',
#               '-pwd',
#               prompt=True,
#               hide_input=True,
#               help='Password for login')
# def auth(username, password):
#     data = login_auth(username, password)
#     if data['code'] == 0:
#         user_id = data['data']['id']
#         encryption(username, password, user_id)
#         click.echo('Login successful!')
#     else:
#         click.echo('Invalid username or password!')
#         exit(1)


@login.command('check',
               help='Check if the skypilot configuration file is effective',
               context_settings=_CONTEXT_SETTINGS)
def check():
    pat = check_key()
    if pat is not None:
        headers = {
            "Authorization": "Bearer " + pat,
            "Content-Type": "application/json"
        }
        response = requests.get(check_url, headers=headers)
        if response.status_code == 401:
            click.echo('Authentication failed, please check the configuration file!')
        else:
            click.echo('Authentication successful!')


@click.group()
def upload():
    """SkyCtl Upload CLI."""
    pass


@upload.command('upload',
                help='Upload skypilot configuration file',
                cls=_CustomClickCommand,
                context_settings=_CONTEXT_SETTINGS)
@click.option('--space',
              '-s',
              help='Namespace for file upload. If omitted, files will be uploaded to the default namespace.',
              default='default',
              show_default=True,
              prompt='Enter the namespace for file upload (or leave blank for default)',
              type=str)
def file(space: Optional[str]):
    if not click.confirm(f'Are you sure want to upload to the "{space}" namespace?'):
        click.echo('Aborted by user.')
        return

    click.echo(f"Uploading files to namespace: '{space}'")
    pat = check_key()
    if pat is not None:
        upload_file.execute(pat, upload_url, space)


@click.group()
def namespace():
    """SkyCtl Namespace CLI."""
    pass


@namespace.command('namespace',
                   help='Operation of Namespace',
                   context_settings=_CONTEXT_SETTINGS)
@click.option('--create',
              '-c',
              help='Create a namespace',
              type=str)
@click.option('--ls',
              '-l',
              is_flag=True,
              default=False,
              required=False,
              help='Show the namespace list')
def create_space(create: Optional[str], ls: bool):
    pat = check_key()
    if pat is not None:
        if create:
            ls = False
            name_space.create(create_url, pat, create)

        if ls:
            name_space.get_list(list_url, pat)


def encryption(account, pwd, user_id):
    # 生成密钥
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # 加密用户id
    uid = str(user_id).encode()
    encrypted_uid = cipher_suite.encrypt(uid)

    # 加密账号
    account_byte = account.encode()  # 密码需要是bytes类型
    encrypted_account = cipher_suite.encrypt(account_byte)

    # 加密密码
    password = pwd.encode()  # 密码需要是bytes类型
    encrypted_password = cipher_suite.encrypt(password)

    # Base64编码
    encoded_uid = base64.urlsafe_b64encode(encrypted_uid).decode()
    encoded_account = base64.urlsafe_b64encode(encrypted_account).decode()
    encoded_password = base64.urlsafe_b64encode(encrypted_password).decode()

    # 创建ConfigParser对象
    config = configparser.ConfigParser()
    key_config = configparser.ConfigParser()

    # 添加一个section
    config.add_section('CREDENTIALS')
    key_config.add_section('CREDENTIALS')

    # 在这个section下设置键值对
    config.set('CREDENTIALS', 'uid', encoded_uid)
    config.set('CREDENTIALS', 'username', encoded_account)
    config.set('CREDENTIALS', 'password', encoded_password)
    key_config.set('CREDENTIALS', 'uc_access_key', base64.urlsafe_b64encode(key).decode())

    # 使用os.path.exists()函数检查目录是否存在
    if not os.path.exists(dir_path):
        # 使用os.makedirs()函数创建目录，注意这里可以创建多级目录
        os.makedirs(dir_path)

    # 写入到文件中
    with open(dir_path + '/credentials.ini', 'w') as configfile:
        config.write(configfile)

    with open(dir_path + '/key.ini', 'w') as configfile:
        key_config.write(configfile)


def decryption():
    files = [dir_path + '/key.ini', dir_path + '/credentials.ini']
    for filename in files:
        if not os.path.exists(filename):
            click.echo('No user authentication profile detected!')
            return

    try:
        config = configparser.ConfigParser()
        # 读取INI文件并解密
        config.read(dir_path + '/key.ini')
        key = base64.urlsafe_b64decode(config['CREDENTIALS']['uc_access_key'].encode())
        cipher_suite = Fernet(key)

        config.read(dir_path + '/credentials.ini')
        encoded_uid = config['CREDENTIALS']['uid']
        encoded_username = config['CREDENTIALS']['username']
        encoded_password = config['CREDENTIALS']['password']

        # Base64解码
        encrypted_uid = base64.urlsafe_b64decode(encoded_uid.encode())
        encrypted_username = base64.urlsafe_b64decode(encoded_username.encode())
        encrypted_password = base64.urlsafe_b64decode(encoded_password.encode())

        # 解密账号密码
        decrypted_uid = cipher_suite.decrypt(encrypted_uid).decode()
        decrypted_username = cipher_suite.decrypt(encrypted_username).decode()
        decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    except:
        click.echo('User profile error, please check and log in again!')
    else:
        return User(decrypted_uid, decrypted_username, decrypted_password)


def check_key():
    file_path = dir_path + '/pat.ini'
    if not os.path.exists(file_path):
        click.echo('No user authentication profile detected!')
        return None
    try:
        config = configparser.ConfigParser()
        # 读取INI文件
        config.read(file_path)
        pat = config['CREDENTIALS']['pat']

    except:
        click.echo('User profile error, please check and log in again!')
    else:
        return pat


def login_auth(username, password):
    data = {'preferredUsername': username, 'password': password}
    response = requests.post(login_url, data=data)
    return response.json()


def authority(user: User):
    if user:
        data = login_auth(user.username, user.password)
        if data['code'] == 0:
            return True
        else:
            return False


cli = click.CommandCollection(sources=[login, upload, namespace])
if __name__ == '__main__':
    cli()
