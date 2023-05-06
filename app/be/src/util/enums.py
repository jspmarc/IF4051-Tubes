from ctypes import ArgumentError
from enum import Enum, EnumMeta


class AppModeMeta(EnumMeta):
    def __contains__(cls, item: object) -> bool:
        """
        This enables check using `in` operator
        example: `if 'Ai' in AppMode:`
        """
        try:
            cls(item)
        except ValueError:
            return False
        return True


class AppMode(Enum, metaclass=AppModeMeta):
    Ai = "Ai"
    Override = "Override"


class AlertType(str, Enum):
    HighTemperature = "HighTemp"
    LowTemperature = "LowTemp"
    HighCo2Ppm = "HighCo2"
    LowCo2Ppm = "LowCo2"

    def to_mail_subject(self):
        match self:
            case AlertType.HighCo2Ppm:
                return "HIGH CO2 PPM warning"
            case AlertType.LowCo2Ppm:
                return "LOW CO2 PPM warning"
            case AlertType.HighTemperature:
                return "HIGH temperature warning"
            case AlertType.LowTemperature:
                return "LOW temperature warning"
