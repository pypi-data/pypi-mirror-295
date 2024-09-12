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

`pip install magento-2`

Alternatively, clone the repository and install it manually:

bash

Copy code

`git clone https://github.com/Gunn1/Magento-2-API.git
cd Magento-API
pip install .`

Usage
-----

### Authentication

The `LoginController` class handles user authentication and manages the login session. Here's how you can use it:

`from magento_2 import magento.LoginController, magento.Magento

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

`from magento_2 import magento.Magento

# Initialize the Magento class with the LoginController
magento = Magento(login_controller=login_controller)

# Make a GET request to the API
response = magento.make_api_request(
    endpoint='https://your-magento-store.com/rest/V1/orders',
    request_type='get'
)

print(response)`

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue to report bugs or request new features.

License
-------

This package is licensed under the MIT License. See the LICENSE file for more details.

Contact
-------

For questions or support, please contact tylerjgunn@gmail.com.
