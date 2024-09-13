import base64
from datetime import datetime
from io import BytesIO

from flask import jsonify, request
from loguru import logger
from PIL import Image

from ..app import app
from ..interface import interface


@app.route("/hw_proxy/default_printer_action", methods=["POST", "PUT"])
@logger.catch
def default_printer_action():
    data = request.json.get("params", {}).get("data", {})
    logger.trace(f"default_printer_action() ({data.get('action', False)})")
    if not data:
        raise Exception(f"Incorrect argument: '{request.json}'")

    if data.get("action") == "print_receipt":
        receipt = data["receipt"]
        if logger._core.min_level <= logger.level("DEBUG").no:
            try:
                image = Image.open(BytesIO(base64.b64decode(receipt)))
                dt = datetime.now().isoformat("_").replace(":", "-").replace(".", "-")
                filepath = f"/tmp/odoo-pos-driver__print__{dt}.{image.format}"
                image.save(filepath)
                logger.debug(f"Image saved into {filepath}")
            except Exception as e:
                logger.debug(f"Unable to log image. {e}")
        interface.device_printer_task_print(receipt)

    elif data.get("action") == "cashbox":
        interface.device_printer_task_open_cashbox()

    else:
        raise Exception(f"Incorrect action value: '{data.get('action')}'")

    return jsonify(jsonrpc="2.0", result=True)
