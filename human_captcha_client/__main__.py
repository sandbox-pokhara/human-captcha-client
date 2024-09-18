import time
from argparse import ArgumentParser
from argparse import Namespace

import chime  # type:ignore
import httpx

from human_captcha_client import __version__
from human_captcha_client import logger
from human_captcha_client.api import post_captcha_solution
from human_captcha_client.api import request_captcha_task
from human_captcha_client.api import retrieve_settings
from human_captcha_client.api import skip_captcha
from human_captcha_client.auth import TokenAuth
from human_captcha_client.bbox import BboxSolver
from human_captcha_client.grid import GridSolver


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
    from ValLib.captcha import exceptions as valexceptions  # type:ignore
    from ValLib.captcha.web import WebServerSolver  # type:ignore

    solver_server = WebServerSolver(address="127.0.0.1")

    stop = False  # exit flag

    while not stop:
        try:
            task = request_captcha_task(args.url, auth)
            if "detail" in task:
                time.sleep(5)
                continue

            logger.info(f"New task received!")
            if not args.mute:
                chime.success()

            if "rqdata" in task["captcha_obj"]:
                solution = solver_server.token(
                    task["captcha_obj"]["rqdata"],
                    task["captcha_obj"]["sitekey"],
                )
            elif (
                "type" in task["captcha_obj"]
                and task["captcha_obj"]["type"] == "GRID"
            ):
                app = GridSolver(task)
                app.mainloop()
                stop = app.stop
                solution = app.solution
            elif (
                "type" in task["captcha_obj"]
                and task["captcha_obj"]["type"] == "BBOX"
            ):
                app = BboxSolver(task)
                app.mainloop()
                stop = app.stop
                solution = app.solution
            else:
                raise NotImplementedError("Captcha type not supported")
            logger.info("Solution received.")
            if solution:
                post_captcha_solution(args.url, auth, task["id"], solution)
            else:
                skip_captcha(args.url, auth, task["id"])
        except valexceptions.HCaptchaTimeoutException:
            logger.error("Captcha timed out.")
            time.sleep(5)
        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            time.sleep(5)
        except Exception as e:
            logger.exception(f"Unhandled exception: {e}")
            break


def main():
    parser = ArgumentParser()
    parser.add_argument("token")
    parser.add_argument("--mute", action="store_true")
    parser.add_argument("--url", default="https://captcha.sandbox.com.np")
    parser.add_argument(
        "-v", "--version", action="version", version=__version__
    )
    args = parser.parse_args()
    main_loop(args)


if __name__ == "__main__":
    main()
