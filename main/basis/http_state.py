try:
    import requests
except ImportError as e:
    import os

    print("安装环境中...")
    os.system("pip install requests")
    print("安装成功")
finally:
    try:
        import requests
    except ImportError as e:
        print("安装失败：%s" % e)


class State(object):
    __def_url = "http://pic4us.com:8100/api/internal/readme/status"

    def __init__(self, url=__def_url) -> None:
        session = requests.Session()
        session.trust_env = False
        self.__url = url
        self.__session = session
        super().__init__()

    def get_state_json(self):
        with self.__session.get(self.__url, params=None) as req:
            return req.content.decode("utf-8")
