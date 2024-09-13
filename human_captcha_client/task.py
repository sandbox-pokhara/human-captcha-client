from urllib.parse import urljoin

import httpx

from human_captcha_client.auth import TokenAuth
from human_captcha_client.constants import API_URL


def request_captcha_task(auth: TokenAuth):
    url = urljoin(API_URL, "api/captcha-tasks/request/?type=token")
    res = httpx.get(url, auth=auth, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()


def post_captcha_solution(auth: TokenAuth, task_id: int, solution: str):
    url = urljoin(API_URL, f"/api/captcha-tasks/{task_id}/submit-solution/")
    data = {"solution": solution}
    res = httpx.post(url, auth=auth, json=data, verify=False, timeout=30)
    res.raise_for_status()
    return res.json()
