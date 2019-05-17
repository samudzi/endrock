from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json, datetime


# https://developers.google.com/analytics/devguides/reporting/core/dimsmets#mode=api&cats=user,traffic_sources,session,page_tracking
class GoogleAnalyticsAPI:
    def __init__(self) -> None:
        super().__init__()
        self.VIEW_ID = '146102650'
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        # self.KEY_FILE_LOCATION = '../client_secrets.json'
        self.KEY_FILE_LOCATION = 'client_secrets.json'

    def get_report(self, start_date, end_date, metrics, dimensions, next_token=None):
        analytics = self.__initialize_analytics_reporting()
        """Queries the Analytics Reporting API V4.
      
        Args:
          analytics: An authorized Analytics Reporting API V4 service object.
        Returns:
          The Analytics Reporting API V4 response.
        """


        reportRequest = {
            'viewId': self.VIEW_ID,
            'dateRanges': [{
                'startDate': start_date,
                'endDate': end_date
            }],
            'metrics': metrics,
            'dimensions': dimensions,
            "pageSize": "1000",
        }

        # https://developers.google.com/analytics/devguides/reporting/core/v4/basics#pagination
        # Taken from `nextPageToken` of a previous response.
        if next_token is not None:
            reportRequest["pageToken"] = next_token

        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    reportRequest
                    ]
            }
        ).execute()

    def __initialize_analytics_reporting(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.KEY_FILE_LOCATION, self.SCOPES)
        # print(str(credentials))
        # Build the service object.
        analytics = build('analyticsreporting', 'v4', credentials=credentials)

        return analytics

    def get_reports(self, report_type, start_date, end_date, metrics, dimensions, next_page_token=None):
        print(report_type)
        print("next_page_token: " + str(next_page_token))
        response = self.get_report(start_date, end_date, metrics, dimensions, next_page_token)

        response_list = list()

        next_page_token = self.__extract_next_page_token(response)
        if next_page_token is not None:
            response_list.append(response)
            response_list = response_list + self.get_reports(report_type, start_date, end_date, metrics, dimensions, next_page_token)
        else:
            response_list.append(response)
        # print(json.dumps(response, indent=4, sort_keys=False))
        print("------------------------------------------------------------------------------------------------------")
        return response_list

    def __extract_next_page_token(self, response):
        if "reports" in response:
            reports = response["reports"]
            if len(reports) > 0:
                report = reports[0]
                if "nextPageToken" in report:
                    return report["nextPageToken"]
        return None


if __name__ == '__main__':
    api = GoogleAnalyticsAPI()

    # api.invoke("Country Wise Report", [{'expression': 'ga:sessions'}, {'expression': 'ga:avgSessionDuration'}], [{'name': 'ga:country'}])
    #
    # invoke("Browser Wise Report", [{'expression': 'ga:sessions'}, {'expression': 'ga:avgSessionDuration'}], [{'name': 'ga:browser'}])
    #
    # invoke("Country-Browser Wise Report", [{'expression': 'ga:sessions'}, {'expression': 'ga:avgSessionDuration'}], [{'name': 'ga:country'}, {'name': 'ga:browser'}])
    #
    # invoke("User Type Wise Report",
    #        [{'expression': 'ga:users'}],
    #        [{'name': 'ga:userType'}]
    # )

    # invoke("Referer Site Wise Report",
    #        [{'expression': 'ga:users'}],
    #        [{'name': 'ga:fullReferrer'}]
    #        )

    # invoke("Source Redirection Wise Report",
    #        [{'expression': 'ga:users'}],
    #        [{'name': 'ga:source'}]
    #        )

    # invoke("Number of Website Views Report",
    #        [{'expression': 'ga:pageviews'}, {'expression': 'ga:uniquePageviews'}],
    #        [{'name': 'ga:hostname'}]
    #        )

    # invoke("Number of Page Path Views Report",
    #        [{'expression': 'ga:pageviews'}, {'expression': 'ga:uniquePageviews'},
    #         {'expression': 'ga:timeOnPage'}, {'expression': 'ga:avgTimeOnPage'}
    #         ],
    #        [{'name': 'ga:pagePath'}]
    #        # [{'name': 'ga:pageTitle'}]
    #        )


