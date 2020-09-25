import requests
import base64
import getpass

#Get info
ibserver = input("IB Server: ")
wapiversion = input("WAPI Version: ")
username = input("user: ")
passwd = getpass.getpass("pass: ")
changeto = input("CNAME Destination: ")

data = username + ':' + passwd

# Standard Base64 Encoding
encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

urlsfile = open("urllist.txt")

for name in urlsfile:
    try:
        #URL that looks for the existing record
        url = "https://" + ibserver + "/wapi/v" + wapiversion + "/record:cname?name=" + name.strip()

        payload = {}
        headers = {
          'Authorization': 'Basic ' + encodedStr,
        }

        response = requests.request("GET", url, headers=headers, data = payload, verify=False)

        print(response.json())

        referenceurl = response.json()[0]['_ref']

        #Make a new URL with _ref to use in the PUT request
        url = "https://" + ibserver + "/wapi/v" + wapiversion + "/" + referenceurl

        #Payload
        payload = "{\n    \"canonical\" : \"" + changeto + "\"\n}"
        headers = {
          'Authorization': 'Basic ' + encodedStr,
          'Content-Type': 'application/json',
        }

        response = requests.request("PUT", url, headers=headers, data = payload, verify=False)
        
        print(response.json())

    except:
        print("failed for " + name)

urlsfile.close()
