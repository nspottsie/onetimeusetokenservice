import requests
import json
import time

class TokenServiceClient:
    def __init__(self, api_url):
        """Initialize the client with the API Gateway URL"""
        self.api_url = api_url.rstrip('/')

    def get_token(self):
        """Call the GET /tokens endpoint to obtain a new token"""
        try:
            response = requests.get(f"{self.api_url}/tokens")
            if response.status_code == 200:
                return response.json().get('token')
            else:
                raise Exception(f"Failed to get token. Status: {response.status_code}, Response: {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting token: {str(e)}")

    def validate_token(self, token=None):
        """Call the POST /tokens endpoint to validate a token"""
        if not token:
            raise ValueError("No token provided")

        try:
            response = requests.post(
                f"{self.api_url}/tokens",
                json={"token": token}
            )
            return {
                "is_valid": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else response.text
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error validating token: {str(e)}")


def main():
    # Replace with your actual API Gateway URL
    api_url = "https://hf6e90h5dk.execute-api.us-east-1.amazonaws.com/prod"
    
    client = TokenServiceClient(api_url)
    
    # Get a token
    print("Getting token...")
    token = client.get_token()
    print(f"Received token: {token}")

    time.sleep(10)

    # Validate the token
    print("\nValidating token...")
    result = client.validate_token(token=token)
    print(f"Validation result: {result}")

    # Example of validating an invalid token
    print("\nTesting invalid token...")
    result = client.validate_token("invalid-token")
    print(f"Invalid token result: {result}")


if __name__ == "__main__":
    main()
