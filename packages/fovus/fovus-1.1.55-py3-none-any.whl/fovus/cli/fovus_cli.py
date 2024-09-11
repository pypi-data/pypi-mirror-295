#!/usr/bin/env python3
import logging
import os
import sys
import time

from fovus.cli.cli_action_runner import CliActionRunner
from fovus.cli.fovus_cli_argument_parser import FovusCliArgumentParser
from fovus.cli.ssl import configure_ssl_env
from fovus.constants.cli_constants import PATH_TO_LOGS
from fovus.constants.util_constants import UTF8
from fovus.exception.status_code_exception import StatusException

OK_RETURN_STATUS = 0
ERROR_RETURN_STATUS = 1

BASIC_FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def main():
    configure_ssl_env()

    return_status = OK_RETURN_STATUS

    logger = logging.getLogger()

    log_path = os.path.join(PATH_TO_LOGS, time.strftime("%Y-%m-%d_%H-%M-%S.log"))
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    file_handler = logging.FileHandler(log_path, mode="a", encoding=UTF8)
    file_handler.setFormatter(BASIC_FORMATTER)

    log_level = logging.INFO

    if "--debug" in sys.argv:
        sys.argv.remove("--debug")
        log_level = logging.DEBUG

    logger.setLevel(log_level)
    file_handler.setLevel(log_level)

    logger.addHandler(file_handler)

    try:
        _main()
    except StatusException as exc:
        print(exc)
        logging.critical("An status exception occurred in main.")
        logging.exception(exc)
        return_status = ERROR_RETURN_STATUS
    except Exception as exc:  # pylint: disable=broad-except
        print(exc)
        logging.critical("An unhandled exception occurred in main.")
        logging.exception(exc)
        return_status = ERROR_RETURN_STATUS

    return return_status


def _main():
    parser = FovusCliArgumentParser()
    parser.parse_args()
    parser.update_overridden_configs()

    args = parser.get_args_dict()

    cli_action_runner = CliActionRunner(args)
    cli_action_runner.run_actions()


if __name__ == "__main__":
    sys.exit(main())
