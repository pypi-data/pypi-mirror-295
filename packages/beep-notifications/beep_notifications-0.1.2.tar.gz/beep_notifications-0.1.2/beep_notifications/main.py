import hashlib

import requests


class BeepNotify:
    def __init__(self, project):
        self.project = project

    def create_link_code(self):
        """
         Returns the link code that the user can use to connect to your notification project.
        :return:
        """
        response = requests.post(f"https://beep.api.worldz.tech/api/{self.project}/link/create/")
        res = response.json()

        return res['code']

    def check_link_code(self, code):
        """
        Performs whether the linking code has been activated by the user. If yes, returns a dictionary with accepted and receiver fields, the latter stores the internal user code in the Beep system, which can be used to perform actions with a particular user. Be sure to save this code! If the code is not activated, it returns a dictionary with the accepted field storing False.
        :param code:
        :return:
        """
        response = requests.get(f"https://beep.api.worldz.tech/api/{self.project}/link/check/{code}")
        res = response.json()

        return res

    def send_notification(self, beep_code, title, body):
        """
        Sends notification to user.
        :param beep_code:
        :param title:
        :param body:
        :return:
        """
        requests.post(f'https://beep.api.worldz.tech/api/notifications/{self.project}/{beep_code}/', data={
            'title': title,
            'body': body,
        })

    def send_verification_code(self, beep_code):
        """
        Sends verification code to user. Verification code's lifetime - 15 minutes.
        :param beep_code:
        :return:
        """
        requests.post(f'https://beep.api.worldz.tech/api/{self.project}/{beep_code}/send_verification/')

    def verification(self, beep_code, verification_code):
        """
        Makes check if verification code is valid.
        :param beep_code:
        :param verification_code:
        :return:
        """
        response = requests.post(f'https://beep.api.worldz.tech/api/{self.project}/{beep_code}/verificate/', data={
            'value': hashlib.sha256(str(verification_code).encode('utf-8')).hexdigest(),
        })

        print(response, response.status_code)
        return response.status_code == 200

    def send_authorization_code(self, beep_code):
        """
        Sends authorization code to user.
        :param beep_code:
        :return:
        """
        requests.get(f'https://beep.api.worldz.tech/api/auth/{self.project}/{beep_code}/acode')

    def authorize_user(self, beep_code, acode):
        """
        Authorizes user and return auth token.
        :param beep_code:
        :param acode:
        :return:
        """
        response = requests.post(f'https://beep.api.worldz.tech/api/auth/{self.project}/{beep_code}/acode/', data={
            'code': acode,
        })

        res = response.json()

        return res['token']