from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
import math

try:
    import swisseph  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    swisseph = None


MOON_SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)

PHASE_NAMES = (
    "new_moon",
    "waxing_crescent",
    "first_quarter",
    "waxing_gibbous",
    "full_moon",
    "waning_gibbous",
    "last_quarter",
    "waning_crescent",
)


@dataclass(frozen=True)
class MoonReading:
    moon_sign: str
    moon_phase: str
    illuminated_fraction: float
    source: str


class MoonCalculator:
    def __init__(self, use_swisseph: bool = True) -> None:
        self.use_swisseph = use_swisseph and swisseph is not None

    def calculate(
        self,
        birth_date: date | str,
        birth_time: time | str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
    ) -> MoonReading:
        moment = self._coerce_datetime(birth_date, birth_time)

        if self.use_swisseph:
            try:
                return self._calculate_with_swisseph(moment, latitude, longitude)
            except Exception:
                pass

        return self._calculate_with_approximation(moment)

    def _calculate_with_swisseph(
        self,
        moment: datetime,
        latitude: float | None,
        longitude: float | None,
    ) -> MoonReading:
        del latitude, longitude

        julian_day = swisseph.julday(
            moment.year,
            moment.month,
            moment.day,
            moment.hour + moment.minute / 60 + moment.second / 3600,
        )
        moon_longitude = swisseph.calc_ut(julian_day, swisseph.MOON)[0][0] % 360
        sun_longitude = swisseph.calc_ut(julian_day, swisseph.SUN)[0][0] % 360
        phase_fraction = ((moon_longitude - sun_longitude) % 360) / 360

        return MoonReading(
            moon_sign=MOON_SIGNS[int(moon_longitude // 30)],
            moon_phase=self._phase_name(phase_fraction),
            illuminated_fraction=(1 - math.cos(phase_fraction * 2 * math.pi)) / 2,
            source="swisseph",
        )

    def _calculate_with_approximation(self, moment: datetime) -> MoonReading:
        julian_day = self._julian_day(moment)
        phase_fraction = self._moon_phase_fraction(julian_day)
        moon_longitude = self._approximate_moon_longitude(julian_day)

        return MoonReading(
            moon_sign=MOON_SIGNS[int(moon_longitude // 30)],
            moon_phase=self._phase_name(phase_fraction),
            illuminated_fraction=(1 - math.cos(phase_fraction * 2 * math.pi)) / 2,
            source="approximation",
        )

    @staticmethod
    def _coerce_datetime(
        birth_date: date | str,
        birth_time: time | str | None,
    ) -> datetime:
        if isinstance(birth_date, str):
            parsed_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        else:
            parsed_date = birth_date

        if birth_time is None:
            parsed_time = time(hour=12, minute=0)
        elif isinstance(birth_time, str):
            parsed_time = datetime.strptime(birth_time, "%H:%M").time()
        else:
            parsed_time = birth_time

        return datetime.combine(parsed_date, parsed_time)

    @staticmethod
    def _julian_day(moment: datetime) -> float:
        year = moment.year
        month = moment.month
        day = (
            moment.day
            + moment.hour / 24
            + moment.minute / 1440
            + moment.second / 86400
        )

        if month <= 2:
            year -= 1
            month += 12

        a = year // 100
        b = 2 - a + a // 4

        return (
            math.floor(365.25 * (year + 4716))
            + math.floor(30.6001 * (month + 1))
            + day
            + b
            - 1524.5
        )

    @staticmethod
    def _moon_phase_fraction(julian_day: float) -> float:
        synodic_month = 29.53058867
        known_new_moon = 2451550.1
        return ((julian_day - known_new_moon) / synodic_month) % 1

    @staticmethod
    def _approximate_moon_longitude(julian_day: float) -> float:
        days_since_epoch = julian_day - 2451545.0
        mean_longitude = (218.316 + 13.176396 * days_since_epoch) % 360
        mean_anomaly = (134.963 + 13.064993 * days_since_epoch) % 360
        mean_elongation = (297.850 + 12.190749 * days_since_epoch) % 360

        return (
            mean_longitude
            + 6.289 * math.sin(math.radians(mean_anomaly))
            + 1.274 * math.sin(math.radians((2 * mean_elongation) - mean_anomaly))
            + 0.658 * math.sin(math.radians(2 * mean_elongation))
            + 0.214 * math.sin(math.radians(2 * mean_anomaly))
        ) % 360

    @staticmethod
    def _phase_name(phase_fraction: float) -> str:
        index = int(((phase_fraction * 8) + 0.5) % 8)
        return PHASE_NAMES[index]
