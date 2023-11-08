# Xandr Bulk Segment Push
This script greatly increases to speed at which a keyword segment can be deployed. After the script is run the segment will be privately available to a select buyer seat within the Data Marketplace. Note: Keyword segments area always added to the Web endpoint, not the Mobile, since they are URL based.

## CSV Input
The input file should have only one column:
1. segment id

## Running the Script & Arguments 
To run the script, use the following argument:
1. CSV file name (ex. "APNSeg_Desktop_Example_Input.csv")

`python app_bulk_push_segment.py APNSeg_Desktop_Example_Input.csv buyer_seat_id`

Note: Script can error when special or hidden characters are present