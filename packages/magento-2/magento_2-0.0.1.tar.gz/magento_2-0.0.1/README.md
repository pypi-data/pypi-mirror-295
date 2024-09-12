Magento 2 API Package
=====================

Overview
--------

This package provides an interface for interacting with the Magento 2 API, allowing you to perform various operations such as logging in, making API requests, and handling data. It is designed to simplify interactions with the Magento 2 API by managing authentication and making HTTP requests.

Features
--------

-   User authentication with Magento 2 API
-   Making various types of API requests (GET, POST, PUT, DELETE)
-   Token-based session management
-   Handling API responses and errors

Installation
------------

To use this package, you need to have Python installed on your system. Install the package using pip:

bash

Copy code

`pip install magento-api-2`

Alternatively, clone the repository and install it manually:

bash

Copy code

`git clone https://github.com/Gunn1/Magento-API.git
cd Magento-API
pip install .`

Usage
-----

### Authentication

The `LoginController` class handles user authentication and manages the login session. Here's how you can use it:

python

Copy code

`from magento_api import LoginController, Magento

# Initialize the LoginController with your Magento credentials
login_controller = LoginController(username='your_username', password='your_password')

# Log in to Magento
login_controller.login()

# Check if the user is logged in
if login_controller.is_logged_in():
    print("User is logged in.")
else:
    print("User is not logged in.")`

### Making API Requests

Once authenticated, you can make API requests using the `Magento` class. Here's an example:

python

Copy code

`from magento_api import Magento

# Initialize the Magento class with the LoginController
magento = Magento(login_controller=login_controller)

# Make a GET request to the API
response = magento.make_api_request(
    endpoint='https://your-magento-store.com/rest/V1/orders',
    request_type='get'
)

print(response)`

### Classes

#### `LoginController`

A class for managing the login process to the Magento 2 API.

**Attributes:**

-   `token`: Stores the authentication token.
-   `store`: The store code used in the API endpoint.
-   `api_endpoint`: The base URL for the Magento 2 API.
-   `logged_in`: Indicates if the user is logged in.
-   `login_time`: The timestamp when the user logged in.
-   `token_expiration`: The expiration time for the token (4 hours by default).

**Methods:**

-   `__init__(self, username=None, password=None)`: Initializes the controller. Prompts for credentials if not provided.
-   `login(self)`: Logs in the user and stores the token. Raises `InvalidCredentialsError` if login fails.
-   `is_logged_in(self)`: Checks if the user is logged in by verifying the token's validity. Returns `True` or `False`.

#### `Magento`

A class for making API requests using an authenticated session.

**Attributes:**

-   `login_controller`: An instance of `LoginController` used for authentication.

**Methods:**

-   `make_api_request(self, endpoint: str, params: Params = None, request_type: str = "get", data: dict = None, json: dict = None) -> dict`: Makes an API request to the specified endpoint.

    **Parameters:**

    -   `endpoint` (str): The API endpoint to send the request to.
    -   `params` (Optional[Params]): Query parameters for the request.
    -   `request_type` (str): Type of HTTP request ("get", "post", "put", "delete").
    -   `data` (Optional[dict]): Data to send with the request (for POST and PUT requests).
    -   `json` (Optional[dict]): JSON data to send with the request (for POST and PUT requests).

    **Raises:**

    -   `InvalidCredentialsError`: If the user is not logged in.
    -   `PermissionDeniedError`: If the request is unauthorized.
    -   `APIRequestError`: If the request fails.

    **Returns:**

    -   `dict`: The response data from the API request.

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue to report bugs or request new features.

License
-------

This package is licensed under the MIT License. See the LICENSE file for more details.

Contact
-------

For questions or support, please contact tylerjgunn@gmail.com.
