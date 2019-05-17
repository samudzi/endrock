import json, time, boto3
from s3.S3API import S3API
from klaviyo.KlaviyoAPI import KlaviyoAPI
from util.AppUtil import *


def handler(event, context):
    print("event: " + json.dumps(event))
    event_date = event["event_date"]
    metrics_id = event["metrics_id"]
    uuid = event["uuid"]

    s3_api = S3API()
    exists = s3_api.timeline_event_exists_in_klaviyo(event_date, metrics_id, uuid)
    print("exists: " + str(exists))
    time_remaining = context.get_remaining_time_in_millis() # millis
    while time_remaining > 10000:
        time.sleep(5) # seconds
        time_remaining = context.get_remaining_time_in_millis()
        print(time_remaining)

    print("Done!")


if __name__ == '__main__':
    configure_running_from_local()
    api = KlaviyoAPI()
    s3_api = S3API()
    next = "9867a500-4b10-11e9-8001-8760b8c20f9d"
    while True:
        api_response = api.get_complete_timeline(next)
        last_row = api_response["data"][len(api_response["data"]) - 1]
        next = api_response["next"]

        uuid = last_row["uuid"]
        metrics_id = last_row["statistic_id"]
        event_datetime = last_row["datetime"]
        event_date = str(event_datetime.split(" ")[0])

        exists = s3_api.timeline_event_exists_in_klaviyo(event_date, metrics_id, uuid)
        print("uuid: " + uuid + ", exists: " + str(exists))
        if not exists:
            print(">>>>>> uuid: " + uuid + ", exists: " + str(exists))
            break
