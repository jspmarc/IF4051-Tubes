from enum import Enum, EnumMeta


class AppModeMeta(EnumMeta):
    def __contains__(cls, item: object) -> bool:
        '''
        This enables check using `in` operator
        example: `if 'Ai' in AppMode:`
        '''
        try:
            cls(item)
        except ValueError:
            return False
        return True


class AppMode(Enum, metaclass=AppModeMeta):
    Ai = 'Ai'
    Override = 'Override'


class AlertType(Enum):
    HighTemperature = 0
    HighCo2Ppm = 1
