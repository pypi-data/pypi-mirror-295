


import requests


def get_account_token(developer_token):

    developer_token = developer_token

    url = 'https://api.ready2order.com/v1/developerToken/grantAccessToken'
    payload = {
        "authorizationCallbackUri": "http://localhost"  # Use a placeholder URI
    }
    headers = {
        "Authorization": f"Bearer {developer_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    grant_access_token = response.json().get('grantAccessToken')
    grant_access_uri = response.json().get('grantAccessUri')

    print('Your grant access token is:', grant_access_token)
    print("Visit the following URL to grant access:")
    print(grant_access_uri)


