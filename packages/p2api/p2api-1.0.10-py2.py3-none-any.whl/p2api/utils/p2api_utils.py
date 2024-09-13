# -*- coding: utf-8 -*-
import datetime
import logging
import p2api
import sys
import time
import getpass
import keyring
import re

from p2api.utils.eso_period import *

try:
    import astropy.units as u
    from astropy.coordinates import EarthLocation
    # The GPS coordinates of the UTs
    # https://www.eso.org/sci/facilities/paranal/astroclimate/site.html
    UT1_loc = EarthLocation.from_geodetic('-70d24m18.27s', '-24d37m39.44s', (2635.43+13.044)*u.m)
    UT2_loc = EarthLocation.from_geodetic('-70d24m17.39s', '-24d37m37.80s', (2635.43+13.044)*u.m)
    UT3_loc = EarthLocation.from_geodetic('-70d24m16.32s', '-24d37m36.64s', (2635.43+13.044)*u.m)
    UT4_loc = EarthLocation.from_geodetic('-70d24m14.25s', '-24d37m37.36s', (2635.43+13.044)*u.m)
    VST_loc = EarthLocation.from_geodetic('-70d24m14.27s', '-24d37m34.79s', (2635.43+4.5399)*u.m)
    VISTA_loc = EarthLocation.from_geodetic('-70d23m51.36s', '-24d36m56.52s', (2530.)*u.m)

    # https://www.eso.org/sci/facilities/lasilla/telescopes/3p6/overview.html
    ## The telescope is at a geographical location of:
    ## 70° 43' 54.1" W  -29° 15' 39.5" S (WGS84), 2400 metres above sea level
    LS3p6_loc = EarthLocation.from_geodetic('-70d43m54.1s', '-29d15m39.5s', (2400.)*u.m)

    # https://www.eso.org/sci/facilities/lasilla/telescopes/ntt/overview.html
    ## 70° 44' 01.5" W  -29° 15' 32.1" S (WGS84), 2375m
    LSntt_loc = EarthLocation.from_geodetic('-70d44m01.5s', '-29d15m32.1s', (2375.)*u.m)

    # https://www.eso.org/sci/facilities/lasilla/telescopes/national/2p2.html
    # 2p2 70°44'4"543 W 29°15'15"433 S
    LS2p2_loc = EarthLocation.from_geodetic('-70d44m04.543s', '-29d15m15.433s', (2335.)*u.m)

    ## All together as a dictionary:
    telescope_locations={
        'UT1': UT1_loc,
        'UT2': UT2_loc,
        'UT3': UT3_loc,
        'UT4': UT4_loc,
        'VST': VST_loc,
        'VISTA': VISTA_loc,
        'LS3p6': LS3p6_loc,
        'LSntt': LSntt_loc,
        'LS2p2': LS2p2_loc,
    }
except:
    pass
'''
## ToDo: make usd_config module public...
## use local copy (for now) of usd_config.eso_period
# ---------------------------------------------------------------------------------------
def current_ESO_period():
    d=datetime.datetime.utcnow()
    return ((d.year-2012)+44)*2+int(float(d.month+2)/6.)
# ---------------------------------------------------------------------------------------
def ESO_period_start_end_dates(P):
    ESO_period_first_last_dates=[
        ['-10-01','-03-31'],
        ['-04-01','-09-30'],
    ]
    y1=1967+(P+1)//2
    md1=ESO_period_first_last_dates[P%2][0]
    y2=1967+(P+2)//2
    md2=ESO_period_first_last_dates[P%2][1]
    return ["{}{}".format(y1,md1),"{y2}{md2}.format(y2,md2)"]
# ---------------------------------------------------------------------------------------
def ESO_period_start_end_datetimes(P):
    ESO_period_first_last_dates=[
        ['-10-01T12:00:00','-04-01T12:00:00'],
        ['-04-01T12:00:00','-10-01T12:00:00'],
    ]
    y1=1967+(P+1)//2
    md1=ESO_period_first_last_dates[P%2][0]
    y2=1967+(P+2)//2
    md2=ESO_period_first_last_dates[P%2][1]
    return ["{}{}".format(y1,md1),"{y2}{md2}.format(y2,md2)"]
'''
# ---------------------------------------------------------------------------------------
def ESO_period_start_end_dates(P):
    return [
        ESO_period_date_start(P),
        ESO_period_date_end(P),
    ]
# ---------------------------------------------------------------------------------------
def ESO_period_start_end_datetimes(P):
    return [
        ESO_period_datetime_start(P),
        ESO_period_datetime_end(P),
    ]
# ---------------------------------------------------------------------------------------
def get_attrs(klass):
  return [k for k in klass.__dict__.keys()
    if not k.startswith('__')
    and not k.endswith('__')]

# ---------------------------------------------------------------------------------------
# https://gist.github.com/cynici/4084518
'''
optparse offers IndentedHelpFormatter() and TitledHelpFormatter() but they don't honor the newlines embedded in the description string.
author: Tim Chase
source: https://groups.google.com/forum/?fromgroups=#!topic/comp.lang.python/bfbmtUGhW8I
usage: parser = OptionParser(description=help_text, formatter=IndentedHelpFormatterWithNL())
'''

from optparse import OptionParser, IndentedHelpFormatter, textwrap

class IndentedHelpFormatterWithNL(IndentedHelpFormatter):
  def format_description(self, description):
    if not description: return ""
    desc_width = self.width - self.current_indent
    indent = " "*self.current_indent
# the above is still the same
    bits = description.split('\n')
    formatted_bits = [
      textwrap.fill(bit,
        desc_width,
        initial_indent=indent,
        subsequent_indent=indent)
      for bit in bits]
    result = "\n".join(formatted_bits) + "\n"
    return result

  def format_option(self, option):
    # The help for each option consists of two parts:
    #   * the opt strings and metavars
    #   eg. ("-x", or "-fFILENAME, --file=FILENAME")
    #   * the user-supplied help string
    #   eg. ("turn on expert mode", "read data from FILENAME")
    #
    # If possible, we write both of these on the same line:
    #   -x    turn on expert mode
    #
    # But if the opt string list is too long, we put the help
    # string on a second line, indented to the same column it would
    # start in if it fit on the first line.
    #   -fFILENAME, --file=FILENAME
    #       read data from FILENAME
    result = []
    opts = self.option_strings[option]
    opt_width = self.help_position - self.current_indent - 2
    if len(opts) > opt_width:
      opts = "%*s%s\n" % (self.current_indent, "", opts)
      indent_first = self.help_position
    else: # start help on same line as opts
      opts = "%*s%-*s  " % (self.current_indent, "", opt_width, opts)
      indent_first = 0
    result.append(opts)
    if option.help:
      help_text = self.expand_default(option)
# Everything is the same up through here
      help_lines = []
      for para in help_text.split("\n"):
        help_lines.extend(textwrap.wrap(para, self.help_width))
# Everything is the same after here
      result.append("%*s%s\n" % (
        indent_first, "", help_lines[0]))
      result.extend(["%*s%s\n" % (self.help_position, "", line)
        for line in help_lines[1:]])
    elif opts[-1] != "\n":
      result.append("\n")
    return "".join(result)
# ---------------------------------------------------------------------------------------
def rgetFolderIds( api, cIds ):

    ids = []
    for cId in cIds :
        rItems, _ = api.get('/containers/'+str(cId)+'/items')
        logging.debug(rItems)
        for r in rItems :
            if r['itemType'] == 'Folder' :
                logging.debug('Adding %d to folder list' %(r['containerId']))
                ids.extend([r['containerId'],])
                ids.extend(rgetFolderIds(api, [r['containerId'],]))
    return ids
# ---------------------------------------------------------------------------------------
def rgetContainerIds( api, cIds, status=None ):
    ids = []
    for cId in cIds :
        rItems, _ = api.get('/containers/'+str(cId)+'/items')
        logging.debug(rItems)
        for r in rItems :
            if r['itemType'] == 'TimeLink' or r['itemType'] == 'Group' or r['itemType'] == 'Concatenation' :
                if status is None or r['containerStatus'] in list(status) :
                    logging.debug('Adding %d to container list' %(r['containerId']))
                    ids.extend([r['containerId'],])
    return ids
# ---------------------------------------------------------------------------------------
def rgetOBIds( api, cIds, status=None ):
    ids = []
    for cId in cIds :
        logging.debug('Checking container %d' %(cId))
        rItems, _ = api.get('/containers/'+str(cId)+'/items')
        logging.debug(rItems)
        for r in rItems :
            if r['itemType'] == 'OB' or  r['itemType'] == 'CB' :
                if status is None or r['obStatus'] in list(status) :
                    logging.debug('Adding %d to OB list' %(r['obId']))
                    ids.extend([r['obId'],])
    return ids
# ---------------------------------------------------------------------------------------
def r_get_all_OBIds( api, obj_list ) :
    obIds=[]
    for ID in obj_list :
        nID=int(ID)
        logging.info("Processing OB/Container ID = %d" %(nID))
        # The containes and OBs
        try:
            container, containerVersion = api.getContainer(nID)
            fIds = [nID,]
            fIds.extend(rgetFolderIds(api, [nID,]))
            logging.info('================================================================================')
            cIds=rgetContainerIds(api, fIds )
            fcIds = fIds+cIds
            if cIds is not None :
                logging.info("containerId list = %s" %(str(cIds)))
            else :
                logging.error("No containers found")
            logging.info('================================================================================')
            obIds=obIds+rgetOBIds(api, fcIds )
            logging.info("obId list = %s" %(str(obIds)))
            if obIds is None :
                logging.error("No OBs found")

        except p2api.P2Error as e :
            ## Looks like this ID is not a container, assume it is an OB, below...
            obIds.append(nID)
        except:
            raise
    return obIds
# ---------------------------------------------------------------------------------------
def get_api( options ) :
    password_from_keyring = None
    # Login...
    if options.env in ['demo',]:
        user='52052'
        pwstream='tutorial'
    else:
        user=options.user
        ## from astroquery.eso
        # Get password from keyring or prompt
        if options.pwreenter is False:
            password_from_keyring = keyring.get_password(
                "usd_p2api_interactive:www.eso.org", user)

        if password_from_keyring is None:
            #if system_tools.in_ipynb():
            #    log.warning("You may be using an ipython notebook:"
            #                " the password form will appear in your terminal.")
            # see https://pymotw.com/2/getpass/
            if sys.stdin.isatty():
                pwstream = getpass.getpass(user+"@<"+options.env+"> password : ", stream=sys.stderr)
            else:
                pwstream = sys.stdin.readline().rstrip()
        else:
            pwstream = password_from_keyring

    i=0
    api = None
    while api is None and i < 10 :
        try:
            api = p2api.ApiConnection(options.env, user, pwstream)
        except p2api.P2Error as e :
            logging.error(e)
            time.sleep(2)
        except :
            pass
        i+=1
    if api is None :
        logging.error('Ooops, login failed...')
        sys.exit(1)

    ## from astroquery.eso
    # When authenticated, save password in keyring if needed
    if options.env not in ['demo','defidev7',] and password_from_keyring is None and options.pwstore:
        keyring.set_password("usd_p2api_interactive:www.eso.org", user, pwstream)

    return api
# ---------------------------------------------------------------------------------------
def decode_datetime( d ) :
    if d is None :
        return None
    if isinstance(d,datetime.date) :
        return d
    if isinstance(d,datetime.datetime) :
        return d.date()

    # Python can't actually handle TimeZones by name, except the one that
    # time.tzname is currently set to:
    # see https://docs.python.org/3/library/time.html
    # So we replace as needed TZ names (%Z) with the %z format...
    tz_info={
        'UTC': '+0000',
        'CET': '+0100',
        'CEST': '+0200',
    }
    d_tz=d
    for tz in tz_info :
        d_tz=re.sub(
            '{}.format(tz)',
            '{}.format(tz_info[tz])',
            d_tz,
        )
    for s in [d_tz,d] :
        for df in [
            '%a, %d %b %Y %H:%M:%S %z', # 'Wed, 8 Feb 2023 21:43:40 +0000'
            '%A, %d %B %Y at %H:%M %Z', # 'Thursday, 22 February 2024 at 12:00 CET'
            '%A, %d %B %Y at %H:%M %z', # 'Thursday, 22 February 2024 at 12:00 +0100'
            '%d %b %Y',
            '%Y.%m.%d',
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',  # 2023-04-01T16:45:59
            '%Y-%m-%dT%H:%M',     # 2023-04-01T16:45
        ] :
            try :
                dt=datetime.datetime.strptime(s, df)
                return dt
            except :
                pass
    raise Exception("Could not decode date '{}'.".format(d))
# ---------------------------------------------------------------------------------------
