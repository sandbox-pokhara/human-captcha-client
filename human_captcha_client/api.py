from urllib.parse import urljoin

import httpx

from human_captcha_client import logger
from human_captcha_client.auth import TokenAuth


def retrieve_settings(url: str, auth: TokenAuth):
    logger.info("Retrieving settings...")
    url = urljoin(url, "/api/settings/")
    res = httpx.get(url, auth=auth, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()


def request_captcha_task(url: str, auth: TokenAuth):
    logger.info("Requesting new captcha task...")
    url = urljoin(url, "/api/captcha-tasks/request/")
    res = httpx.get(url, auth=auth, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()


def post_captcha_solution(
    url: str, auth: TokenAuth, task_id: int, solution: str | list[int]
):
    logger.info("Posting solution...")
    url = urljoin(url, f"/api/captcha-tasks/{task_id}/submit-solution/")
    data = {"solution": solution}
    res = httpx.post(url, auth=auth, json=data, verify=False, timeout=30)
    res.raise_for_status()
    logger.info("Success.")
    return res.json()


def skip_captcha(url: str, auth: TokenAuth, task_id: int):
    logger.info("Skipping captcha...")
    url = urljoin(url, f"/api/captcha-tasks/{task_id}/skip/")
    res = httpx.patch(url, auth=auth, verify=False, timeout=30)
    res.raise_for_status()
    logger.info("Success.")
    return res.json()
