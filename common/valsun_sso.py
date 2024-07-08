import base64
import json
import requests
from flask import request, session
from config.available_pro_users import AVAILABLE_PRO_USERS
from config.system import SSO_URL

class Sso:
    sso_url = SSO_URL
    system_name = ''
    err_code = "0"
    err_msg = ""
    def __init__(self, system_name=""):
        self.system_name = system_name
    def logout(self):
        if 'ticket' not in request.args and 'sid' not in request.args:
            sso_logout_url = self.get_sso_logout_url()
            if sso_logout_url is not None:
                requests.get(self.get_sso_logout_url())
            session.clear()
            self.del_session()
        elif request.args.get('ticket') == session.get('ptlogout'):
            session.clear()
            self.del_session()
    @staticmethod
    def del_session():
        session.pop('ptoken', None)
        session.pop('ssoSid', None)
    def check_login(self):
        if session.get('userToken'):
            return True
        if 'ticket' not in request.args:
            self.err_code = '002'
            self.err_msg = 'no ticket'
            return False
        url = f"{self.sso_url}index.php?mod=sso&act=changeTicket&ticket={request.args.get('ticket')}"
        response = requests.get(url)
        token = json.loads(response.text)
        if not token or 'errCode' not in token:
            self.err_code = '001'
            self.err_msg = 'Access to SSO has a problem!'
            return False
        elif token['errCode'] != 200:
            self.err_code = token['errCode']
            self.err_msg = token['errMsg']
            return False
        login_info = token['data']['userInfo']
        session['ptoken'] = token['data']['ptoken']
        session['ssoSid'] = token['data']['sid']
        session['ptlogout'] = token['data']['ptlogout']
        session['userToken'] = login_info['userToken']
        self.set_conversation(login_info)
        return True
    def get_sso_url(self):
        current_url = request.url
        encoded_url = base64.b64encode(current_url.encode('utf-8')).decode('utf-8')
        return f"{self.sso_url}index.php?mod=sso&act=getTicket&urlfrom={encoded_url}&systemName={self.system_name}"
    def get_sso_logout_url(self):
        ptoken = session.get('ptoken', None)
        ssoSid = session.get('ssoSid', None)
        if ptoken is None or ssoSid is None:
            return None
        return f"{self.sso_url}index.php?mod=sso&act=logout&ptoken={ptoken}&systemName={self.system_name}&sid={ssoSid}"
    @staticmethod
    def set_conversation(login_info):
        session['userName'] = login_info['userCnName']
        session['userLoginName'] = login_info['userName']
        session['userToken'] = login_info['userToken']
        session['globalUserId'] = login_info['globalUserId']
        session['userId'] = login_info['userId']
        session['company'] = login_info['company']
        session['userInfo'] = login_info
    @staticmethod
    def get_user():
        return session.get('userInfo', {})
    @staticmethod
    def get_user_info():
        info = session.get('userInfo', {})
        if info is not None:
            return {
                "name": info['userCnName'],
                "job_no": info['globalUserJobNo'],
                "mail": info['userName'],
                "available_pro" : info['userName'] in AVAILABLE_PRO_USERS,
            }
        return {}