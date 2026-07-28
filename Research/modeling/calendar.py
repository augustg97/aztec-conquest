"""The four calendar systems of the conquest, and their conversions. Stdlib only.

The canonical frame decision (SCOPE.md §5), as code:

  * JULIAN is canonical — it is what every Spanish source uses (the Gregorian
    reform is 1582). Gregorian equivalents are shown alongside (+10 days in this
    century).
  * The app's time scalar `t` is a JULIAN fractional year: 1521.0 is 1 January
    1521 (Julian); one day is 1/365 or 1/366 of that Julian year.
  * Nahua dates: the 260-day tonalpohualli and the 365-day xiuhpohualli
    (18 veintenas of 20 days + 5 nemontemi), with named year-bearers.

THE CORRELATION IS ITSELF A CLAIM. This module anchors on the one pairing the
literature agrees on —

    13 August 1521 (Julian), the fall of Tenochtitlan, = 1 Cóatl,
    2nd day of Xocotlhuetzi, in the year 3 Calli
    (Caso 1967; the day-sign is repeated across the colonial annals)

— and extends it arithmetically. Alfonso Caso's other two anchor pairs
(first entry into Tenochtitlan = 8 Ehécatl, year 1 Ácatl; the Noche Triste
= 9 Ollin, year 2 Técpatl) are consistent with this anchor and are asserted in
the selftest. Confidence fields:

  * tonalpohualli day count ..... 'good'   (agreed across correlations for this window)
  * year-bearer 1519-1521 ....... 'good'   (attested: 1 Ácatl, 2 Técpatl, 3 Calli)
  * veintena + year boundary .... 'contested' (Caso himself concluded the year began
        with Izcalli, not Atlcahualo; azteccalendar-style extensions use Atlcahualo-first;
        this module uses Atlcahualo-first and SAYS SO in the output)
  * anything outside 1519-1521 .. degrade one step: the xiuhpohualli has no leap day,
        so any extension drifts ~1 day per 4 Julian years and no colonial attestation
        pins it. describe() marks dates outside the attested window.

The known ±1-day subtlety: European sources put the first entry on 8 November
1519; Caso's day-sign pairing (8 Ehécatl) falls on 9 November by this module's
arithmetic — the Nahua day did not start at midnight, and which European date a
Nahua day-sign "is" depends on that convention. The selftest asserts the 9
November pairing (Caso's own), and events.py stores European event dates from
the European sources. Never resolve this silently; it is why every Nahua date in
the UI is labelled a correlation.

Run me:  python3 calendar.py
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Julian / Gregorian / JDN  (standard integer algorithms)
# ---------------------------------------------------------------------------

def jdn_of_julian(y: int, m: int, d: int) -> int:
    """Julian Day Number of a Julian-calendar date (at noon)."""
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - 32083


def jdn_of_gregorian(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def julian_of_jdn(j: int):
    c = j + 32082
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = d - 4800 + m // 10
    return year, month, day


def gregorian_of_jdn(j: int):
    a = j + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + m // 10
    return year, month, day


def _julian_leap(y: int) -> bool:
    return y % 4 == 0


def julian_year_days(y: int) -> int:
    return 366 if _julian_leap(y) else 365


# ---------------------------------------------------------------------------
# the app's time scalar: Julian fractional year
# ---------------------------------------------------------------------------

def t_of_julian(y: int, m: int, d: int) -> float:
    """App scalar t for a Julian date: year + elapsed-days/year-length."""
    doy = jdn_of_julian(y, m, d) - jdn_of_julian(y, 1, 1)
    return y + doy / julian_year_days(y)


def julian_of_t(t: float):
    """Inverse of t_of_julian (nearest day)."""
    y = int(t)
    doy = round((t - y) * julian_year_days(y))
    doy = max(0, min(julian_year_days(y) - 1, doy))
    return julian_of_jdn(jdn_of_julian(y, 1, 1) + doy)


# ---------------------------------------------------------------------------
# tonalpohualli (260-day count)
# ---------------------------------------------------------------------------

SIGNS = ["Cipactli", "Ehécatl", "Calli", "Cuetzpalin", "Cóatl",
         "Miquiztli", "Mázatl", "Tochtli", "Atl", "Itzcuintli",
         "Ozomahtli", "Malinalli", "Ácatl", "Océlotl", "Cuauhtli",
         "Cozcacuauhtli", "Ollin", "Técpatl", "Quiáhuitl", "Xóchitl"]

VEINTENAS = ["Atlcahualo", "Tlacaxipehualiztli", "Tozoztontli", "Huey Tozoztli",
             "Tóxcatl", "Etzalcualiztli", "Tecuilhuitontli", "Huey Tecuílhuitl",
             "Tlaxochimaco", "Xocotlhuetzi", "Ochpaniztli", "Teotleco",
             "Tepeílhuitl", "Quecholli", "Panquetzaliztli", "Atemoztli",
             "Títitl", "Izcalli"]           # + 5 nemontemi days close the year

# THE anchor: 13 August 1521 (Julian) = 1 Cóatl, 2 Xocotlhuetzi, year 3 Calli.
ANCHOR_JDN = jdn_of_julian(1521, 8, 13)
ANCHOR_NUMBER_IDX = 0          # "1"
ANCHOR_SIGN_IDX = SIGNS.index("Cóatl")       # 4
ANCHOR_XIUH_DOY = 9 * 20 + 1   # 0-based day-of-xiuhpohualli-year: 2nd day of Xocotlhuetzi
ANCHOR_YEAR_NUMBER = 3
ANCHOR_YEAR_SIGN = SIGNS.index("Calli")      # year-bearer sign of 3 Calli

ATTESTED_WINDOW = (jdn_of_julian(1519, 2, 1), jdn_of_julian(1521, 12, 31))


def tonalpohualli(jdn: int):
    """(number 1-13, sign name) for any JDN. Confidence 'good' in the window."""
    delta = jdn - ANCHOR_JDN
    return ((ANCHOR_NUMBER_IDX + delta) % 13 + 1,
            SIGNS[(ANCHOR_SIGN_IDX + delta) % 20])


def xiuhpohualli(jdn: int):
    """(veintena-or-'nemontemi', day 1-20/1-5, year_number, year_sign, confidence).

    Atlcahualo-first day count anchored at 2 Xocotlhuetzi = 13 Aug 1521; the year
    bearer advances at each 365-day boundary. The veintena naming of the year
    START is the contested part (Caso: Izcalli-first) — hence 'contested'.
    """
    delta = jdn - ANCHOR_JDN
    doy = (ANCHOR_XIUH_DOY + delta) % 365
    years_on = (ANCHOR_XIUH_DOY + delta) // 365          # completed 365-day years since anchor year start
    if doy < 360:
        v, day = VEINTENAS[doy // 20], doy % 20 + 1
    else:
        v, day = "nemontemi", doy - 360 + 1
    n = (ANCHOR_YEAR_NUMBER - 1 + years_on) % 13 + 1
    s = SIGNS[(ANCHOR_YEAR_SIGN + 5 * years_on) % 20]
    conf = "contested" if ATTESTED_WINDOW[0] <= jdn <= ATTESTED_WINDOW[1] else "contested (extended)"
    return v, day, n, s, conf


def describe(jdn: int) -> dict:
    """Everything the app's card needs for one day, with confidence per system."""
    jy, jm, jd = julian_of_jdn(jdn)
    gy, gm, gd = gregorian_of_jdn(jdn)
    num, sign = tonalpohualli(jdn)
    v, vd, yn, ys, conf = xiuhpohualli(jdn)
    in_window = ATTESTED_WINDOW[0] <= jdn <= ATTESTED_WINDOW[1]
    return {
        "jdn": jdn,
        "julian": (jy, jm, jd),
        "gregorian": (gy, gm, gd),
        "t": t_of_julian(jy, jm, jd),
        "tonalpohualli": f"{num} {sign}",
        "tonalpohualli_confidence": "good" if in_window else "moderate",
        "xiuhpohualli": f"{vd} {v}, year {yn} {ys}",
        "xiuhpohualli_confidence": conf,
        "note": "Nahua equivalents are a correlation (anchor: 13 Aug 1521 = 1 Cóatl), not an attestation.",
    }


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt_julian(jdn: int) -> str:
    y, m, d = julian_of_jdn(jdn)
    return f"{d} {MONTHS[m - 1]} {y}"


# ---------------------------------------------------------------------------
# selftest — the contract
# ---------------------------------------------------------------------------

def _selftest():
    # JDN round trips, both calendars, across the model window and edges.
    for y in range(1500, 1553):
        for (m, d) in ((1, 1), (2, 28), (3, 1), (8, 13), (12, 31)):
            j = jdn_of_julian(y, m, d)
            assert julian_of_jdn(j) == (y, m, d), f"julian roundtrip {y}-{m}-{d}"
            g = jdn_of_gregorian(y, m, d)
            assert gregorian_of_jdn(g) == (y, m, d), f"gregorian roundtrip {y}-{m}-{d}"

    # Julian leap day exists in 1520 (and the century year 1500 IS a Julian leap year).
    assert julian_of_jdn(jdn_of_julian(1520, 2, 29)) == (1520, 2, 29)
    assert julian_of_jdn(jdn_of_julian(1500, 2, 29)) == (1500, 2, 29)

    # The 10-day offset of this century: 13 Aug 1521 Julian = 23 Aug 1521 Gregorian.
    assert gregorian_of_jdn(jdn_of_julian(1521, 8, 13)) == (1521, 8, 23)

    # The anchor itself.
    assert tonalpohualli(ANCHOR_JDN) == (1, "Cóatl")
    v, vd, yn, ys, _ = xiuhpohualli(ANCHOR_JDN)
    assert (v, vd, yn, ys) == ("Xocotlhuetzi", 2, 3, "Calli"), (v, vd, yn, ys)

    # Caso's other two anchor pairs, consistent with THIS anchor by pure arithmetic:
    #   Noche Triste, 1 Jul 1520 = 9 Ollin, in year 2 Técpatl.
    nt = jdn_of_julian(1520, 7, 1)
    assert tonalpohualli(nt) == (9, "Ollin"), tonalpohualli(nt)
    assert xiuhpohualli(nt)[2:4] == (2, "Técpatl"), xiuhpohualli(nt)
    #   First entry pairing 8 Ehécatl falls on 9 Nov 1519 (European sources say the
    #   meeting was 8 Nov — the documented day-start ambiguity; see module docstring).
    fe = jdn_of_julian(1519, 11, 9)
    assert tonalpohualli(fe) == (8, "Ehécatl"), tonalpohualli(fe)
    assert xiuhpohualli(fe)[2:4] == (1, "Ácatl"), xiuhpohualli(fe)

    # Periodicity.
    assert tonalpohualli(ANCHOR_JDN + 260) == (1, "Cóatl")
    assert xiuhpohualli(ANCHOR_JDN)[0:2] == xiuhpohualli(ANCHOR_JDN + 365)[0:2]
    # Year bearer advances +1 number, +5 signs: 3 Calli -> 4 Tochtli.
    assert xiuhpohualli(ANCHOR_JDN + 365)[2:4] == (4, "Tochtli")

    # Nemontemi are reachable and bounded.
    seen = set()
    for k in range(365):
        v = xiuhpohualli(ANCHOR_JDN + k)[0]
        seen.add(v)
    assert "nemontemi" in seen and len(seen) == 19, len(seen)

    # t scalar round trips at day resolution.
    for (y, m, d) in ((1502, 1, 1), (1519, 11, 8), (1520, 7, 1), (1521, 8, 13), (1550, 12, 31)):
        assert julian_of_t(t_of_julian(y, m, d)) == (y, m, d), (y, m, d)
    # t is monotone across a year boundary and a leap day.
    assert t_of_julian(1520, 12, 31) < t_of_julian(1521, 1, 1)
    assert t_of_julian(1520, 2, 28) < t_of_julian(1520, 2, 29) < t_of_julian(1520, 3, 1)

    print("selftest OK — Julian/Gregorian/JDN, tonalpohualli, xiuhpohualli, t scalar; "
          "3 Caso anchor pairs consistent")


if __name__ == "__main__":
    _selftest()
    for label, (y, m, d) in [("first entry into Tenochtitlan (European date)", (1519, 11, 8)),
                             ("Noche Triste", (1520, 7, 1)),
                             ("fall of Tenochtitlan", (1521, 8, 13))]:
        info = describe(jdn_of_julian(y, m, d))
        jy, jm, jd = info["julian"]; gy, gm, gd = info["gregorian"]
        print(f"\n{label}:")
        print(f"  Julian {jd} {MONTHS[jm-1]} {jy}  =  Gregorian {gd} {MONTHS[gm-1]} {gy}")
        print(f"  tonalpohualli {info['tonalpohualli']} ({info['tonalpohualli_confidence']})"
              f"  ·  xiuhpohualli {info['xiuhpohualli']} ({info['xiuhpohualli_confidence']})")
        print(f"  t = {info['t']:.4f}")
