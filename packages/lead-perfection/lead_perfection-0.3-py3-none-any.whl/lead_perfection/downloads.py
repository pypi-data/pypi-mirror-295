from . import utils


class Downloads(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def get_leads_by_cqdid(self,
                           cqd_id: int,
                           start_row: int,
                           end_row: int
                           ):
        data = {
            'cqd_id': cqd_id,
            'startrow': start_row,
            'endrow': end_row
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Downloads/GetLeadsByCQDID'
        return utils.make_post_request(url, data, self.headers)

    def get_leads_by_cqdid_long(self,
                                cqd_id: int,
                                start_row: int,
                                end_row: int,
                                clf_id: int = None
                                ):
        data = {
            'cqd_id': cqd_id,
            'startrow': start_row,
            'endrow': end_row,
            'clf_id': clf_id
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Downloads/GetLeadsByCQDIDLong'
        return utils.make_post_request(url, data, self.headers)

    def process_call_history_xml(self, str_xml: str = None):
        data = {'strXML': str_xml}
        url = f'https://{self.server_id}.leadperfection.com/api/Downloads/ProcessCallHistoryXML'
        return utils.make_post_request(url, data, self.headers)

    def process_notes_xml(self, str_xml: str = None):
        data = {'strXML': str_xml}
        url = f'https://{self.server_id}.leadperfection.com/api/Downloads/ProcessNotesXML'
        return utils.make_post_request(url, data, self.headers)
