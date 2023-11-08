import csv
import sys
import requests
import argparse


def main(short_name,apn_segment_code,buyer_seat_id):
    cookies = {}
    #APN API credentials
    credential = {"env_type":"1296","data":"{\"auth\": {\"username\":\"adsafe_admin\",\"password\": \"alksjdflk\"}}"}
    dmp_credential = {"env_type":"1296","data":"{\"auth\": {\"username\":\"ias_member_user\",\"password\": \"Pa$$w0rd\"}}"}
    
    #Authenticate APN API, obtain cookies
    cookies = authenticate(credential)

    #Create Segment in APN using "Segment Service". Retrieve segment id (can be searched for in console)
    segment_id = create_segment(short_name,apn_segment_code,cookies)

    #Authenticate APN DMP API, obtain cookies
    cookies = authenticate(dmp_credential)

    #POST segment into keyword billing category using the "Segment Billing Category Service". Obtain APN DMP ID 
    apn_dmp_id = map_to_kw_billing_cat(segment_id,cookies)

    #Use buyer seat id to obtain data member sharing id using the "Member Data Sharing Service"
    member_data_sharing_id = get_member_data_sharing_id(buyer_seat_id,cookies)

    #Append the segment to the data sharing record using Member Data Sharing Service
    append_to_data_sharing_seg_list(buyer_seat_id,member_data_sharing_id,segment_id,cookies)

    print("\nAPN Segment ID: "+str(segment_id)+'\n')
    print("\nAPN DMP ID: "+str(apn_dmp_id)+'\n')

def authenticate(credential):
    cookies = {}
    response = requests.post('https://api.adnxs.com/auth', cookies=cookies, data=credential['data'])
    return response.cookies

def authenticate(credential):
    cookies = {}
    response = requests.post('https://api.adnxs.com/auth', cookies=cookies, data=credential['data'])
    return response.cookies

def create_segment(short_name,apn_segment_code,cookies):
    json_request = '{"segment":{"member_id":1296,"short_name":"'+short_name+'","code":"'+apn_segment_code+'","price":0.00}}'
    response = requests.post('https://api.adnxs.com/segment/1296', cookies=cookies, data=json_request)
    print(response.text)
    response_json = response.json()
    return response_json['response']['segment']['id']

def map_to_kw_billing_cat(segment_id,cookies):
    json_request = '{"segment-billing-category":{"active":true,"data_provider_id":1296,"data_category_id":8765,"segment_id":'\
        +str(segment_id)+',"is_public":false}}'
    response = requests.post('https://api.adnxs.com/segment-billing-category?member_id=1296', cookies=cookies, data=json_request)
    print(response.text)
    response_json = response.json()
    return response_json['response']['segment-billing-category'][0]['id']

def get_member_data_sharing_id(buyer_seat_id,cookies):
    response = requests.get('https://api.adnxs.com/member-data-sharing?data_member_id=1296&buyer_member_id='+str(buyer_seat_id), cookies=cookies)
    print(response.text)
    response_json = response.json()
    return response_json['response']['member_data_sharings'][0]['id']

def append_to_data_sharing_seg_list(buyer_seat_id,member_data_sharing_id,segment_id,cookies):
    json_request = '{"member_data_sharing":{"buyer_member_id":'+ str(buyer_seat_id) +',"data_member_id":1296,"id":'+\
         str(member_data_sharing_id) + ',"segment_exposure": "list", "segments": [{"id":'+str(segment_id)+'}]}}'
    response = requests.put('https://api.adnxs.com/member-data-sharing?data_member_id=1296&id='+ str(member_data_sharing_id) +'& \
        append=true',cookies=cookies, data=json_request)
    print(response.text)

def read_csv():
    new_data = []
    with open(sys.argv[1]) as csvFile:
        rowReader = csv.reader(csvFile, delimiter=',', quotechar='|')
        for row in rowReader:
            new_data.append([row[0],row[1],row[2]])
    
    return new_data

if __name__ == "__main__":
    '''parser = argparse.ArgumentParser(description="Deploy a keyword segment to a buyer seat on Appnexus")
    
    parser.add_argument("short_name", metavar="short_name", 
                        help="Enter short name. Example: IAS KW List:1451")
    parser.add_argument("apn_segment_code", metavar="apn_segment_code", 
                        help="Enter APN Segment Code. Example: IAS_11178_1451_KW")
    parser.add_argument("buyer_seat_id", metavar="buyer_seat_id", 
                        help="Enter the Buyer Seat ID. Example: 6926")
        args = parser.parse_args()'''
    data = read_csv()
    for row in data:
        main(row[0],row[1],row[2])   
