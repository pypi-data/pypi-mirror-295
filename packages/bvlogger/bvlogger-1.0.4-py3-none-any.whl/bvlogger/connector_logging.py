import requests

class ConnectorLog:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def create_connector_log(self, connector_name, start_time):
        response = requests.post(
            f"{self.base_url}/logConnector",
            json={
                'connectorName': connector_name,
                'startTime': start_time
            },
            headers={
                'Authorization': f'Bearer {self.token}'
            }
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def update_connector_log(self, connector_log_id, end_time):
        url = f"{self.base_url}/logConnector/end"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'connectorLogId': connector_log_id,
            'endTime': end_time
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Since the response is plain text, return the text content
        return response.text

