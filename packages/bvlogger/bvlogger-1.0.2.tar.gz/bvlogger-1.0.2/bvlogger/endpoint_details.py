import requests

class EndpointDetails:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def create_endpoint_detail(self, connector_log_id, endpoint_name, endpoint_started_at, endpoint_ended_at, records_count, record_max_date):
        url = f"{self.base_url}/logEndpoint"
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'connectorLogId': connector_log_id,
            'endpointName': endpoint_name,
            'endpointStartedAt': endpoint_started_at,
            'endpointEndedAt': endpoint_ended_at,
            'recordsCount': records_count,
            'recordMaxDate': record_max_date
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json()

# Example usage
# endpoint_details = EndpointDetails('https://bv.dataanalytics.nl:3000', 'your_token_here')
# response = endpoint_details.create_endpoint_detail(
#     connector_log_id='1234',
#     endpoint_name='Endpoint1',
#     endpoint_started_at='2024-08-27T14:30:00',
#     endpoint_ended_at='2024-08-27T14:45:00',
#     records_count=100,
#     record_max_date='2024-08-27'
# )
# print(response)
