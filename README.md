# RestTest
Finds details of a mac address.

The details of the given Mac address are fetched from macaddress.io
The given mac address is validated before sending the API request.
API connection does not use requests/urllib packages of python.
The API call is handled in a rudimentary HTTP client way.
The API key required to access the details is stored in a separate config file, for security and easy management.

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
The program also generates a log file.

Also, this python app can be dockerized, and can be run as an independant container.
Steps to create and run the docker container:

step 1:
docker build -t <docker_image_name> .
{to be run at the location where dockerfile is present}

step 2:
docker run -it <docker_image_name>
{-i stands for interactive mode. Program expects the input from the User.}