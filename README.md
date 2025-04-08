Salesforce Data Integration with MongoDB Atlas and Kafka
This project demonstrates how to use MongoDB Atlas Stream Processing to transform and enrich Salesforce CDC (Change Data Capture) events in real-time. The data flow includes Kafka as a message broker, with both source and destination data stored in MongoDB Atlas clusters.

Setup Overview
Create a source MongoDB Atlas cluster (Cluster1)
Create a destination MongoDB Atlas cluster (Cluster2) and populate with user and account data
Connect Kafka to the source cluster using Confluent MongoDB Atlas Source connector
Configure Stream Processing in MongoDB Atlas
Run sample data generator to simulate Salesforce CDC events
Prerequisites
Before you begin, ensure you have the following installed and configured:

Python 3.6+ with the following packages:
pymongo - For MongoDB connectivity
faker - For generating sample data
random, datetime, time, os - Standard libraries used in scripts
MongoDB Atlas Account - Free tier is sufficient for testing
Confluent Cloud Account - For Kafka cluster and connectors
Environment Variables:
CLUSTER2_URI - MongoDB connection string for your destination cluster
CLUSTER1_URI - MongoDB connection string for your source cluster
You can install the required Python packages using:

Detailed Instructions
1. Create Source MongoDB Atlas Cluster
Log in to MongoDB Atlas
Click "Build a Database" and select your preferred cloud provider
Choose the "M0 Free Tier" for testing purposes
Name your cluster "Cluster1"
Create a database user with read/write privileges
Configure network access to allow connections from your IP address
Once the cluster is deployed, note the connection string for use in later steps
This cluster will serve as the source for Salesforce CDC events in our demo, emulating data that would normally come directly from Salesforce.

2. Create Destination MongoDB Atlas Cluster and Populate Reference Data
Follow the same steps as above to create a second MongoDB Atlas cluster
Name this cluster "Cluster2"
Create a database user with read/write privileges
Configure network access to allow connections from your IP address
Set the connection string as an environment variable:
Now populate the reference collections in Cluster2 by running:

These scripts will:

Create 1000 random user documents in the users.info collection, each with:
Unique ID (formatted as "0001", "0002", etc.)
Random name, email, age, city, and registration date
Create 1000 random account documents in the accounts.info collection, each with:
Salesforce ID (formatted as "A0001", "A0002", etc.)
Customer ID (formatted as "C0001", "C0002", etc.)
Random name, email, age, city, and registration date
3. Connect Kafka to Source MongoDB Atlas Cluster
Set up a Confluent MongoDB Atlas Source connector to stream changes from Cluster1 to Kafka.

Visit Confluent's website to create a Kafka cluster
Configure the MongoDB Atlas Source connector with the following details:
Connection string for Cluster1
Topic name: demo.sample_salesforce.cdc_events
Enable change streams on the source collection
4. Set Up Stream Processor in MongoDB Atlas
Log in to your MongoDB Atlas account
From the left navigation menu, select "Stream Processing"
Click "Create New Instance"
Choose your preferred cloud provider and region (ideally in the same region as your clusters)
Select an appropriate size for your instance:
For this demo, an XS or S instance is sufficient
For production workloads, choose based on expected data volume and processing needs
Name your instance (e.g., "SalesforceStreamProcessor")
Create two connections:
salesforce_cdc: Connect to your Kafka cluster
Provide the Bootstrap server address
Configure authentication (SASL/SCRAM) with your Confluent credentials
demo_destination: Connect to your MongoDB Atlas Cluster2
Use the same connection string as in your CLUSTER2_URI environment variable
This Stream Processing instance will serve as the real-time data transformation engine between Kafka and your destination MongoDB cluster.

5. Configure the Stream Processor
After setting up the Stream Processing instance, open the command line interface and execute:

Copy and paste the contents of stream_processor_config.js
Run the command from create_sp.txt: sp.createStreamProcessor("salesforcedemo", spconfig)
Pipeline Explanation
The Stream Processor configuration defines a pipeline with these stages:

$source: Reads data from the Kafka topic demo.sample_salesforce.cdc_events via the "salesforce_cdc" connection

$lookup (Users): Enriches the CDC events with user information by joining with the users.info collection

$lookup (Accounts): Enriches the CDC events with account information

$project: Reshapes the document structure to match the desired output schema

$addFields: Converts string date fields to proper MongoDB Date objects

$merge: Writes the processed data to the destination collection

6. Generate Sample Salesforce Data
Run the following script to simulate Salesforce CDC events:

This script will:

Clear existing data in both source and destination collections
Generate 1000 Salesforce-like CDC events at a rate of 1 per second
Each event includes information about location objects similar to what would come from Salesforce
Data Flow and Transformation
The complete data flow is:

Sample Salesforce data is inserted into Cluster1
Kafka reads these changes via the Confluent MongoDB Atlas Source connector
The Stream Processor consumes the Kafka messages
The processor performs lookups, transformations, and enrichments
Processed data is written to Cluster2 in the desired format
This approach demonstrates the power of using MongoDB Atlas Stream Processing for real-time data integration and transformation, with minimal custom code and infrastructure management.

Sample Documents
Sample Salesforce CDC Event - Example of raw Salesforce CDC event
Desired MongoDB Document - Target schema after transformation