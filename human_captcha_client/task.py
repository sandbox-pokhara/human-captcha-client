from urllib.parse import urljoin

import httpx

from human_captcha_client import logger
from human_captcha_client.auth import TokenAuth


def request_captcha_task(url: str, auth: TokenAuth):
    logger.info("Requesting new captcha task...")
    url = urljoin(url, "/api/captcha-tasks/request/?type=token")
    res = httpx.get(url, auth=auth, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()


def post_captcha_solution(
    url: str, auth: TokenAuth, task_id: int, solution: str
):
    url = urljoin(url, f"/api/captcha-tasks/{task_id}/submit-solution/")
    data = {"solution": solution}
    res = httpx.post(url, auth=auth, json=data, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()
