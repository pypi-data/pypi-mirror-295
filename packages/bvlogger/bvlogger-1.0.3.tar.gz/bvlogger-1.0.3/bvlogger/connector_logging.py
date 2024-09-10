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
        response = requests.post(
            f"{self.base_url}/logConnector/end",
            json={
                'connectorLogId': connector_log_id,
                'endTime': end_time
            },
            headers={
                'Authorization': f'Bearer {self.token}'
            }
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

# Example usage:
# connector_log = ConnectorLog('https://bv.dataanalytics.nl:3000', 'your_token')
# create_response = connector_log.create_connector_log('ZainsConnector', '2024-08-27 14:28:30.359')
# print(create_response)
# update_response = connector_log.update_connector_log(create_response['connectorLogId'], '2024-08-27 14:50:
