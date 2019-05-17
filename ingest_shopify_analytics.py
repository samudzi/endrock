import json
from shopify.ShopifyAnalyticsAPI import ShopifyAnalyticsAPI
from s3.S3API import S3API
from util.AppUtil import *


def handler(event, context):
    api = ShopifyAnalyticsAPI()
    last_n_days = 1

    if "last_n_days" in event:
        last_n_days = event["last_n_days"]

    orders_count = api.get_last_n_days_orders_count(last_n_days)
    last_n_days_date = api.get_last_n_day_created_date(last_n_days)
    print("orders_count: " + str(orders_count))
    print("last_n_days_date: " + str(last_n_days_date))

    if os.environ["ENVIRONMENT"] == "LOCAL":
        orders_count = 50

    orders_json = api.get_last_n_days_orders(orders_count, last_n_days)
    # print(orders_json)

    s3_api = S3API()
    for order in orders_json:
        s3_api.upload_shopify_order(last_n_days_date, order["id"], json.dumps(order, indent=4, sort_keys=False))
        if os.environ["ENVIRONMENT"] == "LOCAL":
            break

    body = {
        "message": "Your function executed successfully!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print("Response: " + json.dumps(response))
    return response


if __name__ == '__main__':
    configure_running_from_local()
    handler('', '')
