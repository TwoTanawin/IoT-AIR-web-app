import boto3
from decimal import Decimal


last_data = []

def dec_to_int(decimal_list):
    # Convert Decimal objects to integers using list comprehension
    int_list = [int(decimal) for decimal in decimal_list]

    return int_list  # Output: [8, 14, 18]

try:
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Assuming 'pms3003_data' is the name of your DynamoDB table
    table = dynamodb.Table('pms3003_data')

    # Perform the scan operation to get all items
    response = table.scan()

    # Retrieve items from the response
    items = response['Items']

    # Check if there are more items to retrieve
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    # # If there are items, sort them by timestamp
    # if items:
    #     sorted_items = sorted(items, key=lambda x: x['timestamp'])
    #     latest_item = sorted_items[-1]  # Get the latest item based on timestamp

    #     # Print the latest item's details
    #     print("Latest Data:")
    #     for key, value in latest_item.items():
    #         # print(f"{key}: {value}")
    #         last_data.append(value)
            
    #     # last_data = last_data[:-2]
        
    #     # last_data = dec_to_int(last_data)
    #     print(last_data)
    if items:
        sorted_items = sorted(items, key=lambda x: x['timestamp'], reverse=True)
        latest_items = sorted_items[:10]  # Get the last 10 items based on timestamp (most recent)

        # Print the latest 10 items' details
        print("Latest 10 Data:")
        # for item in latest_items:
        #     print(item)
            
        for entry in latest_items:
            # entry.pop('timestamp', None)
            entry.pop('station_number', None)

        # print(latest_items)
        
            # Iterate over each item in the entry
            for key, value in entry.items():
                print(f"{key}: {value}")
                last_data.append(value)
        
        print(last_data)
            
    else:
        print("No data found in the database.")

except Exception as e:
    print("An error occurred:", e)
