#!/bin/python3
# AeUeCalendar, urspruenglich erstellt fuer die Infinite Adventures
# Die gesamte Datei ist gemeinfrei / public domain / CC0.
# Tobias Frei, 2022

# This is free and unencumbered software released into the public domain.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

TF_SECONDS_PER_OERZKLOEK: float = 7909306972 / 9192631770
TF_SECONDS_PER_OERZBIT: float = 343 * 49 * 49 * 49 * TF_SECONDS_PER_OERZKLOEK


def tf_convert_utc_auc(tf_in_date: dict) -> dict:
    # UTC -> AUC
    tf_out_date: dict[str, int] = {
        "year": -5000,
        "month": 1,
        "day": 1,
        "hour": 0,
        "minute": 0,
        "second": 0
    }

    if ((tf_in_date["year"] % 4 == 0) and (tf_in_date["year"] % 100 != 0)) or (tf_in_date["year"] % 400 == 0):
        # leap year
        tf_calendar: list[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        tf_current_year_days: int = 366
    else:
        tf_calendar: list[int] = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        tf_current_year_days: int = 365
    tf_current_year_hours: int = tf_current_year_days * 24
    tf_current_year_minutes: int = tf_current_year_hours * 60
    tf_current_year_seconds: int = tf_current_year_minutes * 60
    tf_past_days: int = 0
    # Months start at 1, so "1" means no month has passed and "12" means 11 have passed
    tf_past_months: int = tf_in_date["month"] - 1
    for x in tf_calendar:
        if tf_past_months < 1:
            break
        tf_past_days += x
        tf_past_months -= 1

    # Days start at 1 as well
    tf_in_year_decimal: float = tf_in_date["year"]
    tf_in_year_decimal += (tf_past_days + tf_in_date["day"] - 1) / tf_current_year_days
    tf_in_year_decimal += tf_in_date["hour"] / tf_current_year_hours
    tf_in_year_decimal += tf_in_date["minute"] / tf_current_year_minutes
    tf_in_year_decimal += tf_in_date["second"] / tf_current_year_seconds
    tf_out_year_decimal: float = tf_seconds_ab_urbe_condita(tf_in_date["year"])
    tf_out_year_decimal += (tf_past_days + tf_in_date["day"] - 1) * 24 * 60 * 60
    tf_out_year_decimal += tf_in_date["hour"] * 60 * 60
    tf_out_year_decimal += tf_in_date["minute"] * 60
    tf_out_year_decimal += tf_in_date["second"]
    tf_out_year_decimal /= TF_SECONDS_PER_OERZBIT

    # Exporting to AUC is simple as there are no leap years, each month has the same length and all fields start at 0.
    tf_rest = tf_out_year_decimal  # e.g. 2033.4029528
    tf_out_date["year"] = int(tf_out_year_decimal // 1)  # e.g. 2033
    tf_rest -= tf_out_date["year"]  # e.g. 0.4029528
    tf_out_date["month"] = int((tf_rest * 7) // 1)  # AUC years have 7 months
    tf_rest -= tf_out_date["month"] / 7
    tf_out_date["day"] = int((tf_rest * 343) // 1)  # AUC years have 343 days
    tf_rest -= tf_out_date["day"] / 343
    tf_out_date["hour"] = int((tf_rest * 343 * 49) // 1)  # AUC days have 49 hours
    tf_rest -= tf_out_date["hour"] / (343 * 49)
    tf_out_date["minute"] = int((tf_rest * 343 * 49 * 49) // 1)  # AUC hours have 49 minutes
    tf_rest -= tf_out_date["minute"] / (343 * 49 * 49)
    tf_out_date["second"] = int((tf_rest * 343 * 49 * 49 * 49) // 1)  # AUC minutes have 49 seconds
    tf_rest -= tf_out_date["second"] / (343 * 49 * 49 * 49)

    return tf_out_date


def tf_seconds_ab_urbe_condita(tf_in_year: int) -> int:
    # How many seconds have passed between the start of "-752" and the start of the current year?
    tf_out_seconds: int = 0
    tf_loop_begin: int = min(tf_in_year, (-752))
    tf_loop_end: int = max(tf_in_year, (-752))
    tf_loop_sign: int = (tf_in_year > (-752)) - (tf_in_year < (-752))
    for y in range(tf_loop_begin, tf_loop_end):
        if ((y % 4 == 0) and (y % 100 != 0)) or (y % 400 == 0):
            # leap year
            tf_out_seconds += 366 * 24 * 60 * 60
        else:
            tf_out_seconds += 365 * 24 * 60 * 60
    return tf_loop_sign * tf_out_seconds


def main() -> None:
    tf_calendar_main: list[int] = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    tf_in_date: dict[str, int] = {
        "year": -999,
        "month": 1,
        "day": 1,
        "hour": 0,
        "minute": 0,
        "second": 0
    }

    while tf_in_date["year"] <= 3000:
        tf_out_date = tf_convert_utc_auc(tf_in_date)
        tf_out_string = str(int(tf_in_date["year"])).zfill(4) + "-"
        tf_out_string += str(int(tf_in_date["month"])).zfill(2) + "-"
        tf_out_string += str(int(tf_in_date["day"])).zfill(2) + ", "
        tf_out_string += str(int(tf_in_date["hour"])).zfill(2) + ":"
        tf_out_string += str(int(tf_in_date["minute"])).zfill(2) + ":"
        tf_out_string += str(int(tf_in_date["second"])).zfill(2) + " UTC = "
        tf_out_string += str(int(tf_out_date["year"])).zfill(4) + "-"
        tf_out_string += str(int(tf_out_date["month"])).zfill(2) + "-"
        tf_out_string += str(int(tf_out_date["day"])).zfill(2) + ", "
        tf_out_string += str(int(tf_out_date["hour"])).zfill(2) + ":"
        tf_out_string += str(int(tf_out_date["minute"])).zfill(2) + ":"
        tf_out_string += str(int(tf_out_date["second"])).zfill(2) + " ÄÜC"
        print(tf_out_string)

        if ((tf_in_date["year"] % 4 == 0) and (tf_in_date["year"] % 100 != 0)) or (tf_in_date["year"] % 400 == 0):
            # leap year
            tf_calendar_main[1] = 29
        else:
            tf_calendar_main[1] = 28

        tf_in_date["hour"] += 1
        if tf_in_date["hour"] > 23:
            tf_in_date["hour"] = 0
            tf_in_date["day"] += 1
        if tf_in_date["day"] > tf_calendar_main[tf_in_date["month"] - 1]:
            tf_in_date["day"] = 1
            tf_in_date["month"] += 1
        if tf_in_date["month"] > 12:
            tf_in_date["month"] = 1
            tf_in_date["year"] += 1


if __name__ == "__main__":
    main()
