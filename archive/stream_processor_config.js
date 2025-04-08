let a = {
    $source: {
      connectionName: "salesforce_cdc",
      topic : ["sample_salesforce_cdc.sample_salesforce.cdc_events"]
    }
  }

 let c = {
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
  }
  
let d ={
    $lookup: {
      from: {
        "connectionName": "demo_destination",
        "db": "accounts",
        "coll": "info"
      },
      localField: "fullDocument.value.Account__c",
      foreignField: "AccountId", 
      as: "accountInfo"
    }
  }

let e = {
    $project: {
      _id: "$value.Id",
      createdByInfo: { $arrayElemAt: [ "$createdByInfo", 0 ] }, // Get the first element
      createdDate: "$value.CreatedDate",
      lastModifiedBy: "$value.LastModifiedById",
      lastModifiedDate: "$value.LastModifiedDate",
      id: "$value.Id",
      accountInfo: { $arrayElemAt: [ "$accountInfo", 0 ] },     // Get the first element
      locationType: "$value.LocationType",
      isFreightForwarder: "$value.IsMobile",
      isDefault: "$value.Is_Default__c",
      name: "$value.Name",
      phone: "$value.Phone__c",
      address: {
        city: "$value.Address__City__s",
        country: "$value.Address__CountryCode__s",
        latitude: "$value.Address__Latitude__s",
        longitude: "$value.Address__Longitude__s",
        postalCode: "$value.Address__PostalCode__s",
        state: "$value.Address__StateCode__s",
        street: "$value.Address__Street__s"
      }
    }
  }
  
  let f ={
    $addFields: {
      createdDate: {
        $toDate: "$createdDate"
      },
      lastModifiedDate: {
        $toDate: "$lastModifiedDate"
      }
    }
  }

  let g = {
    $project: {
        "value": 0,
        "timestamp": 0,
        "timestampType": 0,
        "partition": 0,
        "offset": 0,
        "key": 0,
        "headers": 0
      }
  }

let h = {
    $merge: {
       into: {
          connectionName: "demo_destination",
          db: "salesforce",
          coll: "locationData"
       }
    }
 }