import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
from azure.storage.blob import BlobServiceClient
import json
import os
from datetime import datetime, timedelta

def main(timer: func.TimerRequest) -> None:
    cosmos_endpoint = os.environ["COSMOS_ENDPOINT"]
    cosmos_key = os.environ["COSMOS_KEY"]
    blob_connection_string = os.environ["BLOB_CONNECTION_STRING"]
    
    # Initialize clients
    cosmos = cosmos_client.CosmosClient(cosmos_endpoint, cosmos_key)
    database = cosmos.get_database_client("BillingDB")
    records_container = database.get_container_client("BillingRecords")
    metadata_container = database.get_container_client("Metadata")
    blob_service = BlobServiceClient.from_connection_string(blob_connection_string)
    blob_container = blob_service.get_container_client("billing-archives")
    
    # Query records older than 90 days
    three_months_ago = (datetime.utcnow() - timedelta(days=90)).isoformat()
    query = f"SELECT * FROM c WHERE c.timestamp < '{three_months_ago}'"
    records = list(records_container.query_items(query, enable_cross_partition_query=True))
    
    for record in records:
        record_id = record["id"]
        # Upload to Blob Storage
        blob_name = f"archives/{record_id}.json"
        blob_client = blob_container.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(record), overwrite=True)
        
        # Create metadata entry
        metadata = {
            "id": record_id,
            "blob_path": blob_name,
            "archived_at": datetime.utcnow().isoformat(),
            "_ttl": 604800  # 7 days in seconds
        }
        metadata_container.upsert_item(metadata)
        
        # Set TTL for original record (delete after 7 days)
        record["_ttl"] = 604800
        records_container.upsert_item(record)