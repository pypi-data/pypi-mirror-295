import time
from datetime import datetime
from threading import Thread

import usb
from loguru import logger

from .devices import DeviceDisplay, DevicePayment, DevicePrinter, DeviceScale
from .usb_device import usb_device_list, usb_device_tools


class Interface(Thread):
    device_types = ["display", "printer", "payment", "scale"]

    def initialize(self, refresh_devices_delay=1, arguments={}):
        self.disconnections = {}
        self.start_date = datetime.now()
        self.usb_devices = []
        self.refresh_devices_delay = refresh_devices_delay
        self.usb_device_display = DeviceDisplay(
            self, arguments.get("display", {}), delay=0.2, max_queue_size=10
        )
        self.usb_device_printer = DevicePrinter(
            self, arguments.get("printer", {}), delay=1, max_queue_size=3
        )

        self.usb_device_payment = DevicePayment(self, arguments.get("payment", {}))

        self.usb_device_scale = DeviceScale(self, arguments.get("scale", {}))

        self.refresh_usb_devices()

        for device in [self.get_device(x) for x in self.device_types]:
            if device.has_queue:
                device.start()

        self.start()

    # ###########################
    # Public Implemented Devices Section
    # ###########################

    def device_display_task_show(self, data):
        self.usb_device_display.add_task(data)

    def device_printer_task_print(self, receipt):
        self.usb_device_printer.add_task(("print", receipt))

    def device_printer_task_open_cashbox(self):
        self.usb_device_printer.add_task(("open_cashbox", False))

    def device_scale_read_weight(self, unit_price, tare):
        return self.usb_device_scale.read_weight(unit_price, tare)

    def device_payment_push_amount(self, amount, currency_iso):
        return self.usb_device_payment.push_amount(amount, currency_iso)

    # ###########################
    # Generic Device Section
    # ###########################

    def get_device(self, device_type):
        return getattr(self, f"usb_device_{device_type}")

    @logger.catch
    def refresh_usb_devices(self):
        logger.debug(
            "Refreshing USB Devices List ..."
            f"(Next refresh in {self.refresh_devices_delay} second(s).)"
        )
        new_devices = [device for device in usb.core.find(find_all=True)]

        # Detect new devices
        for device in new_devices:
            if device not in self.usb_devices:
                self._hook_usb_device_new(device)

        # Handle device removal
        for device in self.usb_devices:
            if device not in new_devices:
                self._hook_usb_device_removed(device)

    def _hook_usb_device_new(self, device):
        """Handle here things to be done, when a new device is detected"""
        (device_type, extra_info) = usb_device_list.get_device_type(
            device.idVendor, device.idProduct
        )
        if (
            usb_device_tools.get_device_id_vendor_id_product(device)
            not in self.disconnections.keys()
        ):
            self.disconnections[
                usb_device_tools.get_device_id_vendor_id_product(device)
            ] = []

        logger.log(
            device_type and "SUCCESS" or "DEBUG",
            f"Found new USB device."
            f" Type '{device_type or 'Unknown'}'."
            f" Name '{device_type and extra_info['name'] or 'Unknown'}'."
            " Code:"
            f" {usb_device_tools.get_device_id_vendor_id_product(device)} ;"
            f" Tecnical Name: {usb_device_tools.get_device_product(device)}",
        )
        if device_type:
            getattr(self, f"usb_device_{device_type}").set_usb_device(
                device, extra_info
            )
        self.usb_devices.append(device)

    def _hook_usb_device_removed(self, device, error=False):
        """Handle here cleanup to be done, when a removal of
        device is detected"""
        (device_type, _extra_info) = usb_device_list.get_device_type(
            device.idVendor, device.idProduct
        )
        self.disconnections[
            usb_device_tools.get_device_id_vendor_id_product(device)
        ].append({"date": datetime.now(), "error": error})
        logger.info(
            f"Removing USB device."
            " Code:"
            f" {usb_device_tools.get_device_id_vendor_id_product(device)} ;"
            f" Name: {usb_device_tools.get_device_product(device)}"
        )
        if device_type:
            getattr(self, f"usb_device_{device_type}").remove_usb_device()
        self.usb_devices.remove(device)

    # ###########################
    # Thread Section
    # ###########################

    def run(self):
        while True:
            time.sleep(self.refresh_devices_delay)
            self.refresh_usb_devices()


interface = Interface()
