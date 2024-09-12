from . import utils


class Client(object):
    def __init__(self, server_id, client_id, username, password, app_key):
        self.server_id = server_id
        self.client_id = client_id
        self.username = username
        self.password = password
        self.app_key = app_key

    def get_credentials(self):
        return {
            'serverid': self.server_id,
            'clientid': self.client_id,
            'username': self.username,
            'password': self.password,
            'appkey':   self.app_key
        }

    def update_credentials(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def authenticate(self):
        data = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'clientid': self.client_id,
            'appkey': self.app_key
        }

        url = f'https://{self.server_id}.leadperfection.com/token'

        headers = {
            'accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            response_data = utils.make_post_request(url=url, data=data, request_headers=headers)
            return response_data
        except (utils.ConnectionError, utils.Timeout, utils.HTTPError, utils.RequestException,
                utils.json.JSONDecodeError) as e:
            return f'Error: {e}'

