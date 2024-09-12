from . import utils


class Sales(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def add_job_images(
            self,
            job_id: int = None,
            file_name: str = None,
            doc_descr: str = None,
            doc_type_id: int = None,
            file_bytes: list = None
    ):
        data = {
            'jobid': job_id,
            'filename': file_name,
            'docdescr': doc_descr,
            'dtyid': doc_type_id,
            'filebytes': file_bytes
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddJobImages'
        return utils.make_post_request(url, data, self.headers)

    def add_notes(self, rec_type: str, rec_id: int, notes: str):
        # Record Type: cst=Prospect, ils=Issued Lead, job=Job Detail
        data = {'rectype': rec_type, 'recid': rec_id, 'notes': notes}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddNotes'
        return utils.make_post_request(url, data, self.headers)

    def add_sales_job_commission(
            self,
            job_id: int,
            sales_rep_id: int,
            commission_pay_amt: float,
            commission_type: int,
            comments: str = None
    ):
        data = {
            'jobid': job_id,
            'comslrid': sales_rep_id,
            'compmtamount': commission_pay_amt,
            'cptid': commission_type,
            'comments': comments
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddSalesJobCommission'
        return utils.make_post_request(url, data, self.headers)

    def add_sales_job_payment(
            self,
            job_id: int,
            payment_date: str,
            payment_amt: float,
            payment_type_id: str,
            payment_method_id: str,
            payment_notes: str = None,
            ar_batch_num: int = 0,
            inc_batch_num: int = 0
    ):
        data = {
            'jobid': job_id,
            'pmtdate': payment_date,
            'pmtamount': payment_amt,
            'pmtid': payment_type_id,
            'pmmid': payment_method_id,
            'pmtnotes': payment_notes,
            'arbatchno': ar_batch_num,
            'incbatchno': inc_batch_num
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddSalesJobPayment'
        return utils.make_post_request(url, data, self.headers)

    def add_sales_job_cost(
            self,
            job_id: int,
            mat_id: str,
            qty: int,
            cost: float,
            price: float,
            comm_flag: bool,
            invoice_date: str,
            invoice_number: str,
            comments: str,
            entered_by: int,
            est_qty: int,
            est_cost: float,
            override_flag: bool = True,
    ):
        data = {
            'job_id': job_id,
            'mat_id': mat_id,
            'qty': qty,
            'cost': cost,
            'price': price,
            'commFlag': comm_flag,
            'invoiceDate': invoice_date,
            'invoiceNumber': invoice_number,
            'comments': comments,
            'enteredBy': entered_by,
            'estQty': est_qty,
            'estCost': est_cost,
            'overrideFlag': override_flag
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddSalesJobCost'
        return utils.make_post_request(url, data, self.headers)

    def add_salesman_images(
            self,
            ils_id: int = None,
            file_name: str = None,
            doc_descr: str = None,
            doc_type_id: int = None,  # use /api/SalesApi/GetSalesApptDispProd with type=y to enumerate possible values
            file_bytes: list = None
    ):
        data = {
            'ilsid': ils_id,
            'filename': file_name,
            'docdescr': doc_descr,
            'dtyid': doc_type_id,
            'filebytes': file_bytes
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/AddSalesmanImages'
        return utils.make_post_request(url, data, self.headers)

    def get_links(self, rec_type: str, rec_id: int):
        data = {'rectype': rec_type, 'recid': rec_id}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetLinks'
        return utils.make_post_request(url, data, self.headers)

    def get_prospect_job_id(self, prospect_id: int = None, contract_id: str = None):
        data = {'prospect_id': prospect_id, 'contractid': contract_id}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetProspectJobID'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_disp_prod(self, data_type: str = None):
        data = {'type': data_type}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptDispProd'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_cal(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptCal'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_day_list(self, appt_date: str):
        data = {'apptdate': appt_date}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptDayList'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_detail(self, appt_date: str, issued_lead_id: int):
        data = {'apptdate': appt_date, 'issuedleadid': issued_lead_id}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptDetail'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_detail_date_range(self, appt_dates: str, appt_date_e: str):
        data = {'apptdates': appt_dates, 'apptdatee': appt_date_e}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptDetailDateRange'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_appt_list(self, appt_date_start: str, appt_date_end: str):
        data = {'apptdatestart': appt_date_start, 'apptdateend': appt_date_end}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesApptList'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_job_detail(self, job_id: int):
        data = {'jobid': job_id}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesJobDetail'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_open(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesOpen'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_sched_cal(self, sched_date: str):
        data = {'scheddate': sched_date}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesSchedCal'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_sched_detail(self, sched_date: str):
        data = {'scheddate': sched_date}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesSchedDetail'
        return utils.make_post_request(url, data, self.headers)

    def get_sales_stats(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/GetSalesStats'
        return utils.make_post_request(url, data, self.headers)

    def sales_login_message(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/SalesLoginMessage'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_appt_detail(self,
                                 issued_lead_id: int,
                                 disposition: str,
                                 product_id1: str = None,
                                 product_id2: str = None,
                                 product_id3: str = None,
                                 product_id4: str = None,
                                 product_id5: str = None,
                                 gsa1: float = None,
                                 gsa2: float = None,
                                 gsa3: float = None,
                                 gsa4: float = None,
                                 gsa5: float = None,
                                 pres_notes: str = None,
                                 user11: float = None,
                                 user12: float = None,
                                 user13: float = None,
                                 user14: float = None,
                                 user15: float = None,
                                 user21: float = None,
                                 user22: float = None,
                                 user23: float = None,
                                 user24: float = None,
                                 user25: float = None,
                                 user31: float = None,
                                 user32: float = None,
                                 user33: float = None,
                                 user34: float = None,
                                 user35: float = None,
                                 user41: float = None,
                                 user42: float = None,
                                 user43: float = None,
                                 user44: float = None,
                                 user45: float = None,
                                 user51: float = None,
                                 user52: float = None,
                                 user53: float = None,
                                 user54: float = None,
                                 user55: float = None
                                 ):
        data = {
            'issuedleadid': issued_lead_id,
            'disposition': disposition,
            'product_id1': product_id1,
            'product_id2': product_id2,
            'product_id3': product_id3,
            'product_id4': product_id4,
            'product_id5': product_id5,
            'gsa1': gsa1,
            'gsa2': gsa2,
            'gsa3': gsa3,
            'gsa4': gsa4,
            'gsa5': gsa5,
            'presnotes': pres_notes,
            'user11': user11,
            'user12': user12,
            'user13': user13,
            'user14': user14,
            'user15': user15,
            'user21': user21,
            'user22': user22,
            'user23': user23,
            'user24': user24,
            'user25': user25,
            'user31': user31,
            'user32': user32,
            'user33': user33,
            'user34': user34,
            'user35': user35,
            'user41': user41,
            'user42': user42,
            'user43': user43,
            'user44': user44,
            'user45': user45,
            'user51': user51,
            'user52': user52,
            'user53': user53,
            'user54': user54,
            'user55': user55
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesApptDetail'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_appt_detail2(self,
                                  issued_lead_id: int,
                                  disposition: str,
                                  product_id1: str = None,
                                  product_id2: str = None,
                                  product_id3: str = None,
                                  product_id4: str = None,
                                  product_id5: str = None,
                                  gsa1: float = None,
                                  gsa2: float = None,
                                  gsa3: float = None,
                                  gsa4: float = None,
                                  gsa5: float = None,
                                  pres_notes: str = None,
                                  user11: float = None,
                                  user12: float = None,
                                  user13: float = None,
                                  user14: float = None,
                                  user15: float = None,
                                  user21: float = None,
                                  user22: float = None,
                                  user23: float = None,
                                  user24: float = None,
                                  user25: float = None,
                                  user31: float = None,
                                  user32: float = None,
                                  user33: float = None,
                                  user34: float = None,
                                  user35: float = None,
                                  user41: float = None,
                                  user42: float = None,
                                  user43: float = None,
                                  user44: float = None,
                                  user45: float = None,
                                  user51: float = None,
                                  user52: float = None,
                                  user53: float = None,
                                  user54: float = None,
                                  user55: float = None,
                                  followup_date: str = None,
                                  followup_time: str = None
                                  ):
        data = {
            'issuedleadid': issued_lead_id,
            'disposition': disposition,
            'product_id1': product_id1,
            'product_id2': product_id2,
            'product_id3': product_id3,
            'product_id4': product_id4,
            'product_id5': product_id5,
            'gsa1': gsa1,
            'gsa2': gsa2,
            'gsa3': gsa3,
            'gsa4': gsa4,
            'gsa5': gsa5,
            'presnotes': pres_notes,
            'user11': user11,
            'user12': user12,
            'user13': user13,
            'user14': user14,
            'user15': user15,
            'user21': user21,
            'user22': user22,
            'user23': user23,
            'user24': user24,
            'user25': user25,
            'user31': user31,
            'user32': user32,
            'user33': user33,
            'user34': user34,
            'user35': user35,
            'user41': user41,
            'user42': user42,
            'user43': user43,
            'user44': user44,
            'user45': user45,
            'user51': user51,
            'user52': user52,
            'user53': user53,
            'user54': user54,
            'user55': user55,
            'followupdate': followup_date,
            'followuptime': followup_time
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesApptDetail2'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_appt_detail3(self,
                                  issued_lead_id: int = None,
                                  disposition: str = None,
                                  product_id1: str = None,
                                  product_id2: str = None,
                                  product_id3: str = None,
                                  product_id4: str = None,
                                  product_id5: str = None,
                                  gsa1: float = None,
                                  gsa2: float = None,
                                  gsa3: float = None,
                                  gsa4: float = None,
                                  gsa5: float = None,
                                  pres_notes: str = None,
                                  user11: float = None,
                                  user12: float = None,
                                  user13: float = None,
                                  user14: float = None,
                                  user15: float = None,
                                  user21: float = None,
                                  user22: float = None,
                                  user23: float = None,
                                  user24: float = None,
                                  user25: float = None,
                                  user31: float = None,
                                  user32: float = None,
                                  user33: float = None,
                                  user34: float = None,
                                  user35: float = None,
                                  user41: float = None,
                                  user42: float = None,
                                  user43: float = None,
                                  user44: float = None,
                                  user45: float = None,
                                  user51: float = None,
                                  user52: float = None,
                                  user53: float = None,
                                  user54: float = None,
                                  user55: float = None,
                                  followup_date: str = None,
                                  followup_time: str = None,
                                  slt_id: str = None,
                                  st2_id: str = None,
                                  vendor1: str = None,
                                  vendor2: str = None,
                                  vendor3: str = None,
                                  vendor4: str = None,
                                  vendor5: str = None,
                                  ):
        data = {
            'issuedleadid': issued_lead_id,
            'disposition': disposition,
            'product_id1': product_id1,
            'product_id2': product_id2,
            'product_id3': product_id3,
            'product_id4': product_id4,
            'product_id5': product_id5,
            'gsa1': gsa1,
            'gsa2': gsa2,
            'gsa3': gsa3,
            'gsa4': gsa4,
            'gsa5': gsa5,
            'presnotes': pres_notes,
            'user11': user11,
            'user12': user12,
            'user13': user13,
            'user14': user14,
            'user15': user15,
            'user21': user21,
            'user22': user22,
            'user23': user23,
            'user24': user24,
            'user25': user25,
            'user31': user31,
            'user32': user32,
            'user33': user33,
            'user34': user34,
            'user35': user35,
            'user41': user41,
            'user42': user42,
            'user43': user43,
            'user44': user44,
            'user45': user45,
            'user51': user51,
            'user52': user52,
            'user53': user53,
            'user54': user54,
            'user55': user55,
            'followupdate': followup_date,
            'followuptime': followup_time,
            'slt_id': slt_id,
            'st2_id': st2_id,
            'vendor1': vendor1,
            'vendor2': vendor2,
            'vendor3': vendor3,
            'vendor4': vendor4,
            'vendor5': vendor5
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesApptDetail3'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_job_cost(self,
                              job_cost_id: int,
                              job_id: int,
                              mat_id: int,
                              qty: float,
                              cost: float,
                              price: float,
                              comm_flag: bool,
                              override_flag: bool,
                              invoice_date: str,
                              invoice_number: str,
                              comments: str,
                              updated_by: int,
                              est_qty: float,
                              est_cost: float
                              ):
        data = {
            'id': job_cost_id,
            'job_id': job_id,
            'mat_id': mat_id,
            'qty': qty,
            'cost': cost,
            'price': price,
            'commFlag': comm_flag,
            'overrideFlag': override_flag,
            'invoiceDate': invoice_date,
            'invoiceNumber': invoice_number,
            'comments': comments,
            'updatedBy': updated_by,
            'estQty': est_qty,
            'estCost': est_cost

        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesJobCost'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_job_detail(self,
                                job_id: int,
                                cmt_id: str,
                                commission: float,
                                tax_rate: float,
                                gross: float,
                                pws_id: str = None,
                                ):
        data = {
            'jobid': job_id,
            'cmtid': cmt_id,
            'commission': commission,
            'taxrate': tax_rate,
            'gross': gross,
            'pwsid': pws_id
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesJobDetail'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_ack(self, issued_lead_id: int):
        data = {'issuedleadid': issued_lead_id}
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesAck'
        return utils.make_post_request(url, data, self.headers)

    def update_sales_sched_detail(self,
                                  sched_date: str,
                                  tms1: bool = None,
                                  tms2: bool = None,
                                  tms3: bool = None,
                                  tms4: bool = None,
                                  tms5: bool = None,
                                  tms6: bool = None,
                                  ):
        data = {
            'scheddate': sched_date,
            'tms1': tms1,
            'tms2': tms2,
            'tms3': tms3,
            'tms4': tms4,
            'tms5': tms5,
            'tms6': tms6,
        }
        url = f'https://{self.server_id}.leadperfection.com/api/SalesApi/UpdateSalesSchedDetail'
        return utils.make_post_request(url, data, self.headers)
