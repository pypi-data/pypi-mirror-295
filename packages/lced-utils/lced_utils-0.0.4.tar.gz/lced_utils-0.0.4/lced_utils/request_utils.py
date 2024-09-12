import logging

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


def log_before_retry(retry_state):
    if retry_state.attempt_number > 1:
        logging.warning(
            f"Retrying... Attempt number {retry_state.attempt_number - 1} "
            f"of {retry_state.retry_object.stop.max_attempt_number - 1} "
            f"for function '{retry_state.fn.__name__}'"
        )


def log_before_sleep(retry_state):
    wait_time = retry_state.next_action.sleep
    logging.info(f"Waiting {wait_time:.2f} seconds before next retry")


@retry(
    stop=stop_after_attempt(11),
    wait=wait_fixed(5),
    before=log_before_retry,
    before_sleep=log_before_sleep,
    reraise=True,
)
def base_requests_post(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("json") or kwargs.get("data")
    timeout = kwargs.get("timeout")
    logging.info(
        f"LiCloud Sending info include <method:POST, url:{url}, params:{params}, timeout:{timeout}>"
    )
    res = requests.post(**kwargs)
    res_json = res.json()
    code = res_json.get("code")
    msg = res_json.get("msg")
    logging.info(f"LiCloud Receiving info include <code:{code}, msg:{msg}>")
    return res_json


@retry(
    stop=stop_after_attempt(11),
    wait=wait_fixed(5),
    before=log_before_retry,
    before_sleep=log_before_sleep,
    reraise=True,
)
def base_requests_get(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")
    timeout = kwargs.get("timeout")
    logging.info(
        f"LiCloud Sending info include <method:GET, url:{url}, params:{params}, timeout:{timeout}>"
    )
    res = requests.get(**kwargs)
    res_json = res.json()
    code = res_json.get("code")
    msg = res_json.get("msg")
    logging.info(f"LiCloud Receiving info include <code:{code}, msg:{msg}>")
    return res_json
