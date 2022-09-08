import requests
import json
from bs4 import BeautifulSoup
from src.TestData import username, password


class TestAnalyzeSessionID:

    def test_oauth_analyse_session_id(self):

        with requests.Session() as session:
            r = session.get("https://clarity.dexcom.com/users/auth/dexcom_sts", allow_redirects=False)
            print(r.status_code)
            r = session.get(r.headers['Location'], allow_redirects=False)
            print(r.status_code)
            cookie = r.headers['set-cookie']
            signin = cookie[cookie.index("SignInMessage.") + 1: cookie.index("=")]
            r = session.get("https://uam1.dexcom.com/identity/login?signin={}".format(signin))
            print(r.status_code)
            soup = BeautifulSoup(r.content, 'html5lib')
            idsrv = soup.find(name='input', attrs={'name': 'idsrv.xsrf'}).get('value')
            # print(idsrv)
            payload = {"username": username, "password": password, "idsrv.xsrf": idsrv}
            r = session.post("https://uam1.dexcom.com/identity/login?signin={}".format(signin), data=payload)
            print(r.status_code)
            r = session.get(r.headers['location'], allow_redirects=False)
            print(r.status_code)
            r = session.post("https://clarity.dexcom.com/api/subject/1594950620847472640/analysis_session")
            print(r.status_code)
            response_body = json.loads(r.text)
            assert response_body['analysisSessionId'] is not None
