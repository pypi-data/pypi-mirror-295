from . import utils


def get_leads_inbounds():
    return 'Method not yet defined by LeadPerfection'


def get_leads_settings():
    return 'Method not yet defined by LeadPerfection'


class Leads(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = utils.headers(access_token=access_token)

    def get_inbound_lead_info(
            self,
            start_date: str = None,
            end_date: str = None,
            pro_id: float = None,
            log_number: str = None,
            page_size: float = 10,
            start_index: float = 1
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'pro_id': pro_id,
            'lognumber': log_number,
            'PageSize': page_size,
            'StartIndex': start_index
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetInboundLeadInfo'
        return utils.make_post_request(url, data, self.headers)

    def get_leads_forward_look(self, branch_id: str = None, product_id: str = None, zip_: str = None):
        data = {'branchid': branch_id, 'productid': product_id, 'zip': zip_}
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetLeadsForwardLook'
        return utils.make_post_request(url, data, self.headers)

    def lead_add(
            self,
            prefix: str = None,
            first_name: str = None,
            last_name: str = None,
            suffix: str = None,
            address1: str = None,
            address2: str = None,
            city: str = None,
            state: str = None,
            zip_: str = None,
            cross_street: str = None,
            phone: str = None,
            phone_type: float = None,
            phone2: str = None,
            phone_type2: float = None,
            phone3: str = None,
            phone_type3: float = None,
            product_id: str = None,
            prooddescr: str = None,
            email: str = None,
            sender: str = None,
            log_number: str = None,
            sent_to: str = None,
            qnum: float = None,  # currently unused
            call_morning: bool = False,
            call_afternoon: bool = False,
            call_evening: bool = False,
            call_weekend: bool = False,
            date_received: str = None,
            source: str = None,
            srs_id: float = None,
            force_source: bool = True,
            brn_id: str = None,
            rnk_id: float = None,
            notes: str = None,
            waiver: bool = False,
            user1: str = None,
            user2: str = None,
            user3: str = None,
            user4: str = None,
            user5: str = None,
            user6: str = None,
            user7: str = None,
            user8: str = None,
            user9: str = None,
            user10: str = None,
            user11: float = None,
            user12: float = None,
            user13: float = None,
            user14: float = None,
            user15: float = None,
            pro_id: float = None,
            appt_date: str = None,
            appt_time: str = None,
            recd_date: str = None,
            recd_time: str = None
    ):
        data = {
            'prefix': prefix,
            'firstname': first_name,
            'lastname': last_name,
            'suffix': suffix,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'zip': zip_,
            'crossStreet': cross_street,
            'phone': phone,
            'phonetype': phone_type,
            'phone2': phone2,
            'phonetype2': phone_type2,
            'phone3': phone3,
            'phonetype3': phone_type3,
            'productID': product_id,
            'prooddescr': prooddescr,
            'email': email,
            'sender': sender,
            'lognumber': log_number,
            'sentto': sent_to,
            'qnum': qnum,  # currently unused,
            'callmorning': call_morning,
            'callafternoon': call_afternoon,
            'callevening': call_evening,
            'callweekend': call_weekend,
            'datereceived': date_received,
            'source': source,
            'srs_id': srs_id,
            'forceSource': force_source,
            'brn_id': brn_id,
            'rnk_id': rnk_id,
            'notes': notes,
            'waiver': waiver,
            'user1': user1,
            'user2': user2,
            'user3': user3,
            'user4': user4,
            'user5': user5,
            'user6': user6,
            'user7': user7,
            'user8': user8,
            'user9': user9,
            'user10': user10,
            'user11': user11,
            'user12': user12,
            'user13': user13,
            'user14': user14,
            'user15': user15,
            'pro_id': pro_id,
            'apptdate': appt_date,
            'appttime': appt_time,
            'recdDate': recd_date,
            'recdTime': recd_time
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/LeadAdd'
        return utils.make_post_request(url, data, self.headers)

    def get_lead_data(
            self,
            start_date: str = None,
            end_date: str = None,
            ils_id: float = None,
            milestones: str = None,
            option1: str = None,
            option2: str = None,
            option3: str = None,
            option4: str = None,
            option5: str = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'ils_id': ils_id,
            'milestones': milestones,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'option4': option4,
            'option5': option5
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetLeadData'
        return utils.make_post_request(url, data, self.headers)

    def get_leads_source_sub_promoter(self, type_: str = 'S'):  # S=SourceSub, P=Promoter, B=Branches, R=Products
        data = {'type': type_}
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetLeadsSourceSubPromoter'
        return utils.make_post_request(url, data, self.headers)

    def update_leads_perspective_detail(
            self,
            last_name: str = None,
            first_name: str = None,
            phone: str = None,
            work_phone: str = None,
            cell_phone: str = None,
            address1: str = None,
            city: str = None,
            state: str = None,
            source_sub_id: float = None,
            promoter_id: float = None,
            product_id: str = None,
            alt_data1: str = None,
            alt_data2: str = None,
            appt_date: str = None,
            appt_time: str = None,
            waiver: bool = False,
            notes: str = None,
            last_name2: str = None,
            first_name2: str = None,
            email: str = None
    ):
        data = {
            'lastname': last_name,
            'firstname': first_name,
            'phone': phone,
            'workphone': work_phone,
            'cellphone': cell_phone,
            'address1': address1,
            'city': city,
            'state': state,
            'SourceSubID': source_sub_id,
            'PromoterID': promoter_id,
            'productid': product_id,
            'altdata1': alt_data1,
            'altdata2': alt_data2,
            'apptdate': appt_date,
            'appttime': appt_time,
            'waiver': waiver,
            'notes': notes,
            'Lastname2': last_name2,
            'Firstname2': first_name2,
            'email': email
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/UpdateLeadsPerspectiveDetail'
        return utils.make_post_request(url, data, self.headers)

    def leads_login_message(self, type_: str = 'Leads'):
        data = {'type': type_}
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/LeadsLoginMessage'
        return utils.make_post_request(url, data, self.headers)

    def get_leads_confirmed_message(self, type_: str = 'Leads', confirmed_by: float = None):
        data = {'type': type_, 'confirmedby': confirmed_by}
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetLeadsConfirmedMessage'
        return utils.make_post_request(url, data, self.headers)

    # Method is floatended only for the vendor Spectrum.
    def add_spectrum_lead(
            self,
            first_name: str = None,
            last_name: str = None,
            address1: str = None,
            city: str = None,
            state: str = None,
            zip_: str = None,
            phone: str = None,
            phone_type: float = None,
            phone2: str = None,
            phone_type2: float = None,
            phone3: str = None,
            phone_type3: float = None,
            product_id: str = None,
            prooddescr: str = None,
            email: str = None,
            log_number: str = None,
            sender: str = None,
            sent_to: str = None,
            call_morning: bool = False,
            call_afternoon: bool = False,
            call_evening: bool = False,
            call_weekend: bool = False,
            date_received: str = None,
            srs_id: float = None,
            notes: str = None,
            force_source: bool = True,
            ad_word: str = None,
            user5: str = None,
            waiver: bool = False,
            opt_in: float = None,
            pro_id: float = None,
            a_date: str = None,
            a_time: str = None
    ):
        data = {
            'firstname': first_name,
            'lastname': last_name,
            'address1': address1,
            'city': city,
            'state': state,
            'zip': zip_,
            'phone': phone,
            'phonetype': phone_type,
            'phone2': phone2,
            'phonetype2': phone_type2,
            'phone3': phone3,
            'phonetype3': phone_type3,
            'productID': product_id,
            'prooddescr': prooddescr,
            'email': email,
            'lognumber': log_number,
            'sender': sender,
            'sentto': sent_to,
            'callmorning': call_morning,
            'callafternoon': call_afternoon,
            'callevening': call_evening,
            'callweekend': call_weekend,
            'datereceived': date_received,
            'srs_id': srs_id,
            'notes': notes,
            'forceSource': force_source,
            'adword': ad_word,
            'user5': user5,
            'waiver': waiver,
            'optin': opt_in,
            'pro_id': pro_id,
            'ADate': a_date,
            'ATime': a_time
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/AddSpectrumLead'
        return utils.make_post_request(url, data, self.headers)

    # Method is floatended only for the vendor Spectrum.
    def get_spectrum_results(self, s_date: str = None, e_date: str = None):
        data = {'sdate': s_date, 'edate': e_date}
        url = f'https://{self.server_id}.leadperfection.com/api/Leads/GetSpectrumResults'
        return utils.make_post_request(url, data, self.headers)
