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
    HighTemperature = "high temperature"
    HighCo2Ppm = "high CO2 PPM"

    def to_mail_subject(self):
        return (
            "High CO2 PPM warning"
            if self == AlertType.HighCo2Ppm
            else "High temperature warning"
        )
