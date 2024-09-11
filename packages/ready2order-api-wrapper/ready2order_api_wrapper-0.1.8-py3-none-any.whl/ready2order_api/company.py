import requests

class Company:
    def __init__(self, account_token):
        self.account_token = account_token
        self.base_url = "https://api.ready2order.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.account_token}",
            "Content-Type": "application/json"
        }

    def get_company_info(self):
        """
        Retrieve information about the company associated with the Account-Token.

        :return: dict, JSON response from the API.
        """
        url = f"{self.base_url}/company"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()