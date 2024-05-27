import requests

status = False
class PaymentProcessor:
    @staticmethod
    def process_payment(payment_data='No Data', url='http://127.0.0.1:8000'):
        url = url + '/api/endpoint'
        """
        Processes the payment by making a POST request to the API endpoint.

        Args:
            url (str): The API endpoint URL.
            payment_data (dict): The data to be sent in the payment request.

        Returns:
            str: The status of the payment.

        Raises:
            Exception: If there is an issue with the network request or response.
        """
        try:
            response = requests.get(url, json=status)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            response_data = response.json()  # Parse the JSON response

            if 'status' in response_data:
                return response_data['status']
            else:
                raise ValueError("Response JSON does not contain 'status' key")

        except requests.exceptions.RequestException as e:
            raise Exception(f"An error occurred while making the request: {e}")
        except ValueError as e:
            raise Exception(f"An error occurred while processing the response: {e}")


# Example usage:
if __name__ == "__main__":
    try:
        status = PaymentProcessor.process_payment()
        print(f"Payment status: {status}")
    except Exception as e:
        print(f"Error: {e}")
