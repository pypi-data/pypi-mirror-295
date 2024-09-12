from . import utils


class Installer(object):
    def __init__(self, access_token, server_id):
        self.server_id = server_id
        self.headers = self.headers = utils.headers(access_token=access_token)

    def installer_login_message(self, message_type: str = None):
        data = {'type': message_type}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/InstallerLoginMessage'
        return utils.make_post_request(url, data, self.headers)

    def add_installer_job_notes(self, job_id: int = None, notes: str = None):
        data = {'jobid': job_id, 'notes': notes}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/AddInstallerJobNotes'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_appt_cal(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerApptCal'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_appt_day_list(self, appt_date: str):
        data = {'apptdate': appt_date}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerApptDayList'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_appt_detail(self, appt_date: str, job_id: int):
        data = {'apptdate': appt_date, 'jobid': job_id}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerApptDetail'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_job_detail(self, appt_date: str, job_id: int):
        data = {'apptdate': appt_date, 'jobid': job_id}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerJobDetail'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_job_notes(self, appt_date, job_id: int):
        data = {'apptdate': appt_date, 'jobid': job_id}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerJobNotes'
        return utils.make_post_request(url, data, self.headers)

    def get_installer_stats(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallerStats'
        return utils.make_post_request(url, data, self.headers)

    def get_installs_open(self):
        data = {}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetInstallsOpen'
        return utils.make_post_request(url, data, self.headers)

    def get_job_images(self, rec_type: str, rec_id: int):
        data = {'recytype': rec_type, 'recid': rec_id}
        url = f'https://{self.server_id}.leadperfection.com/api/Installer/GetJobImages'
        return utils.make_post_request(url, data, self.headers)
