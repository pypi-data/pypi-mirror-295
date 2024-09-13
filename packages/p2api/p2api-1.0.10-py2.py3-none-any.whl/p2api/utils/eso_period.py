# -*- coding: utf-8 -*-
import datetime
import copy

# ---------------------------------------------------------------------------------------
## From https://stackoverflow.com/questions/51913210/python-script-with-timezone-fails-when-back-ported-to-python-2-7
ZERO = datetime.timedelta(0)
HOUR = datetime.timedelta(hours=1)

class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

tz_utc=UTC()
if hasattr(datetime,'timezone') :
    if hasattr(datetime.timezone,'utc') :
        tz_utc=datetime.timezone.utc
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
def get_ESO_period( d ):
    """
    Return the (int) ESO period for a specified datetime.date or datetime.datetime
    If d is naive (no timezone), UTC is assumed
    """
    ## ToDo: Update this method when we go to yearly cycle!
    ## 2024-07: currently planned for P117, with P116 lasting 7 months...
    # 113 2024-04 -- 2024-09
    # 114 2024-10 -- 2025-03
    # 115 2025-04 -- 2026-09
    # 116 2025-10 -- 2026-04
    # 117 2026-05 -- 2027-04
    # 118 2027-05 -- 2028-04
    # ...
    if isinstance(d,datetime.date) :
        d=datetime.datetime(
            year=d.year,
            month=d.month,
            day=d.day,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=tz_utc,
        )
    if d.tzinfo is None :
        d=d.replace(tzinfo=tz_utc)
    if d < datetime.datetime(2025,10,1,0,0,tzinfo=tz_utc) :
        # P < 116...
        return ((d.year-2012)+44)*2+int(float(d.month+2)/6.)
    elif d > datetime.datetime(2026,5,1,0,0,tzinfo=tz_utc) :
        # P > 116...
        return ((d.year-2026)+116)+int(float(d.month+7)/12.)
    elif d > datetime.datetime(2026,4,1,0,0,tzinfo=tz_utc) :
        ## Special case for 7month long P116
        return ((d.year-2012)+44)*2+int(float(d.month+2)/7.)  
    return ((d.year-2012)+44)*2+int(float(d.month+2)/6.)
# ---------------------------------------------------------------------------------------
def current_ESO_period( days_from_now=0, dt=None ):
    d=datetime.datetime.now(tz_utc) + datetime.timedelta(days=days_from_now)
    return get_ESO_period(d)
# ---------------------------------------------------------------------------------------
def ESO_period_datetime_start( eso_period=current_ESO_period() ):
    ## ToDo: Update this method when we go to yearly cycle!
    ## 2024-07: currently planned for P117, with P116 lasting 7 months...
    ## i.e.
    ## P115 starts 
    if eso_period < 116 :
        y=2024+(eso_period-113)//2
        m=4+6*((eso_period-113)%2)
    elif eso_period > 116 :
        y=2026+(eso_period-117)
        m=5
    else :
        y=2025
        m=10
    return datetime.datetime(y,m,1,0,0,0,0,tzinfo=tz_utc)
# ---------------------------------------------------------------------------------------
def ESO_period_datetime_end( eso_period=current_ESO_period() ):
    return ESO_period_datetime_start((eso_period or current_ESO_period())+1)-datetime.timedelta(days=1)
# ---------------------------------------------------------------------------------------
def ESO_period_date_start( eso_period=current_ESO_period() ):
    return ESO_period_datetime_start( eso_period ).date()
# ---------------------------------------------------------------------------------------
def ESO_period_date_end( eso_period=current_ESO_period() ):
    return ESO_period_datetime_end( eso_period ).date()
# ---------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__' :
    ## ToDo: These tests, should be moved to proper tests...

    ## Testing get_ESO_period
    ## verify input date type is not changed
    d=datetime.date(2024,4,1)
    get_ESO_period(d)
    assert isinstance(d,datetime.date)
    
    # verify input datetime tzinfo is not modified
    d=datetime.datetime(2024,4,1,0,0)
    get_ESO_period(d)
    assert d.tzinfo is None

    # P113
    assert get_ESO_period(datetime.date(2024,4,1))               == 113
    assert get_ESO_period(datetime.datetime(2024,4,1,0,0))       == 113
    assert get_ESO_period(datetime.datetime(2024,9,30,23,59,59)) == 113
    # P114
    assert get_ESO_period(datetime.datetime(2024,10,1,0,0))      == 114
    assert get_ESO_period(datetime.datetime(2025,3,31,23,59,59)) == 114
    # P115
    assert get_ESO_period(datetime.datetime(2025,4,1,0,0))       == 115
    assert get_ESO_period(datetime.datetime(2025,9,30,23,59,59)) == 115
    # P116
    assert get_ESO_period(datetime.datetime(2025,10,1,0,0))      == 116
    assert get_ESO_period(datetime.datetime(2026,3,31,23,59,59)) == 116
    assert get_ESO_period(datetime.datetime(2026,4,30,23,59,59)) == 116
    # P117
    assert get_ESO_period(datetime.datetime(2026,5,1,0,0))       == 117
    assert get_ESO_period(datetime.datetime(2027,4,30,23,59,59)) == 117
    # P118
    assert get_ESO_period(datetime.datetime(2027,5,1,0,0))       == 118
    assert get_ESO_period(datetime.datetime(2028,4,30,23,59,59)) == 118

    ## testing ESO_period_date_start() & ESO_period_date_end()
    # P113
    assert ESO_period_date_start(113) == datetime.date(2024,4,1)
    assert ESO_period_date_end(113)   == datetime.date(2024,9,30)
    # P114
    assert ESO_period_date_start(114) == datetime.date(2024,10,1)
    assert ESO_period_date_end(114)   == datetime.date(2025,3,31)
    # P115
    assert ESO_period_date_start(115) == datetime.date(2025,4,1)
    assert ESO_period_date_end(115)   == datetime.date(2025,9,30)
    # P116
    assert ESO_period_date_start(116) == datetime.date(2025,10,1)
    assert ESO_period_date_end(116)   == datetime.date(2026,4,30)
    # P117
    assert ESO_period_date_start(117) == datetime.date(2026,5,1)
    assert ESO_period_date_end(117)   == datetime.date(2027,4,30)
    # P118
    assert ESO_period_date_start(118) == datetime.date(2027,5,1)
    assert ESO_period_date_end(118)   == datetime.date(2028,4,30)
