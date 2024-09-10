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
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            
            # Handle plain text response from server
            response_text = response.text.strip()
            if response.status_code == 201:
                return {
                    'status_code': response.status_code,
                    'message': response_text
                }
            elif response.status_code == 400:
                return {
                    'status_code': response.status_code,
                    'message': 'Missing required fields'
                }
            elif response.status_code == 401:
                return {
                    'status_code': response.status_code,
                    'message': 'Unauthorized'
                }
            elif response.status_code == 500:
                return {
                    'status_code': response.status_code,
                    'message': 'Server error'
                }
            else:
                return {
                    'status_code': response.status_code,
                    'message': response_text
                }
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return {
                'status_code': response.status_code if response else None,
                'message': str(err)
            }
        except Exception as err:
            print(f"An error occurred: {err}")
            return {
                'status_code': None,
                'message': str(err)
            }