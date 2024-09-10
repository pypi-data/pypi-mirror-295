import requests

class Auth:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth",
            json={
                'username': username,
                'password': password
            }
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json().get('token')

# Example usage:
# auth = Auth('https://bv.dataanalytics.nl:3000')
# token = auth.login('admin', 'admin@123')
# print(token)
