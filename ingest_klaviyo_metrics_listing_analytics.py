import json
from klaviyo.KlaviyoAPI import KlaviyoAPI
from s3.S3API import S3API
from util.AppUtil import *


def handler(event, context):
    api = KlaviyoAPI()
    s3_api = S3API()

    all_metrics_listing = api.get_metrics()
    print("all_metrics_listing Count: " + str(len(all_metrics_listing)))
    print("all_metrics_listing: " + str(all_metrics_listing))

    for metrics in all_metrics_listing:
        s3_api.upload_klaviyo_metric_listing(metrics["id"], json.dumps(metrics, indent=4, sort_keys=False))
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
