from . import utils


class Customers(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def add_call_history(
            self,
            cust_id: int,
            emp_id: int,
            call_date: str,
            result_code: int,
            phone: int,
            call_type: str,
            call_queue_id: int,
            duration: str,
            recording_url: str
    ):
        data = {
            'CustID': cust_id,
            'EmpID': emp_id,
            'CallDate': call_date,
            'ResultCode': result_code,
            'Phone': phone,
            'CallType': call_type,
            'CallQueueID': call_queue_id,
            'Duration': duration,
            'RecordingURL': recording_url
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/AddCallHistory'
        return utils.make_post_request(url, data, self.headers)

    def get_customers(self, prospect_id: int = None, last_name: str = None):
        data = {'prospectid': prospect_id, 'lastname': last_name}
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetCustomers'
        return utils.make_post_request(url, data, self.headers)

    def get_customers2(self, prospect_id: int = None, job_number: str = None, last_name: str = None, phone: str = None):
        data = {'prospectid': prospect_id, 'jobnumber': job_number, 'lastname': last_name, 'phone': phone}
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetCustomers2'
        return utils.make_post_request(url, data, self.headers)

    def get_customers_by_prospect_id(
            self,
            prospect_id: int = None,
            job_number: str = None,
            first_name: str = None,
            last_name: str = None,
            phone: str = None
    ):
        data = {'prospectid': prospect_id,
                'jobnumber': job_number,
                'firstname': first_name,
                'lastname': last_name,
                'phone': phone}
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetCustomersByProspectID'
        return utils.make_post_request(url, data, self.headers)

    def get_lead(
        self,
        start_date: str = None,
        end_date: str = None,
        cst_id: int = None,
        lds_id: int = None,
        ils_id: int = None,
        page_size: int = 10,
        start_index: int = 1,
        options: int = 0,
        sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'cst_id': cst_id,
            'lds_id': lds_id,
            'ils_id': ils_id,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetLead'
        return utils.make_post_request(url, data, self.headers)

    def get_job_status_changes(
        self,
        start_date: str = None,
        end_date: str = None,
        cst_id: int = None,
        job_id: int = None,
        jbs_id: str = None,
        format_: int = None,
        page_size: int = None,
        start_index: int = None,
        options: int = None,
        sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'cst_id': cst_id,
            'job_id': job_id,
            'jbs_id': jbs_id,
            'format': format_,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetJobStatusChanges'
        return utils.make_post_request(url, data, self.headers)

    def get_lead_info(self, prospect_id: int = None, job_number: str = None, last_name: str = None, phone: str = None):
        data = {'prospectid': prospect_id, 'jobnumber': job_number, 'lastname': last_name, 'phone': phone}
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetLeadInfo'
        return utils.make_post_request(url, data, self.headers)

    def get_milestones(
        self,
        start_date: str = None,
        end_date: str = None,
        date_mode: str = None,
        mdt_id: str = 'S',
        cst_id: int = None,
        lds_id: int = None,
        ils_id: int = None,
        page_size: int = 10,
        start_index: int = 1,
        options: int = None,
        sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'datemode': date_mode,
            'mdt_id': mdt_id,  # Can be C, M, R, or S
            'cst_id': cst_id,
            'lds_id': lds_id,
            'ils_id': ils_id,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetMilestones'
        return utils.make_post_request(url, data, self.headers)

    def get_prospect_data(
            self,
            start_date: str = None,
            end_date: str = None,
            cst_id: int = None,
            lds_id: int = None,
            ils_id: int = None,
            page_size: int = 10,
            start_index: int = 1,
            options: int = None,
            sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'cst_id': cst_id,
            'lds_id': lds_id,
            'ils_id': ils_id,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetProspectData'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appointments(
            self,
            start_date: str = None,
            end_date: str = None,
            cst_id: int = None,
            lds_id: int = None,
            ils_id: int = None,
            page_size: int = 10,
            start_index: int = 1,
            options: int = None,
            sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'cst_id': cst_id,
            'lds_id': lds_id,
            'ils_id': ils_id,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetSalesAppointments'
        return utils.make_post_request(url, data, self.headers)

    def get_service_appointments(
            self,
            start_date: str = None,
            end_date: str = None,
            cst_id: int = None,
            lds_id: int = None,
            ils_id: int = None,
            page_size: int = 10,
            start_index: int = 1,
            options: int = None,
            sort_order: int = None
    ):
        data = {
            'startdate': start_date,
            'enddate': end_date,
            'cst_id': cst_id,
            'lds_id': lds_id,
            'ils_id': ils_id,
            'PageSize': page_size,
            'StartIndex': start_index,
            'options': options,
            'SortOrder': sort_order
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/GetServiceAppointments'
        return utils.make_post_request(url, data, self.headers)

    def update_customer(
            self,
            prospect_id: int = None,
            first_name: str = None,
            last_name: str = None,
            phone: str = None
    ):
        data = {
            'prospectid': prospect_id,
            'firstname': first_name,
            'lastname': last_name,
            'phone': phone
        }
        url = f'https://{self.server_id}.leadperfection.com/api/Customers/UpdateCustomer'
        return utils.make_post_request(url, data, self.headers)
