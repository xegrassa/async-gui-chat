import configargparse


def parse_args():
    p = configargparse.ArgParser(description='Парсинг аргументов')
    p.add_argument('--host', default='minechat.dvmn.org', env_var='HOST', help='IP адресс чата')
    p.add_argument('--port', default='5000', env_var='LISTEN_PORT', help='port чата')
    p.add_argument('--token', env_var='TOKEN', help='Токен')
    p.add_argument('--history', default='./minechat.log', env_var='HISTORY', help='Файл логов чата')
    args = p.parse_args()
    return args
