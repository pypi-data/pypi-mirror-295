from . import utils


class File(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def download_web_files(self, path: str):
        data = {'path': path}
        url = f'https://{self.server_id}.leadperfection.com/api/File/DownloadWebFiles'
        return utils.make_post_request(url, data, self.headers)
