import ssl
import json
import socket
import config
import logging
import re
import sys

apiKey = config.apiKey
port = 443  # default port for HTTPS connection.
hostname = config.hostname


class RestClient:
    def execute_API_Call(self, macAddr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s = ssl.wrap_socket(s)
            logging.info("Socket successfully created")
        except socket.error as err:
            logging.error("socket creation failed with error: " + str(err))

        try:
            host_ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            print("Error while resolving the host.")
            sys.exit()

        s.connect((host_ip, port))
        logging.info("The socket has successfully connected to macaddress.io on port 443")

        request = "GET /v1?apiKey={}&output=json&search={} HTTP/1.1\r\nHost: {}\r\n\r\n"\
                  .format(apiKey, macAddr, hostname)
        s.sendall(bytes(request, encoding='utf-8'))
        string = str(s.recv(4096), 'utf-8')
        s.close()

        logging.info("Response received from the host: \n")
        logging.info(string)
        httpResponse, partition, json_data = string.partition('{"')
        data = json.loads(partition + json_data)
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        return data


if __name__ == "__main__":
    # To avoid ssl certificates issue in mac machines.
    ssl._create_default_https_context = ssl._create_unverified_context
    # setting up logger.
    logging.basicConfig(filename='RestTestApp.log', level=logging.INFO, filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    print("==========================================================================")
    print("            RestTest: Find the details of your mac address")
    print("==========================================================================\n")
    print("Please enter the macAddress: ")
    macAddress = input()
    # Validating the given mac address.
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()):
        logging.info("MAC Address validation passed.")
        logging.info('Finding the details of the given macAddress: ' + macAddress)

        data = RestClient().execute_API_Call(macAddress)
        if "vendorDetails" in data:
            print("\n\n")
            print("####################################################################")
            print("Company Details: \n" + data['vendorDetails']['companyName'])
            print(data['vendorDetails']['companyAddress'])
            print("####################################################################")
        else:
            print("\n\n\n")
            print("Sorry. Could not find vendor details of the given Mac Address.")

    else:
        logging.info("Given mac address {} is invalid.".format(macAddress))
        print("\n\nGiven address {} is invalid. Please provide correct mac address.".format(macAddress))
