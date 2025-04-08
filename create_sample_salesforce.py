from pymongo import MongoClient
import time
import datetime
import random
import os

# MongoDB destionation connection details
MONGO_URI_CLUSTER2 = os.environ.get("CLUSTER2_URI")  # Replace with your cluster2 connection string
DATABASE_NAME_CLUSTER2 = "salesforce"
COLLECTION_NAME_CLUSTER2 = "locationData"

# MongoDB source connection details
MONGO_URI = os.environ.get("CLUSTER1_URI")  # Replace with your cluster1 MongoDB connection
DATABASE_NAME = "sample_salesforce"
COLLECTION_NAME = "cdc_events"
NUM_DOCUMENTS = 1000
INSERTION_INTERVAL = 1  # Seconds between insertions

def generate_cdc_event(doc_id):
    timestamp = int(time.time() * 1000)
    random_change_type = random.choice(["CREATE", "UPDATE", "DELETE"])

    return {
        "timestamp": timestamp,
        "timestampType": "CREATE_TIME",
        "partition": random.randint(0, 5),
        "offset": random.randint(1, 100),
        "key": "",
        "value": {
            "Id": f"131D7000000oiSJIA{doc_id + 1:04d}",
            "ReplayId": str(20422023 + doc_id),
            "ChangeEventHeader": {
                "entityName": "Location",
                "recordIds": [
                    f"131D7000000oiSJIA{doc_id + 1:04d}"
                ],
                "changeType": random_change_type,
                "changedFields": random.sample([
                    "OwnerId", "Name", "LocationType", "Latitude", "Longitude",
                    "Description", "Account__c", "Address__Street__s"
                ], random.randint(0, 3)) if random_change_type == "UPDATE" else [],
                "changeOrigin": "com/salesforce/api/rest/63.0",
                "transactionKey": f"{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(1000, 9999):04x}-{random.randint(100000000000, 999999999999):012x}",
                "sequenceNumber": doc_id + 1,
                "commitTimestamp": int((datetime.datetime(2025, 3, 1, 0, 0, 0) + datetime.timedelta(seconds=doc_id * 10)).timestamp() * 1000),
                "commitUser": f"005D700000GBxwzIA{chr(ord('A') + ((doc_id + 5) % 26))}{((doc_id + 5) // 26):02d}",
                "commitNumber": 12226339400407 + doc_id
            },
            "OwnerId": f"005D700000GBxwzIA{chr(ord('A') + ((doc_id + 10) % 26))}{((doc_id + 10) // 26):02d}" if random.random() < 0.5 else None,
            "Name": f"Location {doc_id + 1}" if random.random() < 0.7 else None,
            "CreatedDate": datetime.datetime(2025, 3, 1, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)).isoformat() + "Z" if random_change_type == "CREATE" or random.random() < 0.3 else None,
            "CreatedById": None,  # Will be set in the main loop
            "LastModifiedDate": datetime.datetime(2025, 3, 1 + (doc_id // 100), random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)).isoformat() + "Z" if random_change_type == "UPDATE" or random.random() < 0.4 else None,
            "LastModifiedById": f"005D700000GBxwzIA{chr(ord('A') + ((doc_id + 15) % 26))}{((doc_id + 15) // 26):02d}" if random_change_type == "UPDATE" or random.random() < 0.4 else None,
            "LocationType": random.choice(["Warehouse", "Store", "Office"]) if random.random() < 0.6 else None,
            "Latitude": round(random.uniform(-90, 90), 6) if random.random() < 0.5 else None,
            "Longitude": round(random.uniform(-180, 180), 6) if random.random() < 0.5 else None,
            "Location": None,
            "Description": f"Description for Location {doc_id + 1}" if random.random() < 0.4 else None,
            "DrivingDirections": None,
            "TimeZone": random.choice(["America/Los_Angeles", "America/New_York", "Europe/London"]) if random.random() < 0.3 else None,
            "ParentLocationId": None,
            "PossessionDate": None,
            "ConstructionStartDate": None,
            "ConstructionEndDate": None,
            "OpenDate": None,
            "CloseDate": None,
            "RemodelStartDate": None,
            "RemodelEndDate": None,
            "IsMobile": random.choice([True, False]) if random.random() < 0.2 else None,
            "IsInventoryLocation": random.choice([True, False]) if random.random() < 0.2 else None,
            "VisitorAddressId": None,
            "RootLocationId": None,
            "LocationLevel": random.randint(1, 5) if random.random() < 0.3 else None,
            "ExternalReference": f"EXT-REF-{doc_id + 1}" if random.random() < 0.4 else None,
            "LogoId": None,
            "Account__c": None,  # Will be set in the main loop
            "Address__Street__s": f"{random.randint(100, 999)} Main St" if random.random() < 0.6 else None,
            "Address__City__s": random.choice(["Minneapolis", "St. Paul", "Bloomington"]) if random.random() < 0.6 else None,
            "Address__PostalCode__s": f"{random.randint(10000, 99999)}" if random.random() < 0.6 else None,
            "Address__StateCode__s": "MN" if random.random() < 0.6 else None,
            "Address__CountryCode__s": "US" if random.random() < 0.6 else None,
            "Address__Latitude__s": round(random.uniform(44, 45), 6) if random.random() < 0.4 else None,
            "Address__Longitude__s": round(random.uniform(-93.1, -93.3), 6) if random.random() < 0.4 else None,
            "Address__GeocodeAccuracy__s": random.choice(["High", "Medium", "Low"]) if random.random() < 0.4 else None,
            "Address__c": None,
            "Company_Name__c": f"Company {doc_id + 1}" if random.random() < 0.5 else None,
            "Is_Default__c": random.choice([True, False]) if random.random() < 0.1 else None,
            "Recipient_Name__c": f"Contact {doc_id + 1}" if random.random() < 0.3 else None,
            "Phone__c": f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}" if random.random() < 0.4 else None,
            "_ObjectType": "LocationChangeEvent",
            "_EventType": "T9-Lq3gwb5y8VjpFVUNgGA"
        },
        "headers": []
    }

if __name__ == "__main__":    
    client_cluster2 = None
    try:
        # Connect to cluster2
        client_cluster2 = MongoClient(MONGO_URI_CLUSTER2)
        db_cluster2 = client_cluster2[DATABASE_NAME_CLUSTER2]
        collection_cluster2 = db_cluster2[COLLECTION_NAME_CLUSTER2]

        # Drop the salesforce.locationData collection on cluster2
        if COLLECTION_NAME_CLUSTER2 in db_cluster2.list_collection_names():
            collection_cluster2.drop()
            print(f"Dropped collection: {DATABASE_NAME_CLUSTER2}.{COLLECTION_NAME_CLUSTER2} on cluster2")
        else:
            print(f"Collection {DATABASE_NAME_CLUSTER2}.{COLLECTION_NAME_CLUSTER2} does not exist on cluster2, proceeding.")

    except Exception as e:
        print(f"An error occurred while connecting to or dropping collection on cluster2: {e}")
    finally:
        if client_cluster2:
            client_cluster2.close()

    client = None
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Drop the collection if it exists
        if COLLECTION_NAME in db.list_collection_names():
            collection.drop()
            print(f"Dropped collection: {DATABASE_NAME}.{COLLECTION_NAME}")
        else:
            print(f"Collection {DATABASE_NAME}.{COLLECTION_NAME} does not exist, proceeding with creation.")

        print(f"Inserting {NUM_DOCUMENTS} documents into {DATABASE_NAME}.{COLLECTION_NAME} with a {INSERTION_INTERVAL} second interval...")

        for i in range(NUM_DOCUMENTS):
            start_time = time.time()
            cdc_event = generate_cdc_event(i)
            # Ensure CreatedById and Account__c are monotonically increasing in the desired format
            cdc_event["value"]["CreatedById"] = f"{i + 1:04d}"
            cdc_event["value"]["Account__c"] = f"A{i + 1:04d}"

            collection.insert_one(cdc_event)
            print(f"Inserted document {i + 1} (CreatedById: {cdc_event['value']['CreatedById']}, Account__c: {cdc_event['value']['Account__c']})")

            elapsed_time = time.time() - start_time
            sleep_duration = max(0, INSERTION_INTERVAL - elapsed_time)
            time.sleep(sleep_duration)

        print("Finished inserting all documents.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()