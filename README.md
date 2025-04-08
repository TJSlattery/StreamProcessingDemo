Here’s a clean, well-formatted `README.md` version of your content, complete with headers, sub-bullets, and emojis. You can copy and paste this directly into a file:

---

# ⚡ Salesforce Data Integration with MongoDB Atlas and Kafka

This project demonstrates how to use **MongoDB Atlas Stream Processing** to transform and enrich **Salesforce CDC (Change Data Capture)** events in real-time. The data flow includes **Kafka** as a message broker, with both source and destination data stored in **MongoDB Atlas** clusters.

---

## Setup Overview

1. Create a **source MongoDB Atlas cluster** (`Cluster1`)
2. Create a **destination MongoDB Atlas cluster** (`Cluster2`) and populate it with user and account data
3. Connect **Kafka** to the source cluster using the **Confluent MongoDB Atlas Source connector**
4. Configure **Stream Processing** in MongoDB Atlas
5. Run a **sample data generator** to simulate Salesforce CDC events

---

## ✅ Prerequisites

Before you begin, ensure the following are installed/configured:

- **Python 3.6+** with the following packages:
  - `pymongo` – MongoDB connectivity
  - `faker` – Generate sample data
  - `random`, `datetime`, `time`, `os` – Standard Python libraries
- **MongoDB Atlas Account** – Free tier (M0) is sufficient
- **Confluent Cloud Account** – For Kafka cluster and connectors
- **Environment Variables**:
  - `CLUSTER2_URI` – MongoDB connection string for **destination** cluster
  - `CLUSTER1_URI` – MongoDB connection string for **source** cluster

💡 Install required Python packages using:
```bash
pip install pymongo faker
```

---

## 🛠️ Detailed Instructions

### 1️⃣ Create Source MongoDB Atlas Cluster (`Cluster1`)

- Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Click **"Build a Database"**
- Select your preferred cloud provider
- Choose **"M0 Free Tier"** for testing
- Name the cluster **"Cluster1"**
- Create a **database user** with read/write privileges
- Configure **network access** (whitelist your IP)
- **Note** the connection string – you'll use it later

> This cluster will emulate the source of Salesforce CDC events.

---

### 2️⃣ Create Destination MongoDB Atlas Cluster (`Cluster2`) & Populate Reference Data

- Follow the same steps as above to create a second cluster
- Name it **"Cluster2"**
- Create a database user and set up network access
- Export the connection string as an environment variable: `CLUSTER2_URI`

📦 Now, populate the reference data by running the provided scripts.

#### These scripts will:
- Create **1000 random user documents** in `users.info`:
  - Unique ID (e.g. `"0001"`, `"0002"`)
  - Random name, email, age, city, registration date
- Create **1000 random account documents** in `accounts.info`:
  - Salesforce ID (`"A0001"`, `"A0002"`)
  - Customer ID (`"C0001"`, `"C0002"`)
  - Random contact and location details

---

### 3️⃣ Connect Kafka to Source MongoDB Atlas Cluster

- Set up a **Confluent MongoDB Atlas Source connector**:
  - Visit [Confluent Cloud](https://www.confluent.io/)
  - Create a Kafka cluster
  - Configure the connector with:
    - Cluster1 connection string
    - Topic: `demo.sample_salesforce.cdc_events`
    - Enable change streams on source collections

---

### 4️⃣ Set Up Stream Processor in MongoDB Atlas

- Log in to your **MongoDB Atlas** account
- From the left menu, choose **"Stream Processing"**
- Click **"Create New Instance"**
- Select:
  - Preferred cloud provider & region
  - Size (XS or S is fine for demo)
  - Name (e.g., `SalesforceStreamProcessor`)

#### Create 2 connections:
- `salesforce_cdc`: Kafka cluster
  - Provide **Bootstrap server address**
  - Configure **SASL/SCRAM** authentication
- `demo_destination`: MongoDB Cluster2
  - Use your `CLUSTER2_URI` connection string

> This Stream Processing instance acts as the **real-time transformation engine**.

---

### 5️⃣ Configure the Stream Processor

- Open the Stream Processor CLI
- Copy & paste contents of `stream_processor_config.js`
- Then run:
```js
sp.createStreamProcessor("salesforcedemo", spconfig)
```

---

## 🔁 Pipeline Explanation

The Stream Processor configuration defines a pipeline with these stages:

- **`$source`** – Reads from Kafka topic `demo.sample_salesforce.cdc_events`
- **`$lookup (Users)`** – Joins with `users.info` for user enrichment
- **`$lookup (Accounts)`** – Joins with `accounts.info` for account enrichment
- **`$project`** – Reshapes data structure
- **`$addFields`** – Converts string dates into MongoDB `Date` objects
- **`$merge`** – Writes enriched data into destination collection

---

## 🧪 Generate Sample Salesforce Data

Run the provided **data simulation script**.

This will:
- 🔄 Clear existing source and destination data
- 🚀 Generate **1000 CDC-like events**, 1 per second
- 🗺️ Each event includes **location info**, emulating Salesforce CDC output

---

## 🔄 Data Flow and Transformation

Here's how the end-to-end flow works:

1. 📝 Sample Salesforce data is inserted into `Cluster1`
2. 📡 Kafka reads changes via the **Confluent MongoDB Atlas Source connector**
3. 🧠 Stream Processor consumes Kafka messages
4. 🔍 Processor performs **lookups, transformations, enrichments**
5. 📦 Final output is written to `Cluster2`

> This showcases the power of **MongoDB Atlas Stream Processing** for **real-time, low-code data integration**.

---

## 📄 Sample Documents

- **Salesforce CDC Event** – Raw event format
- **Transformed MongoDB Document** – Enriched and reshaped output

---

Let me know if you'd like this turned into a downloadable file, or want code snippets embedded in the doc as well.