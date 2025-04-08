let spconfig = [
    {
        $source: {
          connectionName: "salesforce_cdc",
          topic : ["demo.sample_salesforce.cdc_events"]
        }
      },
    {
        $lookup: {
          from: {
            "connectionName": "demo_destination",
            "db": "users",
            "coll": "info"
          },
          localField: "fullDocument.value.CreatedById",
          foreignField: "Id",
          as: "createdByInfo"
        }
      },
      {
        $lookup: {
          from: {
            "connectionName": "demo_destination",
            "db": "accounts",
            "coll": "info"
          },
          localField: "fullDocument.value.Account__c",
          foreignField: "sfdcId", 
          as: "accountInfo"
        }
      },
    {
      $project: {
        _id: "$fullDocument.value.Id",
        createdBy: { $arrayElemAt: [ "$createdByInfo.Name", 0 ] },
        createdDate: "$fullDocument.value.CreatedDate",
        lastModifiedBy: "$fullDocument.value.LastModifiedById", // Consider another lookup for the name
        lastModifiedDate: "$fullDocument.value.LastModifiedDate",
        id: "$fullDocument.value.Id",
        customerAccountId: { $arrayElemAt: [ "$accountInfo.customerId", 0 ] }, // Adjust if needed
        locationType: "$fullDocument.value.LocationType",
        isFreightForwarder: "$fullDocument.value.IsMobile",
        isDefault: "$fullDocument.value.Is_Default__c",
        name: "$fullDocument.value.Name",
        phone: "$fullDocument.value.Phone__c",
        address: {
          city: "$fullDocument.value.Address__City__s",
          country: "$fullDocument.value.Address__CountryCode__s",
          latitude: "$fullDocument.value.Address__Latitude__s",
          longitude: "$fullDocument.value.Address__Longitude__s",
          postalCode: "$fullDocument.value.Address__PostalCode__s",
          state: "$fullDocument.value.Address__StateCode__s",
          street: "$fullDocument.value.Address__Street__s"
        }
      }
    },
    {
      $addFields: {
        createdDate: { $toDate: "$createdDate" },
        lastModifiedDate: { $toDate: "$lastModifiedDate" }
      }
    },
    {
        $merge: {
           into: {
              connectionName: "demo_destination",
              db: "salesforce",
              coll: "locationData"
           }
        }
     }
    // You can add a final $validation stage to verify data integrity and write to a dead letter queue if necessary
    ]