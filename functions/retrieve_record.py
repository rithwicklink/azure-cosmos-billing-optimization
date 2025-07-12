import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
from azure.storage.blob import BlobServiceClient
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.route_params.get("id")
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
    
    # Check if record exists in Cosmos DB
    try:
        record = records_container.read_item(item=record_id, partition_key=record_id)
        return func.HttpResponse(json.dumps(record), status_code=200)
    except:
        pass
    
    # Check metadata for archived record
    query = f"SELECT * FROM c WHERE c.id = '{record_id}'"
    metadata_items = list(metadata_container.query_items(query, enable_cross_partition_query=True))
    if not metadata_items:
        return func.HttpResponse("Record not found", status_code=404)
    
    # Retrieve from Blob Storage
    metadata = metadata_items[0]
    blob_client = blob_container.get_blob_client(metadata["blob_path"])
    blob_data = blob_client.download_blob().readall()
    record = json.loads(blob_data)
    
    # Cache in Cosmos DB with TTL
    record["_ttl"] = 604800  # 7 days
    records_container.upsert_item(record)
    
    return func.HttpResponse(json.dumps(record), status_code=200)