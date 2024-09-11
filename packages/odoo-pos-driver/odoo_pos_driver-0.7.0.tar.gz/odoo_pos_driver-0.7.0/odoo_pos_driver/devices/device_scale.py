from .models.device_abstract import DeviceAbstract
from .scale_dialog06 import state_machine


class DeviceScale(DeviceAbstract):
    device_type = "scale"

    def read_weight(self, unit_price, tare):
        with self._get_serial() as serial:
            sm = state_machine.Dialog06Machine(
                serial, self.get_argument("polynomial", int), unit_price, tare
            )

            while not sm.current_state.final:
                sm.continue_communication()

        return {
            "weight": sm.weight,
            "error_number": sm.error_number,
            "error_description": sm.error_description,
        }
