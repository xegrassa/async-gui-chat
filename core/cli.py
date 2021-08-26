import configargparse


def parse_args():
    p = configargparse.ArgParser(default_config_files=['token.txt'], description='Парсинг аргументов')
    p.add_argument('--host', default='minechat.dvmn.org', env_var='HOST', help='IP адресс чата')
    p.add_argument('--listen_port', default='5000', env_var='LISTEN_PORT', help='port чата')
    p.add_argument('--write_port', default='5050', env_var='WRITE_PORT', help='port чата')
    p.add_argument('--token', env_var='TOKEN', help='Токен')
    p.add_argument('--history', default='./minechat.log', env_var='HISTORY', help='Файл логов чата')
    args = p.parse_args()
    return args
