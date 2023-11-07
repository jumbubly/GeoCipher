# GeoCipher

![GeoCipher](https://raw.githubusercontent.com/jumbubly/GeoCipher/master/geocipher.PNG)

GeoCipher is a Python application that allows you to retrieve geographical information based on IP addresses and coordinates (latitude and longitude). This tool provides a user-friendly graphical interface using PyQt6, making it easy to use.

## Features

IP Geolocation: Enter an IP address, and GeoCipher will fetch its geographical details, including latitude, longitude, city, and country.

Coordinate Geolocation: Input latitude and longitude in a comma-separated format, and GeoCipher will provide information such as the city, street, and country.

User Interface: GeoCipher offers a simple and intuitive graphical user interface (GUI) for effortless interaction.

Results Display: The tool displays the results in a separate window with animated text for a user-friendly experience.

## Prerequisites

Before running GeoCipher, make sure you have the following dependencies installed:

Python 3.x

PyQt6

requests

## Installation Requirements

To get started with GeoCipher, follow these simple steps:

1. Clone this repository to your local machine.

2. Install PyQt6 & requests if you haven't already:

   ```bash
   pip install PyQt6 requests

## Getting Started

Clone the repository to your local machine:

```bash```
    git clone <https://github.com/jumbubly/GeoCipher.git>

Change to the project directory:

```bash```
    cd GeoCipher

Run the GeoCipher application:

```bash```
    python geocipher.py

The GUI will open, and you can start using GeoCipher to retrieve geographical data.

## Usage

IP Geolocation: To get geographical data based on an IP address, follow these steps:

a. Enter the IP address in the "Enter IP Address" field.

b. Click the "Get IP Data" button.

c. The results will be displayed in a separate window.

Coordinate Geolocation: To retrieve geographical data using latitude and longitude, follow these steps:

a. Enter the latitude and longitude in the "Enter Latitude and Longitude" field, separated by a comma.

b. Click the "Get Coordinate Data" button.

c. The results will be displayed in a separate window.

Reset Data: Click the "Reset Data" button to clear the input fields.

## Screenshots

![IP Geolocation](https://raw.githubusercontent.com/jumbubly/GeoCipher/master/ipgeo.PNG)

![Coordinate Geolocation](https://raw.githubusercontent.com/jumbubly/GeoCipher/master/cordgeo.PNG)

## Contributing

If you want to contribute to this project, please follow these steps:

Fork the repository on GitHub.

Create a new branch with a descriptive name for your feature or bug fix.

Make your changes and commit them with clear messages.

Push your branch to your forked repository.

Create a pull request to the main repository's master branch.

Wait for feedback and approval from the maintainers.

## License

This project is protected by copyright, and all rights are reserved. Unauthorized use, reproduction, or distribution of this code or any associated materials is prohibited.

## Acknowledgments

This project was created by ReKing.

## Disclaimer

This tool is provided for educational and informational purposes only. Please use it responsibly and ensure compliance with all relevant laws and regulations when using geographical data.

Enjoy using GeoCipher! If you encounter any issues or have suggestions for improvement, feel free to open an issue on GitHub.
