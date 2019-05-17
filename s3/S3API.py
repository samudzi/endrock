import boto3, tempfile, os
from util.AppUtil import *


class S3API:
    def __init__(self) -> None:
        super().__init__()
        self.__BUCKET_NAME = os.environ["S3_BUCKET"]
        self.__GOOGLE_ANALYTICS_S3_BUCKET = os.environ["GOOGLE_ANALYTICS_S3_BUCKET"]
        self.__KLAVIYO_S3_BUCKET = os.environ["KLAVIYO_S3_BUCKET"]
        self.__SHOPIFY_S3_BUCKET = os.environ["SHOPIFY_S3_BUCKET"]

    def upload_ga_country_wise_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "country-wise/" + str(report_date) + ".json", content)

    def upload_ga_browser_wise_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "browser-wise/" + str(report_date) + ".json", content)

    def upload_ga_user_type_wise_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "user-type-wise/" + str(report_date) + ".json", content)

    def upload_ga_website_page_views_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "website-page-views/" + str(report_date) + ".json", content)

    def upload_ga_referer_site_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "full-referer-sites/" + str(report_date) + ".json", content)

    def upload_ga_source_referrals_site_report(self, report_date, content):
        self.__upload(self.__GOOGLE_ANALYTICS_S3_BUCKET, "source-referrals-sites/" + str(report_date) + ".json", content)

    def upload_shopify_order(self, last_n_days_date, order_id, content):
        self.__upload(self.__SHOPIFY_S3_BUCKET, "orders/" + last_n_days_date + "/" + str(order_id) + ".json", content)

    def upload_klaviyo_metric_listing(self, metrics_id, content):
        self.__upload(self.__KLAVIYO_S3_BUCKET, "metrics-listing/" + str(metrics_id) + ".json", content)

    def upload_klaviyo_event_timeline(self, event_date, metrics_id, uuid, content):
        if os.environ["ENVIRONMENT"] == "LOCAL":
            print("ignore - " + self.get_klaviyo_timeline_key(event_date, metrics_id, uuid))
            return None
        self.__upload(self.__KLAVIYO_S3_BUCKET, self.get_klaviyo_timeline_key(event_date, metrics_id, uuid), content)

    def __upload(self, bucket, key, content):
        new_file, filename = tempfile.mkstemp()
        os.write(new_file, str(content).encode())
        os.close(new_file)
        # print("Key: " + key)
        self.__get_s3_client().upload_file(filename, bucket, key)

        if os.path.exists(filename):
            os.remove(filename)

    def timeline_event_exists_in_klaviyo(self, event_date, metrics_id, uuid):
        return self.key_exists(self.__KLAVIYO_S3_BUCKET, self.get_klaviyo_timeline_key(event_date, metrics_id, uuid))

    def key_exists(self, bucket, key):
        try:
            self.__get_s3_client().head_object(Bucket=bucket, Key=key)
            return True
        except Exception as ex:
            # Not found
            # print("ERROR: " + str(ex))
            return False

    def __get_s3_client(self):
        if os.environ["ENVIRONMENT"] == "LOCAL":
            boto3.setup_default_session(profile_name='asoba')

        s3 = boto3.client('s3')
        return s3

    def get_klaviyo_timeline_key(self, event_date, metrics_id, uuid):
        return "timeline/" + str(event_date) + "/" + str(metrics_id) + "/" + str(uuid) + ".json"
