import time


def UtcTime():
    """"  Return the UTC time, converting the named tuple returned by
    Python into a non-named tuple.
      Python      : ( Y,M,D, H,M,S, DOW, DOY, DST )
      MicroPython : ( Y,M,D, H,M,S, DOW, DOY )
    """

    utc = time.gmtime()
    if len(utc) <= 8:
        return utc
    lst = []
    for this in utc[:8]:
        lst.append(this)
    return tuple(lst)


def IsLeapYear(year):
    if (year % 400) == 0:
        return 1
    if (year % 100) == 0:
        return 0
    if (year % 4) == 0:
        return 1
    return 0


def DaysInMonth(year, month):
    dif = 28 + IsLeapYear(year)
#       Jan Feb  Mar Apr May Jun Jul Aug Sep Oct Nov Dec
    return [31, dif, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]


def LocalTime(tz):
    year, month, day, h, m, s, dow, doy = UtcTime()
    x = tz[1]
    y = tz[2]
# Use as is when before DST start
    if month < x[0] \
    or (month == x[0] and day == x[1] and h < x[2] and m < x[3] and s < x[4]):
        pass
# Use as is when after DST ends
    elif month > y[0] \
    or (month == y[0] and day == y[1] and h >= y[2] and m >= y[3] and s >= y[4]):
        pass
# Otherwise apply the DST adjustment
    else:
        s += tz[3][2]
        m += tz[3][1]
        h += tz[3][0]
# Apply the time zone offset
    s += tz[0][2]
    m += tz[0][1] + int(s / 60)
    h += tz[0][0] + int(m / 60)
    s = s % 60
    m = m % 60
# Update Y,M,D
    while h >= 24:
        h -= 24
        day += 1
        if day > DaysInMonth(year, month):
            month += 1
            day = 1
        dow = (dow + 1) % 7
        doy += 1
    while h < 0:
        h += 24
        day -= 1
        if day <= 0:
            month -= 1
            day = DaysInMonth(year, month)
        # dow = (dow + 8) % 7
        dow -= 1
        doy -= 1
    return (year, month, day, h, m, s, dow, doy)


def Readable(t):
    #   0 1 2  3 4 5  6    7
    # ( Y,M,D, H,M,S, DOW, DOY )
    s = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][t[6]]
    s += " {:04}-{:02}-{:02}".format(t[0], t[1], t[2])
    s += " {:02}:{:02}:{:02}".format(t[3], t[4], t[5])
    return s


def Main():
    utc = UtcTime()

    print("UTC = {} = {}".format(utc, Readable(utc)))

# US Time Zone Info for 2022

    tz = [ [         -5, 0, 0],  # Time offset  [      H,M,S] -5 US/Eastern 
           [  3, 13, 1, 0, 0],  # Start of DST [ M,D, H,M,S] Mar 13
           [ 11, 6, 2, 0, 0],  # End   of DST [ M,D, H,M,S] Nov 6
           [         1, 0, 0]  # DST Adjust   [      H,M,S] +1 hour
       ]

    loc = LocalTime(tz)

    print("LOC = {} = {}".format(loc, Readable(loc)))


if __name__ == "__main__":
    Main()
