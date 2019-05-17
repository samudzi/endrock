import os, traceback


def configure_running_from_local():
    os.environ["ENVIRONMENT"] = "LOCAL"
    os.environ["S3_BUCKET"] = "asoba-analytics-dev"
    os.environ["GOOGLE_ANALYTICS_S3_BUCKET"] = "asoba-google-analytics-dev"
    os.environ["KLAVIYO_S3_BUCKET"] = "asoba-klaviyo-analytics-dev"
    os.environ["SHOPIFY_S3_BUCKET"] = "asoba-shopify-analytics-dev"


def key_exist(json_obj, key):
    return key in json_obj and json_obj[key] is not None


def extract_stacktrace(ex):
    return ''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__))
