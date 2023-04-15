class NumberUtils(object):
    @staticmethod
    def is_number(string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False
        