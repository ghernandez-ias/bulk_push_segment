# Xandr Bulk Segment Push
This script greatly increases to speed at which a keyword segment can be deployed. After the script is run the segment will be privately available to a select buyer seat within the Data Marketplace. Note: Keyword segments area always added to the Web endpoint, not the Mobile, since they are URL based.

## CSV Input
The input file should have three columns:
1. Short name. This represents what will be seen by the buyer within the xandr platform UI. Ex. IAS KW List:1451
2. APN segment code. This represents the code sent in the segment API endpoint response. Ex. IAS_11178_1451_KW
3. Buyer Seat Id. This is obtained from the buyer and allows the segment to be privately available to specific buyers

## Services used in this script:

1. Segment Service (latest public docs may no longer align with endpoints used)
2. Segment Billing Category Service
3. Member Data Sharing Service


## Running the Script & Arguments 
To run the script, use the following argument:
1. CSV file name (ex. "APNSeg_Desktop_Example_Input.csv")

`python app_bulk_push_segment.py APNSeg_Desktop_Example_Input.csv`

Note: Script can error when special or hidden characters are present