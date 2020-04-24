import ssl
import json
import config
import logging
import re
from RestClient import rest_client

apiKey = config.apiKey
port = 443  # default port for HTTPS connection.
hostname = config.hostname


class APICall:
    def prepare_request(self, macAddr):
        """
        prepare_request: Prepares the API request.
        :param self:                       self.
        :param macAddr:                    MacAddress collected from User.
        :return:                           String containing the Response from API.
        """
        request_method = "GET"
        request_path = "/v1".format(apiKey, macAddr)
        query_params_dict = {"apiKey": apiKey,
                             "output": "json",
                             "search": macAddress}
        headers = None
        request_body = None
        response = rest_client.execute_API_Call(self, request_method, port, request_path, hostname, query_params_dict,
                                                headers, request_body)
        logging.info("Response received from the host: \n")
        logging.info(response)
        return response

    def parse_API_response(self, response):
        """
        parse_API_response: Parses the string response.
        :param self:                       self.
        :param response:                   String response collected from User.
        :return:                           Dict containing the Response Json from.
        """
        if "HTTP/1.1 200 OK" in response:
            httpResponse, partition, json_data = response.partition('{"')
            data = json.loads(partition + json_data)
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)
            return data
        else:
            return response


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

        response = APICall().prepare_request(macAddress)
        data = APICall().parse_API_response(response)
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
