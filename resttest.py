import http.client
import ssl
import json
import config
import logging
import re

httpClient = None
apiKey = config.apiKey

if __name__ == "__main__":
    # To avoid ssl certificates issue in mac machines.
    ssl._create_default_https_context = ssl._create_unverified_context
    # setting up logger.
    logging.basicConfig(filename='RestTestApp.log', level=logging.INFO, filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    print("Please enter the macAddress: ")
    macAddress = input()
    # Validating the given mac address.
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()):
        logging.info("Validation passed.")
        logging.info('Finding the details of the given macAddress ' + macAddress)
        try:
            logging.debug("Inside the try block")
            httpClient = http.client.HTTPSConnection('api.macaddress.io')
            logging.info("Opening an HTTPS connection with macaddress.io")
            httpClient.request('GET', "/v1?apiKey={}&output=json&search={}".format(apiKey, macAddress))
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            logging.info("Response from the API:  \n" + str(result))
            with open('data.txt', 'w') as outfile:
                json.dump(result, outfile)

            print("\n\n\n")
            print("####################################################################")
            print("Company Details: \n" + result['vendorDetails']['companyName'])
            print(result['vendorDetails']['companyAddress'])
            print("####################################################################")

        except Exception as e:
            logging.info("Caught exception while fetching API response.\n" + str(e))
            print(e)

        finally:
            if httpClient:
                httpClient.close()
                logging.info("Closing the HTTPS connection with macaddress.io")
    else:
        logging.info("Given mac address {} is invalid.".format(macAddress))
        print("\n\nGiven address {} is invalid. Please provide correct mac address.".format(macAddress))
