import requests, json, os


class KlaviyoAPI:
    def __init__(self) -> None:
        super().__init__()
        self.__API_KEY = "pk_5dc8270a33e6157bac5424891fb16c2abd"
        self.__PAGE_LIMIT = 100 # Defaults to 50. The maximum number is 100.

    # https://www.klaviyo.com/docs/api/metrics
    def get_metrics(self, page_number=0):
        url = "https://a.klaviyo.com/api/v1/metrics"

        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        all_metrics = list()
        while True:
            querystring = {
                "api_key": self.__API_KEY,
                "page": page_number,
                "count": self.__PAGE_LIMIT
            }

            print(querystring)

            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

            api_response = json.loads(response.text)
            delta_metrics = api_response["data"]

            all_metrics = all_metrics + delta_metrics
            print("len(all_metrics): " + str(len(all_metrics)) + ", total: " + str(api_response["total"]))

            if len(all_metrics) == api_response["total"]:
                return all_metrics
            else:
                page_number = page_number + 1

        return None

    def get_complete_timeline(self, next=None):
        url = "https://a.klaviyo.com/api/v1/metrics/timeline"

        querystring = {
            "api_key": self.__API_KEY,
            "sort": "desc",
            "count": self.__PAGE_LIMIT # defaults to 100
        }

        if os.environ["ENVIRONMENT"] == "LOCAL":
            querystring["count"] = 10

        if next is not None:
            querystring["since"] = next

        payload = ""
        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        api_response = json.loads(response.text)
        return api_response
