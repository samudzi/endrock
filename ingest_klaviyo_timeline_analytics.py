import json, boto3, threading
from klaviyo.KlaviyoAPI import KlaviyoAPI
from s3.S3API import S3API
from util.AppUtil import *
import datetime


def handler(event, context):
    api_response = None
    last_uuid = None
    event_date = None
    metrics_id = None
    uuid = None

    minimum_datetime_object = datetime.datetime.strptime('2019-03-15', '%Y-%m-%d')

    try:
        print("event: " + json.dumps(event))

        if key_exist(event, "last_uuid"):
            last_uuid = event["last_uuid"]

        if key_exist(event, "last_processed_date"):
            event_date = event["last_processed_date"]

        api = KlaviyoAPI()
        s3_api = S3API()
        subsequent_events_processed = True
        trigger_nested_lambda = False

        while subsequent_events_processed:
            thread_list = list()
            print("last_uuid: " + str(last_uuid) + ", event_date: " + str(event_date))
            api_response = api.get_complete_timeline(last_uuid)

            if not key_exist(api_response, "data"):
                print("No data element present in response")
                subsequent_events_processed = False
            elif len(api_response["data"]) == 0:
                print("Empty data element present in response")
                subsequent_events_processed = False
            else:
                for row in api_response["data"]:
                    uuid = row["uuid"]
                    metrics_id = row["statistic_id"]
                    event_datetime = row["datetime"]
                    event_date = str(event_datetime.split(" ")[0])
                    event_datetime_object = datetime.datetime.strptime(event_date, '%Y-%m-%d')

                    if event_datetime_object < minimum_datetime_object:
                        print("WARN: STOPPING PROCESS TO LOAD PREVIOUS YEAR DATA")
                        subsequent_events_processed = False
                        break
                    elif not s3_api.timeline_event_exists_in_klaviyo(event_date, metrics_id, uuid):
                        t1 = threading.Thread(target=s3_api.upload_klaviyo_event_timeline, args=(event_date, metrics_id, uuid, json.dumps(row, indent=4, sort_keys=False),))
                        t1.start()
                        thread_list.append(t1)
                    else:
                        print("WARN: " + s3_api.get_klaviyo_timeline_key(event_date, metrics_id, uuid) + " Key Already exists!")
                        subsequent_events_processed = False
                        break
                if key_exist(api_response, "next"):
                   last_uuid = api_response["next"]

            if os.environ["ENVIRONMENT"] != "LOCAL":
                time_remaining = context.get_remaining_time_in_millis()
                if time_remaining < 40000:
                    trigger_nested_lambda = True
                    break

            print("Thread List: " + str(len(thread_list)))
            for t in thread_list:
                t.join()

        if trigger_nested_lambda and key_exist(api_response, "next"):
            print("INFO: Lambda function triggered for last_uuid: " + str(last_uuid) + ", event_date: " + str(event_date))
            trigger_lambda_event(api_response["next"], event_date)

        body = {
            "message": "Your function executed successfully!"
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        print("Response: " + json.dumps(response))
        return response
    except Exception as ex:
        exception_occurred_during_uuids = list()
        if api_response is not None:
            for row in api_response["data"]:
                exception_occurred_during_uuids.append(row["uuid"])

        body = {
            "message": extract_stacktrace(ex),
            "exception_occurred_during_uuids": exception_occurred_during_uuids,
            "input_last_uuid": last_uuid,
            "exception_in_uuid": uuid,
            "exception_in_event_date": event_date,
            "exception_in_metrics_id": metrics_id

        }

        response = {
            "statusCode": 500,
            "body": json.dumps(body)
        }

        print("Response: " + json.dumps(response))
        return response


def trigger_lambda_event(last_uuid, last_processed_date):
    input = {
        "last_uuid": last_uuid,
        "last_processed_date": last_processed_date
    }

    # lambda_client = boto3.client('lambda', region_name='us-west-2')
    lambda_client = boto3.client('lambda')

    try:
        #invoking lambda with payload
        fn_name = 'analytics-ingest-' + os.environ["ENVIRONMENT"] + '-ingest-klaviyo-timeline-analytics'
        resp = lambda_client.invoke(FunctionName=fn_name, InvocationType='Event', Payload=json.dumps(input))
    except Exception as ex:
        print(ex)

    return True


if __name__ == '__main__':
    configure_running_from_local()
    # handler('', '')

    event_datetime = "2019-03-27 07:47:08+00:00"
    event_date = str(event_datetime.split(" ")[0])
    print(event_date)
    datetime_object = datetime.datetime.strptime('2018-10-14', '%Y-%m-%d')
    print(datetime_object)

    minimum_date = datetime.datetime.strptime('2018-10-15', '%Y-%m-%d')
    print(minimum_date)
    if datetime_object < minimum_date:
        print("True")
    else:
        print("False")
