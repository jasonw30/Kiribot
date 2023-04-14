from math import floor
from collections import namedtuple

xp_tuple = namedtuple("xp_tuple", ["total_xp", "remain_xp", "level"])

class xp_converter:

    @staticmethod
    def convert_level(xp_amount: str or int) -> str:
        try:
            xp = int(xp_amount)

            return xp_tuple(xp, xp % 100, floor(xp / 100))
        except (TypeError, ValueError) as error:
            print(f"[KiriStat] {str(error)}")

    @staticmethod
    def convert_rank(xp_amount: str or int=None) -> str:
        try:
            xp = int(xp_amount)

            if xp >= 100000:
                return "Kiri-tastic"
            elif xp >= 10000:
                return "God-Tier"
            elif xp >= 1000:
                return "Proactive Member"
            elif xp >= 100:
                return "Active Member"
            else:
                return "Member"
        except (TypeError, ValueError) as error:
            print(f"[KiriStat] {str(error)}")


if __name__ == "__main__":
    x = xp_converter.convert_level(15324324)
    print(x)
    x = xp_converter.convert_rank(15324324)
    print(x)