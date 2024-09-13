import time
from argparse import ArgumentParser
from argparse import Namespace

from ValLib.captcha.web import WebServerSolver

from human_captcha_client import logger
from human_captcha_client.auth import TokenAuth
from human_captcha_client.task import post_captcha_solution
from human_captcha_client.task import request_captcha_task


def main_loop(args: Namespace):
    auth = TokenAuth(args.api_key)
    solver_server = WebServerSolver(address="127.0.0.1")
    while True:
        try:
            task = request_captcha_task(auth)
            if "detail" in task:
                time.sleep(5)
                continue

            logger.info(f"New task received!")
            token = solver_server.token(
                task["captcha_obj"]["rqdata"], task["captcha_obj"]["sitekey"]
            )
            logger.info(f"Token received.")
            post_captcha_solution(auth, task["id"], token)
            time.sleep(5)
        except Exception as e:
            logger.exception(f"Unhandled exception: {e}")
            break


def main():
    parser = ArgumentParser()
    parser.add_argument("api_key")
    args = parser.parse_args()

    main_loop(args)


if __name__ == "__main__":
    main()
