import requests, json, datetime


class ShopifyAnalyticsAPI:
    def __init__(self) -> None:
        super().__init__()
        self.__API_KEY = "974c2a468dcd79a926dcd0ddd2976d3c"
        self.__API_SECRET = "e9eba5598b0062ca6967510b012f7ccc"
        self.__PAGE_LIMIT = 250

    def get_last_n_days_orders(self, orders_count, last_n_days=1):
        last_n_days_date = self.get_last_n_day_created_date(last_n_days)
        return self.get_orders(
            last_n_days_date + "T%00:%00:%00+00:00",
            last_n_days_date + "T%23:%59:%59+00:00",
            orders_count
        )

    def get_last_n_days_orders_count(self, last_n_days=1):
        last_n_days_date = self.get_last_n_day_created_date(last_n_days)
        return self.get_orders_count(
            last_n_days_date + "T%00:%00:%00+00:00",
            last_n_days_date + "T%23:%59:%59+00:00"
        )

    def get_last_n_day_created_date(self, last_n_days):
        last_n_day_utc_time = datetime.datetime.utcnow() - datetime.timedelta(days=last_n_days)
        last_n_day_created_date = last_n_day_utc_time.strftime("%Y-%m-%d")
        return last_n_day_created_date

    def get_orders_count(self, created_at_min, created_at_max):
        url = "https://" + self.__API_KEY + ":" + self.__API_SECRET + "@priverevaux.myshopify.com/admin/orders/count.json"

        querystring = {
            "created_at_min": created_at_min,
            "created_at_max": created_at_max
        }

        payload = ""
        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            return json.loads(response.text)["count"]

        raise Exception(response)

    def get_orders(self, created_at_min, created_at_max, orders_count):
        url = "https://" + self.__API_KEY + ":" + self.__API_SECRET + "@priverevaux.myshopify.com/admin/orders.json"

        querystring = {
            "created_at_min": created_at_min,
            "created_at_max": created_at_max,
            "limit": self.__PAGE_LIMIT,
            "order": "created_at asc"
        }

        payload = ""
        headers = {
            'cache-control': "no-cache"
        }

        print("querystring: " + str(querystring))

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            return self.__fetch_all_orders(json.loads(response.text)["orders"], created_at_max, orders_count)

        raise Exception(response)

    def __fetch_all_orders(self, partial_orders, created_at_max, orders_count):
        print("Merged Orders Length: " + str(len(partial_orders)))
        if len(partial_orders) >= orders_count:
            return partial_orders

        max_order_id = None
        for order in partial_orders:
            if max_order_id is None or max_order_id < order["id"]:
                max_order_id = order["id"]

        delta_partial_orders = self.get_orders_since_id(max_order_id, created_at_max)
        print("Delta Length: " + str(len(delta_partial_orders)))
        return self.__fetch_all_orders(partial_orders + delta_partial_orders, created_at_max, orders_count)

    def get_orders_since_id(self, since_id, created_at_max):
        url = "https://" + self.__API_KEY + ":" + self.__API_SECRET + "@priverevaux.myshopify.com/admin/orders.json"

        querystring = {
            "since_id": since_id,
            "created_at_max": created_at_max,
            "limit": self.__PAGE_LIMIT,
            "order": "created_at asc"
        }

        payload = ""
        headers = {
            'cache-control': "no-cache"
        }

        print("querystring: " + str(querystring))

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            return json.loads(response.text)["orders"]

        raise Exception(response)


if __name__ == '__main__':
    api = ShopifyAnalyticsAPI()
    response_json = api.get_last_n_days_orders(50, 1)
    print(response_json)

    # "2019-03-21T10:12:33-04:00"
    # last_n_days = 1
    # current_utc_time = datetime.datetime.utcnow() - datetime.timedelta(days=last_n_days)
    # created_at_min = current_utc_time.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    # print(created_at_min)
