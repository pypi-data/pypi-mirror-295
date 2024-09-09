# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from sys import stdout


class Logger:
    def __init__(self, logger_name: str) -> None:
        """Initialize a logger.

        Args:
            logger_name (str): A logger name.
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False

        self.logger.setLevel(logging.INFO)

        self.handler: logging.Handler | None = None
        handler = logging.StreamHandler(stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(name)s | %(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self._set_handler(handler)

    def __call__(self) -> logging.Logger:
        """Return a logger.

        Returns:
            logging.Logger: The logger.
        """
        return self.logger

    def _set_handler(self, handler: logging.Handler) -> None:
        """Set a handler.

        Args:
            handler (logging.Handler, optional): Set a handler (replacing the existing handler).
            Defaults to logging.NullHandler().
        """
        if self.handler is not None:
            self.logger.removeHandler(self.handler)
        self.handler = handler
        self.logger.addHandler(self.handler)


logger = Logger("amplify-bbopt")
