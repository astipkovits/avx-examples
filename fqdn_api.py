import requests
import json

CONTROLLER_URL = ""
CONTROLLER_USER = ""
CONTROLLER_PASS = ""


def authenticate_controller(controller_url, controller_user, controller_password):
    # Get a session token
    url = "https://" + controller_url + "/v1/api"
    payload = {'action': 'login', 'username': controller_user, 'password': controller_password}
    response = requests.request("POST", url, headers={}, data=payload, verify=False)

    responseDict = json.loads(response.text)

    if responseDict["return"] == False:
        print("Login failed, check credentials.")
        return ""
    else:
        cid = json.loads(response.text)["CID"]

    return cid


def create_fqdn_tag(controller_url, cid, tag_name, domain_names, gw_name, source_ips):
    url = "https://" + controller_url + "/v1/api"

    # Add tag
    payload = {'action': 'add_fqdn_filter_tag', 'CID': cid, 'tag_name': tag_name}
    response = requests.request("POST", url, headers={}, data=payload, verify=False)
    responseDict = json.loads(response.text)
    if responseDict["return"] == False:
        print(responseDict)

    # Set Tag domain names
    payload = {'action': 'set_fqdn_filter_tag_domain_names', 'CID': cid, 'tag_name': tag_name}

    #Add domains to the payload
    i = 0
    for domain in domain_names:
        domainFqdn = "domain_names[{}][fqdn]".format(i)
        domainProto = "domain_names[{}][proto]".format(i)
        domainPort = "domain_names[{}][port]".format(i)
        payload[domainFqdn] = domain["fqdn"]
        payload[domainProto] = domain["proto"]
        payload[domainPort] = domain["port"]

    response = requests.request("POST", url, headers={}, data=payload, verify=False)
    responseDict = json.loads(response.text)
    if responseDict["return"] == False:
        print(responseDict)

    # Set filter tag color (black or white), white is default
    # payload = {'action': 'set_fqdn_filter_tag_color', 'CID': cid, 'tag_name': tag_name, "color": "white"}
    # response = requests.request("POST", url, headers={}, data=payload, verify=False)
    # responseDict = json.loads(response.text)
    # if responseDict["return"] == False:
    #     print(responseDict)

    # Enable tag
    payload = {'action': 'set_fqdn_filter_tag_state', 'CID': cid, 'tag_name': tag_name, "status": "enabled"}
    response = requests.request("POST", url, headers={}, data=payload, verify=False)
    responseDict = json.loads(response.text)
    if responseDict["return"] == False:
        print(responseDict)

    # Attach tag to gateway
    payload = {'action': 'attach_fqdn_filter_tag_to_gw', 'CID': cid, 'tag_name': tag_name, "gw_name": gw_name}
    response = requests.request("POST", url, headers={}, data=payload, verify=False)
    responseDict = json.loads(response.text)
    if responseDict["return"] == False:
        print(responseDict)

    # Update FQDN tag source IP filters
    payload = {'action': 'update_fqdn_filter_tag_source_ip_filters', 'CID': cid, 'tag_name': tag_name,
               "gateway_name": gw_name, "source_ips": source_ips}
    response = requests.request("POST", url, headers={}, data=payload, verify=False)
    responseDict = json.loads(response.text)
    if responseDict["return"] == False:
        print(responseDict)

    return


if __name__ == '__main__':
    tag_name = "my_fun_tag"
    domain_names = [{"fqdn": "test.com", "proto": "tcp", "port": "443"}]
    gw_name = "aws-db-node"

    # Update with your prod number to match Azure APP VNET CIDR
    source_ips = [""]

    cid = authenticate_controller(CONTROLLER_URL, CONTROLLER_USER, CONTROLLER_PASS)

    if cid != "":
        create_fqdn_tag(CONTROLLER_URL, cid, tag_name, domain_names, gw_name, source_ips)
