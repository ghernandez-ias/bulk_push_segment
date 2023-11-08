import csv
import sys
import requests
import argparse


def main(segment_id,buyer_seat_id):
    cookies = {}
    #APN API credentials
    credential = {"env_type":"1296","data":"{\"auth\": {\"username\":\"adsafe_admin\",\"password\": \"alksjdflk\"}}"}
    dmp_credential = {"env_type":"1296","data":"{\"auth\": {\"username\":\"ias_member_user\",\"password\": \"Pa$$w0rd\"}}"}
    
    #Authenticate APN API, obtain cookies
    cookies = authenticate(credential)

    #Authenticate APN DMP API, obtain cookies
    cookies = authenticate(dmp_credential)

    #Use buyer seat id to obtain data member sharing id using the "Member Data Sharing Service"
    member_data_sharing_id = get_member_data_sharing_id(buyer_seat_id,cookies)

    #Append the segment to the data sharing record using Member Data Sharing Service
    append_to_data_sharing_seg_list(buyer_seat_id,member_data_sharing_id,segment_id,cookies)

def authenticate(credential):
    cookies = {}
    response = requests.post('https://api.adnxs.com/auth', cookies=cookies, data=credential['data'])
    return response.cookies

def authenticate(credential):
    cookies = {}
    response = requests.post('https://api.adnxs.com/auth', cookies=cookies, data=credential['data'])
    return response.cookies

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
    segments = []
    with open(sys.argv[1]) as csvFile:
        rowReader = csv.reader(csvFile, delimiter=',', quotechar='|')
        for row in rowReader:
            segments.append(row[0])
    
    return segments

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
    buyer_seat = sys.argv[2]
    for segment in data:
        main(segment,buyer_seat)
