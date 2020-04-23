# RestTest
Finds details of a mac address.

The details of the given Mac address are fetched from macaddress.io
The given mac address is validated before sending the API request.
API connection does not use requests/urllib/http.client packages of python.
The API call is handled in a more rudimentary socket ssl programming way.
Socket connection is established with the host over the https port 443, and response is parsed to extract the Json.
The Hostname and API key required to access the details are stored in a separate config file, for security and easy management.

Input: Mac Address.

example:
Please enter the macAddress:
44:38:39:ff:ef:57

Output: Company name and details.

example:
####################################################################
Company Details:
Cumulus Networks, Inc
650 Castro Street, suite 120-245 Mountain View CA 94041 US
####################################################################

Though only company details are shown as output, All the details returned by the API are stored as a json file for future use.
The program also generates a log file, Log levels for the same can be set easily.

Also, this python app can be dockerized, and can be run as an independent container.
Steps to create and run the docker container:
(Assuming Docker is already installed and running on the machine)

step 1:
docker build -t <your_docker_image_name> .
{to be run at the location where dockerfile is present}

step 2:
docker run -it <your_docker_image_name>
{-i stands for interactive mode. Program expects some input from the User.}