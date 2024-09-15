import time
from argparse import ArgumentParser
from argparse import Namespace

from human_captcha_client import __version__
from human_captcha_client import logger
from human_captcha_client.api import post_captcha_solution
from human_captcha_client.api import request_captcha_task
from human_captcha_client.api import retrieve_settings
from human_captcha_client.auth import TokenAuth


def version_to_tuple(v: str):
    return tuple([int(i) for i in v.split(".")])


def main_loop(args: Namespace):
    auth = TokenAuth(args.token)

    settings = retrieve_settings(args.url, auth)

    if version_to_tuple(__version__) < version_to_tuple(
        settings["minimum_client_version"]
    ):
        logger.error(
            f"Your version ({__version__}) is out of date. "
            f'Please upgrade to {settings["minimum_client_version"]} '
            'using the command "pip install -U human-captcha-client"'
        )
        return

    # Importing here because the package slows down when script is closed
    # TODO: code a custom web solver
    from ValLib.captcha.web import WebServerSolver  # type:ignore

    solver_server = WebServerSolver(address="127.0.0.1")

    while True:
        try:
            task = request_captcha_task(args.url, auth)
            if "detail" in task:
                time.sleep(5)
                continue

            logger.info(f"New task received!")
            token = solver_server.token(
                task["captcha_obj"]["rqdata"], task["captcha_obj"]["sitekey"]
            )
            logger.info(f"Token received.")
            post_captcha_solution(args.url, auth, task["id"], token)
            time.sleep(5)
        except Exception as e:
            logger.exception(f"Unhandled exception: {e}")
            break


def main():
    parser = ArgumentParser()
    parser.add_argument("token")
    parser.add_argument("--url", default="https://captcha.sandbox.com.np")
    parser.add_argument(
        "-v", "--version", action="version", version=__version__
    )
    args = parser.parse_args()
    main_loop(args)


if __name__ == "__main__":
    main()
