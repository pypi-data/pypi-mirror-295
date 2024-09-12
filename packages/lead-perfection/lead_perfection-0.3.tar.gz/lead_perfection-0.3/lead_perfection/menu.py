from . import utils


class Menu(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def get_menu(self):
        data = None
        url = f'https://{self.server_id}.leadperfection.com/api/Menu/GetMenu'
        return utils.make_get_request(url, data, self.headers)
