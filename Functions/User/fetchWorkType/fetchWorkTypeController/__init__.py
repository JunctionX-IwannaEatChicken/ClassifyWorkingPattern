import logging

import azure.functions as func
import json
from azure.cosmos import CosmosClient, exceptions, PartitionKey


def main(req: func.HttpRequest) -> func.HttpResponse:
    URL = "https://junctionx.documents.azure.com:443/"
    KEY = "BCw9nhNiTSl9ndUokCw6uHhzZSDgsSGoMjPUa0Ech6E9yiuGKCrsswFIXRatcguQYcNLnYdhFPWPhuaRtLfoxg=="
    DATABASE_NAME = "MitoSoftCorp"
    CONTAINER_NAME = "workType"
    client = CosmosClient(URL, credential=KEY)

    work_type = req.params.get("work_type")

    try:
        database = client.create_database(DATABASE_NAME)
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(DATABASE_NAME)

    try:
        container = database.create_container(id=CONTAINER_NAME,
            partition_key=PartitionKey(path="/name"))
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(CONTAINER_NAME)

    user_list = []
    for item in container.query_items(query='SELECT * FROM {} w WHERE w.work_type = "{}"'
    .format(CONTAINER_NAME, work_type), enable_cross_partition_query=True):
        user_list.append(item.get("user_id"))

    return_data = dict(
        id=user_list
    )

    return func.HttpResponse(json.dumps(return_data),
        headers={"Content-Type": "application/json"}, status_code=200)
