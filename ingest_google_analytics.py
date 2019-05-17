import json, datetime
from google_analytics.GoogleAnalyticsAPI import GoogleAnalyticsAPI
from s3.S3API import S3API
from util.AppUtil import *


def handler(event, context):
    s3_api = S3API()

    todays_date = datetime.datetime.utcnow()
    # end_date = todays_date.strftime("%Y-%m-%d")
    # print(end_date)

    start_date = todays_date - datetime.timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    # print(start_date)

    # Fetch yesterday's reports
    country_wise_report = get_country_wise_report(start_date, start_date)
    s3_api.upload_ga_country_wise_report(start_date, json.dumps(country_wise_report, indent=4, sort_keys=False))

    browser_wise_report = get_browser_wise_report(start_date, start_date)
    s3_api.upload_ga_browser_wise_report(start_date, json.dumps(browser_wise_report, indent=4, sort_keys=False))

    user_type_wise_report = get_user_type_wise_report(start_date, start_date)
    s3_api.upload_ga_user_type_wise_report(start_date, json.dumps(user_type_wise_report, indent=4, sort_keys=False))

    website_page_views_report = get_website_page_views_report(start_date, start_date)
    s3_api.upload_ga_website_page_views_report(start_date, json.dumps(website_page_views_report, indent=4, sort_keys=False))

    referer_site_report = get_referer_site_report(start_date, start_date)
    s3_api.upload_ga_referer_site_report(start_date, json.dumps(referer_site_report, indent=4, sort_keys=False))

    source_referrals_report = get_source_referrals_report(start_date, start_date)
    s3_api.upload_ga_source_referrals_site_report(start_date, json.dumps(source_referrals_report, indent=4, sort_keys=False))

    body = {
        "message": "Your function executed successfully!"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    print("Response: " + json.dumps(response))
    return response


def get_source_referrals_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "Source Redirection Wise Report",
        start_date, end_date,
        [{'expression': 'ga:users'}],
        [{'name': 'ga:source'}]
    )

    custom_report_list = list()
    for api_response in api_response_list:
        reports = api_response["reports"]
        for report in reports:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                users_metrics = metrics_values[0]

                custom_report = {
                    dimension: {
                        "ga:users": users_metrics,
                    }
                }
                custom_report_list.append(custom_report)

    print(custom_report_list)
    return custom_report_list


def get_referer_site_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "Referer Site Wise Report",
        start_date, end_date,
        [{'expression': 'ga:users'}],
        [{'name': 'ga:fullReferrer'}]
    )

    custom_report_list = list()
    for api_response in api_response_list:
        reports = api_response["reports"]
        for report in reports:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                users_metrics = metrics_values[0]

                custom_report = {
                    dimension: {
                        "ga:users": users_metrics,
                    }
                }
                custom_report_list.append(custom_report)

    print(custom_report_list)
    return custom_report_list


def get_website_page_views_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "Number of Website Page Views Report",
        start_date, end_date,
        [{'expression': 'ga:pageviews'}, {'expression': 'ga:uniquePageviews'}, {'expression': 'ga:timeOnPage'}, {'expression': 'ga:avgTimeOnPage'}],
        [{'name': 'ga:pagePath'}]
    )

    custom_report_list = list()
    for api_response in api_response_list:
        reports = api_response["reports"]
        for report in reports:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                page_views_metrics = metrics_values[0]
                unique_page_views_metrics = metrics_values[1]
                time_on_page_metrics = metrics_values[2]
                avg_time_on_page_metrics = metrics_values[3]

                custom_report = {
                    dimension: {
                        "ga:pageviews": page_views_metrics,
                        "ga:uniquePageviews": unique_page_views_metrics,
                        "ga:timeOnPage": time_on_page_metrics,
                        "ga:avgTimeOnPage": avg_time_on_page_metrics,

                    }
                }
                custom_report_list.append(custom_report)

    print(custom_report_list)
    return custom_report_list


def get_user_type_wise_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "User Type Wise Report",
        start_date, end_date,
        [{'expression': 'ga:users'}],
        [{'name': 'ga:userType'}]
    )
    custom_report_list = list()
    for api_response in api_response_list:
        reports = api_response["reports"]
        for report in reports:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                user_type_metrics = metrics_values[0]

                custom_report = {
                    dimension: {
                        "ga:userType": user_type_metrics
                    }
                }
                custom_report_list.append(custom_report)

    print(custom_report_list)
    return custom_report_list


def get_browser_wise_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "Browser Wise Report",
        start_date, end_date,
        [{'expression': 'ga:sessions'}, {'expression': 'ga:avgSessionDuration'}],
        [{'name': 'ga:browser'}]
    )
    custom_report_list = list()
    for api_response in api_response_list:
        reports = api_response["reports"]
        for report in reports:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                session_metrics = metrics_values[0]
                avg_session_duration_metrics = metrics_values[1]

                custom_report = {
                    dimension: {
                        "ga:sessions": session_metrics,
                        "ga:avgSessionDuration": avg_session_duration_metrics
                    }
                }
                custom_report_list.append(custom_report)

    print(custom_report_list)
    return custom_report_list


def get_country_wise_report(start_date, end_date):
    api = GoogleAnalyticsAPI()
    api_response_list = api.get_reports(
        "Country Wise Report",
        start_date, end_date,
        [{'expression': 'ga:sessions'}, {'expression': 'ga:avgSessionDuration'}],
        [{'name': 'ga:country'}])

    custom_report_list = list()
    for api_response in api_response_list:
        country_wise_report = api_response["reports"]
        for report in country_wise_report:
            data = report["data"]
            rows = data["rows"]
            for row in rows:
                dimension = row["dimensions"][0]

                metrics_values = row["metrics"][0]["values"]
                session_metrics = metrics_values[0]
                avg_session_duration_metrics = metrics_values[1]

                custom_report = {
                    dimension: {
                        "ga:sessions": session_metrics,
                        "ga:avgSessionDuration": avg_session_duration_metrics
                    }
                }
                custom_report_list.append(custom_report)
    return custom_report_list


if __name__ == '__main__':
    configure_running_from_local()
    handler('', '')
