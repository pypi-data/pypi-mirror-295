from flask import jsonify, request
from loguru import logger

from ..app import app
from ..interface import interface


@app.route("/hw_proxy/scale_get_weight", methods=["POST", "PUT"])
@logger.catch
def scale_get_weight():
    data = request.json.get("params", {}).get("data", {})
    logger.trace(f"scale_get_weight() {data}")

    try:
        unit_price = float(data.get("unit_price"))
    except ValueError:
        unit_price = 0.0
    try:
        tare = float(data.get("tare"))
    except ValueError:
        tare = 0.0

    result = interface.device_scale_read_weight(unit_price, tare)
    return jsonify(jsonrpc="2.0", result=result)
