import simplejson
from flask import jsonify, request
from loguru import logger

from ..app import app
from ..interface import interface


@app.route("/hw_proxy/display_show", methods=["POST", "PUT"])
@logger.catch
def customer_display_send_text():
    logger.trace("customer_display_show()")
    data = request.json.get("params", {}).get("data", {})

    if not data:
        raise Exception(f"Incorrect argument: '{request.json}'")

    if type(data) is str:
        data = simplejson.loads(data)

    interface.device_display_task_show(data)
    return jsonify(jsonrpc="2.0", result=True)
