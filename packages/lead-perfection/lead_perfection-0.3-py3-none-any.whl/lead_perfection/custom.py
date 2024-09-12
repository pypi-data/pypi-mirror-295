from . import utils


class Custom(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def custom_api_method(self, method_name: str = None, appt_date: str = None, issued_lead_id: int = None):
        data = {'methodname': method_name, 'apptdate': appt_date, 'issuedleadid': issued_lead_id}
        url = f'https://{self.server_id}.leadperfection.com/api/CustomAPI/CustomAPIMethod'
        return utils.make_post_request(url, data, self.headers)
