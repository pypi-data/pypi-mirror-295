import logging
import os
import sys

import click
import importlib_resources
import simplejson
from click_loglevel import LogLevel
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from loguru import logger

import odoo_pos_driver

from .app import app
from .interface import interface

# Define loguru specific level for logging
# to make click_loglevel working
logging.addLevelName(5, "TRACE")
logging.addLevelName(25, "SUCCESS")


@click.command()
@click.option(
    "-a",
    "--address",
    type=click.STRING,
    default="0.0.0.0",
    show_default=True,
    help="Address on which the web service will be exposed",
)
@click.option(
    "-p",
    "--port",
    type=click.INT,
    default=8069,
    show_default=True,
    help="Port on which the web service will be exposed",
)
@click.option(
    "--secure/--unsecure",
    default=True,
    show_default=True,
    help="Option 'secure' exposes web service on https."
    " Option 'unsecure' exposes web service on http.",
)
@click.option(
    "-r",
    "--refresh-devices-delay",
    type=click.INT,
    default=1,
    show_default=True,
    help="Interval in seconds between two device refreshes",
)
@click.option(
    "--arguments",
    type=click.STRING,
    default="{}",
    show_default=True,
    help="""Extra JSON arguments to pass to devices. Exemple:"
    " --arguments '{"scale": {"polynomial": "123456"}}'
    """,
)
@click.option(
    "-l",
    "--log-level",
    type=LogLevel(extra=["TRACE", "SUCCESS"]),
    default="INFO",
    show_default=True,
)
@click.version_option(version=odoo_pos_driver.__version__)
def main(log_level, address, port, refresh_devices_delay, secure, arguments):
    logger.success("Lauching odoo-pos-driver ...")
    log_path = "/tmp/odoo-pos-driver.log"
    logger.info(f"Application Path: {os.path.abspath(__file__)}")
    logger.info(f"Log Path: {log_path}")

    kwargs = {"handler_class": WebSocketHandler}

    # Log Configuration
    # remove first default sink that is defined to 'INFO'
    logger.remove()
    # logger.level("TRACE", no=5, color="<gray>")
    # Add stdout logger
    logger.add(sys.stderr, level=log_level)
    # Add file logger
    logger.add(log_path, level=log_level, rotation="1 week", enqueue=True)

    # Initialize Interface
    interface.initialize(
        refresh_devices_delay=refresh_devices_delay,
        arguments=simplejson.loads(arguments),
    )

    # Handle HTTPS, if required
    if secure:
        cert_folder = importlib_resources.files("odoo_pos_driver") / "default_cert"
        server_key_path = cert_folder / "server.key"
        server_cert_path = cert_folder / "server.crt"
        kwargs.update({"keyfile": server_key_path, "certfile": server_cert_path})
    http_server = pywsgi.WSGIServer((address, port), app, **kwargs)
    prefix = secure and "https" or "http"
    logger.success(
        f"Serving odoo-pos-driver (version: {odoo_pos_driver.__version__})"
        f" on {prefix}://{address}:{port} ..."
    )
    http_server.serve_forever()
