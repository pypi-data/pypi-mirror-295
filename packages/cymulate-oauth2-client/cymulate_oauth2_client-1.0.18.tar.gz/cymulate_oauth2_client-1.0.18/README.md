# Cymulate OAuth2 Client

A Python client for OAuth2 authentication with the Cymulate API. This library simplifies the process of authenticating with the Cymulate API using OAuth2, managing tokens, and making secure requests effortlessly.

## Installation

To install the package, use `pip`:

```bash
pip install cymulate-oauth2-client 
```

### Requirements

- **Python Version:** This client supports Python **3.12** and above. Ensure you have Python 3.12 or a later version installed to use this package.

## Usage

Below are examples of how to use the `CymulateOAuth2Client` class to authenticate with the Cymulate API, make secure requests, and manage tokens. Both synchronous and asynchronous examples are provided.

### Synchronous Example

```python
import json
from cymulate_oauth2_client import CymulateOAuth2Client
from requests.exceptions import HTTPError

def main():
    # Initialize the OAuth2 client with your credentials and base URL
    client = CymulateOAuth2Client(
        client_id='your_client_id',         # Your Cymulate OAuth2 client_id
        client_secret='your_client_secret', # Your Cymulate OAuth2 client_secret
        base_url='https://api.cymulate.com' # The Cymulate API base URL (adjust based on your region)
    )

    try:
        # Example 1: Make a GET request to a secure resource
        response = client.get(path='/v1/browsing/templates')
        print("GET response:", json.dumps(response, indent=2))

        # Example 2: Make a POST request to a secure resource
        # data = {'key': 'value'}
        # response = client.post(path='/msfinding/api/v2/filters', json=data)
        # print("POST response:", json.dumps(response, indent=2))

    except HTTPError as e:
        # Handle HTTP errors separately
        try:
            error_message = e.response.json()
        except ValueError:
            # Response is not JSON formatted
            error_message = e.response.text
        print(f"HTTP error occurred: {e}")
        print(f"Response content: {json.dumps(error_message, indent=2)}")
    except Exception as e:
        # Handle all other exceptions
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
```

### Asynchronous Example

For environments that support asynchronous programming, you can use the asynchronous methods provided by `CymulateOAuth2Client`.

```python
import json
import asyncio
from cymulate_oauth2_client import CymulateOAuth2Client
from requests.exceptions import HTTPError

async def async_main():
    # Initialize the OAuth2 client with your credentials and base URL
    client = CymulateOAuth2Client(
        client_id='your_client_id',         # Your Cymulate OAuth2 client_id
        client_secret='your_client_secret', # Your Cymulate OAuth2 client_secret
        base_url='https://api.cymulate.com' # The Cymulate API base URL (adjust based on your region)
    )

    try:
        # Example 1: Make a GET request to a secure resource asynchronously
        async_response = await client.aget(path='/v1/browsing/templates')
        print("Async GET response:", json.dumps(async_response, indent=2))

        # Example 2: Make a POST request to a secure resource asynchronously
        # async_data = {'key': 'value'}
        # async_response = await client.apost(path='/msfinding/api/v2/filters', json=async_data)
        # print("Async POST response:", json.dumps(async_response, indent=2))

    except HTTPError as e:
        # Handle HTTP errors separately
        try:
            error_message = e.response.json()
        except ValueError:
            # Response is not JSON formatted
            error_message = e.response.text
        print(f"HTTP error occurred: {e}")
        print(f"Response content: {json.dumps(error_message, indent=2)}")
    except Exception as e:
        # Handle all other exceptions
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Run asynchronous example
    asyncio.run(async_main())
```

### API URL Configuration

Cymulate provides different API endpoints depending on your region. Ensure you use the correct base URL for your environment:

- **US:** `https://us-api.cymulate.com`
- **EU:** `https://api.cymulate.com`

For detailed API documentation, refer to the appropriate link based on your region:

- **US API Documentation:** [https://us-api.cymulate.com/docs](https://us-api.cymulate.com/docs)
- **EU API Documentation:** [https://api.cymulate.com/docs](https://api.cymulate.com/docs)

### Key Methods

- `get(url, **kwargs)`: Sends a GET request to a secure resource.
- `post(url, data=None, json=None, **kwargs)`: Sends a POST request to a secure resource.
- `put(url, data=None, **kwargs)`: Sends a PUT request to a secure resource.
- `delete(url, **kwargs)`: Sends a DELETE request to a secure resource.
- `aget(url, **kwargs)`: Asynchronously sends a GET request.
- `apost(url, data=None, json=None, **kwargs)`: Asynchronously sends a POST request.
- `aput(url, data=None, **kwargs)`: Asynchronously sends a PUT request.
- `adelete(url, **kwargs)`: Asynchronously sends a DELETE request.

### Exception Handling

This client handles common HTTP exceptions such as connection errors, timeouts, and authentication errors. It also automatically refreshes or obtains a new token if the current token is expired or invalid, retrying the request up to the configured number of retries.

### Logging

The client leverages Python’s built-in logging module to log important events, such as token refreshes, errors, and warnings. Logs can be configured to suit your needs.

## License

This project is licensed under the MIT License. For more information, see the [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! If you have suggestions, find a bug, or want to improve the code, please open an issue or submit a pull request.

## Contact

For any inquiries or support, please contact Cymulate at [support@cymulate.com](mailto:support@cymulate.com).
