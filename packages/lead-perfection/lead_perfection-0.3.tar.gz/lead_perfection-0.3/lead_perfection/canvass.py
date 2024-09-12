from . import utils


class Canvass(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def get_canvass_prod(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/GetCanvassProd'
        return utils.make_post_request(url, data, self.headers)

    def add_canvass_pofloats(self,
                           house_number: str,
                           street_name: str,
                           city: str,
                           state: str,
                           zip_code: str,
                           longitude: float,
                           latitude: float,
                           first_name: str = None,
                           last_name: str = None,
                           first_name2: str = None,
                           last_name2: str = None,
                           phone: str = None,
                           alt_phone: str = None,
                           appt_date: str = None,
                           appt_time: str = None,
                           notes: str = None,
                           email: str = None,
                           waiver_exists: bool = None
                           ):
        data = {
            'housenumber': house_number,
            'streetname': street_name,
            'city': city,
            'state': state,
            'zip': zip_code,
            'longitude': longitude,
            'latitude': latitude,
            'firstname': first_name,
            'lastname': last_name,
            'firstname2': first_name2,
            'lastname2': last_name2,
            'phone': phone,
            'altphone': alt_phone,
            'apptdate': appt_date,
            'appttime': appt_time,
            'notes': notes,
            'email': email,
            'waiverexists': waiver_exists
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/AddCanvassPofloats'
        return utils.make_post_request(url, data, self.headers)

    def add_canvass_pofloats2(self,
                            house_number: str,
                            street_name: str,
                            city: str,
                            state: str,
                            zip_code: str,
                            longitude: float,
                            latitude: float,
                            first_name: str = None,
                            last_name: str = None,
                            first_name2: str = None,
                            last_name2: str = None,
                            phone: str = None,
                            alt_phone: str = None,
                            appt_date: str = None,
                            appt_time: str = None,
                            notes: str = None,
                            name_prefix1: str = None,
                            name_prefix2: str = None,
                            name_suffix1: str = None,
                            name_suffix2: str = None,
                            email: str = None,
                            waiver_exists: bool = None
                            ):
        data = {
            'housenumber': house_number,
            'streetname': street_name,
            'city': city,
            'state': state,
            'zip': zip_code,
            'longitude': longitude,
            'latitude': latitude,
            'firstname': first_name,
            'lastname': last_name,
            'firstname2': first_name2,
            'lastname2': last_name2,
            'phone': phone,
            'altphone': alt_phone,
            'apptdate': appt_date,
            'appttime': appt_time,
            'notes': notes,
            'nameprefix1': name_prefix1,
            'nameprefix2': name_prefix2,
            'namesuffix1': name_suffix1,
            'namesuffix2': name_suffix2,
            'email': email,
            'waiverexists': waiver_exists
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/AddCanvassPofloats2'
        return utils.make_post_request(url, data, self.headers)

    def get_canvassed_info(self,
                           employee_type: str,
                           longitude: float,
                           latitude: float
                           ):
        data = {'type': employee_type, 'longitude': longitude, 'latitude': latitude}
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/GetCanvassedInfo'
        return utils.make_post_request(url, data, self.headers)

    def get_canvassed_region(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/GetCanvassedRegion'
        return utils.make_post_request(url, data, self.headers)

    def add_canvass_images(self, file_name: str = None, file_bytes: list = None):
        data = {'filename': file_name, 'filebytes': file_bytes}
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/GetCanvassImages'
        return utils.make_post_request(url, data, self.headers)

    def canvass_validate_login(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Canvass/CanvassValidateLogin'
        return utils.make_post_request(url, data, self.headers)
