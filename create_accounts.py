from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime
import os

# MongoDB connection details
MONGO_URI = os.environ.get("CLUSTER2_URI")  # Replace with your MongoDB connection string
DATABASE_NAME = "accounts"
COLLECTION_NAME = "info"

def generate_random_user():
    """Generates a dictionary representing a random user."""
    fake = Faker()
    user = {
        "Name": f"{fake.first_name()} {fake.last_name()}",
        "Email": fake.email(),
        "Age": random.randint(18, 70),
        "City": fake.city(),
        "RegistrationDate": datetime.combine(fake.date_this_decade(), datetime.min.time())
    }
    return user

def insert_documents(num_documents=1000):
    """Connects to MongoDB and inserts the specified number of documents."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        documents_to_insert = []
        for i in range(1, num_documents + 1):
            user_data = generate_random_user()
            document = {
                "sfdcId": f"A{i:04d}",  # Added AccountId field
                "customerId": f"C{i:04d}",  # Added customerId field
                **user_data
            }
            documents_to_insert.append(document)

        if documents_to_insert:
            result = collection.insert_many(documents_to_insert)
            print(f"Inserted {len(result.inserted_ids)} documents into '{COLLECTION_NAME}' collection in '{DATABASE_NAME}' database.")
        else:
            print("No documents to insert.")

    except ConnectionError as e:
        print(f"Could not connect to MongoDB: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    insert_documents()
