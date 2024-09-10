#! /usr/bin/env python
# -*- coding: utf-8 -*-

# $Id: generate_finding_charts.py 267033 2021-09-16 11:08:57Z jpritcha $
from __future__ import print_function

_VERSION_ = "$Revision: 267033 $"
try:
    from ..p2api import __version__
except:
    from p2api.__about__ import __version__
_VERSION_ = __version__

import sys                            # interaction with Python interpreter
from optparse import OptionParser     # for parsing command line arguments
from optparse import OptionGroup

import logging

import keyring
import datetime
import re

import p2api
import p2api.utils.p2api_utils as p2api_utils

from astropy.time import Time
import numpy as np
from astroplan import Observer
import astropy.units as u

################################################################################
default_eso_period=p2api_utils.current_ESO_period()+1
min_ATI_length=1.*u.hr
################################################################################
class get_options:
  "get command line options"

  def __init__(self, vers="0.0"):
    # define options and arguments
    parser = OptionParser(version="%prog "+vers, formatter=p2api_utils.IndentedHelpFormatterWithNL())

    group = OptionGroup(parser, "Input OB(s)")
    group.add_option(
        "-i", "--ids",
        dest="ids",
        help="""\
List of run, container, folder, and/or OB IDs. \
Note that the ATCs will be applied to all OBs recursively when a \
run, container or folder is specified.
[required]\
""",
        default=None
    )
    parser.add_option_group(group)

    group = OptionGroup(parser, "Specify the Absolute Time Intervals explicity.")
    group.add_option(
        "--ATCs", dest="ATCs",
        help="""\
Underscore separated list of comma separated Absolute Time Constraints \
e.g. yyyy-mm-ddThh:mm,yyyy-mm-ddThh:mm_yyyy-mm-ddThh:mm,yyyy-mm-ddThh:mm{_...}
[optional]\
""",
        default=None
    )
    group.add_option("-f", "--file", dest="file", help="A file with one ATC per line [optional]", default=None)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Specify the Absolute Time Intervals using an orbital ephemeris. This functionality is EXPERIMENTAL, please check carefully!!!")
    group.add_option("-E", "--ephem", dest="ephem", metavar="T0,PERIOD", help="Comma separated list of orbital T0[JD] and period[days] [optional]", default=None)
    group.add_option(
        "--phase_intervals",
        dest="phase_intervals",
        help="""\
Comma separated list of phase intervals e.g. 0.1-0.2,0.305-0.375 [optional].
Remember that ATCs specify the intervals during which the OBs must be started.
This code however interprets the phase intervals as the intervals during which the OB must start AND finish. \
Therefore the ending phase intervals of the ATCs that will be added to the OBs will always be \
less than the phase intervals specified.\
""",
        default=None
    )
    group.add_option("--phase_target", dest="phase_target",  help="Comma separated list of target phase, start_before [mins], min_start_before [mins] e.g. 0.01,120,30 [optional]", default=None)
    group.add_option("--periods", dest="periods", help="Comma separated list of periods, default={} [optional]".format(default_eso_period), default=str(default_eso_period))
    parser.add_option_group(group)

    group = OptionGroup(parser, "Do NOT check ATCs for experimental methods.")
    group.add_option("--NO_checkATCs", dest="NO_checkATCs", help="Do NOT check ATCs for experimental methods.", action="store_true", default=False)
    parser.add_option_group(group)

    group = OptionGroup(parser, "p2 server selection, options and password management")
    group.add_option("--env", dest="env", help="Use the %s environment [optional], default = production" %("|".join(p2api.API_URL.keys())), default='production')
    group.add_option("-u", "--user", dest="user", metavar="USER", help="the User Portal account of the user to use, e.g. ASMITHSONIAN [required for production (not required for demo)]", default=None)
    group.add_option("-S", "--PWstore", dest="pwstore", metavar="PWSTORE", help="Store the password in the keyring, default=False", action="store_true", default=False)
    group.add_option("-R", "--PWreenter", dest="pwreenter", metavar="PWREENTER", help="Reenter the password, thus overriding any PW in the keyring, default=False", action="store_true", default=False)
    group.add_option("-Z", "--PWremove", dest="pwremove", metavar="PWREMOVE", help="Remove any password from the keyring, default=False", action="store_true", default=False)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Verbosity...",
                    "All optional")
    group.add_option("-n", "--dryRun", dest="dryrun", help="Do everything but make any changes to tickets [optional]", action="store_true", default=False)
    group.add_option("-D", "--debug", dest="debug", help="Write out debugging info [optional]", action="store_true", default=False)
    #group.add_option("-v", "--verbose", dest="vbose", help="Write out verbose info [optional]", action="store_true", default=False)
    group.add_option("-q", "--quiet", dest="quiet", help="Write out minimal info [optional]", action="store_true", default=False)
    parser.add_option_group(group)

    # parse arguments
    (options, args) = parser.parse_args()

    if options.ids is None or (
        (
            options.ATCs is None
            and
            options.file is None
            and
            (
                options.ephem is None
                or
                options.periods is None
                or
                options.phase_intervals is None
            )
            and
            (
                options.ephem is None
                or
                options.periods is None
                or
                options.phase_target is None
            )
        )
    ) :
        parser.print_help()
        sys.exit(2)

    self.ids = options.ids
    self.periods = options.periods
    self.ATCs = options.ATCs
    self.file = options.file
    self.ephem = options.ephem
    self.phase_intervals = options.phase_intervals
    self.phase_target = options.phase_target

    self.NO_checkATCs = options.NO_checkATCs

    self.user = options.user
    self.env = options.env
    self.pwstore = options.pwstore
    self.pwreenter = options.pwreenter
    self.pwremove = options.pwremove

    self.debug = options.debug
    self.dryrun = options.dryrun
    self.quiet = options.quiet

    logFMT = "%(asctime)s %(module)15s[%(process)5d] [%(levelname)s] %(message)s"
    logLVL=logging.INFO
    if options.debug:
      logLVL=logging.DEBUG
    if options.quiet:
      logLVL=logging.WARN
    logging.basicConfig(level=logLVL, format=logFMT)

options = get_options(_VERSION_)

# ------------------------------------------------------------------------------
def get_ob_ATCs(telescope=None, ob_info=None, run_info=None) :
    ob_ATCs=[]
    ATCs=None
    check_ATCs=False
    if options.ATCs is not None :
        ATCs=[
            [p2api_utils.decode_datetime(x.split(',')[0]),p2api_utils.decode_datetime(x.split(',')[1])]
            for x in options.ATCs.split('_')
        ]

    elif options.file is not None :
        with open(options.file) as file:
            lines = file.readlines()
            lines = [line.rstrip().lstrip().split(',') for line in lines]
        ATCs=[
            [
                p2api_utils.decode_datetime(x[0])+datetime.timedelta(seconds=30), # rounding to 1min
                p2api_utils.decode_datetime(x[1])+datetime.timedelta(seconds=30), # rounding to 1min
            ] for x in lines
        ]

    elif options.ephem is not None :
        ob_exec_time=ob_info['executionTime']
        T0,P=(float(x) for x in options.ephem.split(','))
        periods=[
            item for sublist in 
            [[y for y in range(int(x.split('-')[0]),int(x.split('-')[-1])+1)] for x in options.periods.split(',')]
            for item in sublist
        ]
        periods.sort()
        period_range=[periods[0],]
        period_ranges=[]
        _pp=periods[0]
        sf_jds=[]
        for _p in periods[1:] :
            if _p > _pp+1 :
                period_range+=[_pp,]
                sf_jd=Time([p2api_utils.ESO_period_start_end_datetimes(ESO_P) for ESO_P in period_range]).jd
                sf_jds+=[[sf_jd[0][0],sf_jd[1][1]],]
                period_ranges+=[period_range,]
                period_range=[_p,]
            _pp=_p
        period_range+=[_pp,]
        sf_jd=Time([p2api_utils.ESO_period_start_end_datetimes(ESO_P) for ESO_P in period_range]).jd
        sf_jds+=[[sf_jd[0][0],sf_jd[1][1]],]
        period_ranges+=[period_range,]

        post_ob_exec_time=0.
        if options.phase_intervals is not None :
            phase_intervals=[[float(y) for y in x.split('-')] for x in options.phase_intervals.split(',')]
            min_start_before=0.
        elif options.phase_target is not None :
            phase_target,start_before,min_start_before=(float(x) for x in options.phase_target.split(','))
            phase_intervals=[[phase_target-start_before/P/24./60.,phase_target],]
            post_ob_exec_time=ob_exec_time
            ob_exec_time=0.
        else :
            logging.error('No means to calculate phase intervals specified.')

        checked_phase_intervals=[]
        for p_int in phase_intervals :
            if p_int[1] < p_int[0] :
                p_int[0]=p_int[0]-1.
            p_int_in_sec=(p_int[1]-p_int[0])*P*24.*60.*60.
            if (
                ob_exec_time < p_int_in_sec
                and
                p_int_in_sec > min_ATI_length.to_value(u.second)
            ) :
                checked_phase_intervals+=[p_int,]
            else :
                if ob_exec_time < p_int_in_sec :
                    logging.warning(
                        'Phase interval {}--{} == {:3.1f}sec is too short to start and finish this OB with execution time of {}secs.'.format(
                            p_int[0],
                            p_int[1],
                            p_int_in_sec,
                            ob_exec_time,
                        )
                    )
                if p_int_in_sec > min_ATI_length.to_value(u.second) :
                    logging.warning(
                        'Phase interval {}--{} == {:3.1f}sec is shorter than the minimum ATI length time of {}secs.'.format(
                            p_int[0],
                            p_int[1],
                            p_int_in_sec,
                            min_ATI_length.to_value(u.second),
                        )
                    )

        sf_ints=[]
        for sf_jd in sf_jds :
            orbits=(np.array(sf_jd)-T0)//P
            for o in range(int(orbits[0])-1,int(orbits[1])+1) :
                for p_int in checked_phase_intervals :
                    sf_int=[
                        T0+(o+p_int[0])*P,
                        T0+(o+p_int[1])*P-ob_exec_time/24./60./60.,
                    ]
                    if (
                        ( sf_int[0] > sf_jd[0] and sf_int[0] < sf_jd[1] )
                        or
                        ( sf_int[1] > sf_jd[0] and sf_int[1] < sf_jd[1] )
                    ) :
                        # Interval is within the time range of the specified period(s)...
                        original_sf_int=sf_int
                        int_spans_nighttime=True
                        if sf_int[1] - sf_int[0] < 1. :
                            sssr=[]
                            # Check that some part of the interval occurs during nighttime...
                            int_spans_nighttime=False
                            for which in ['previous','next',] :
                                sun_set_time=telescope.sun_set_time(Time(sf_int[0], format='jd'), which=which)
                                if isinstance(sun_set_time.value,np.float64) :
                                    sun_rise_time=telescope.sun_rise_time(sun_set_time, which='next')
                                    sssr+=[[sun_set_time,sun_rise_time],]
                                    if (
                                        (sf_int[0] > sun_set_time.jd and sf_int[0] < sun_rise_time.jd-ob_exec_time/24./60./60. )
                                        or
                                        (sf_int[1] > sun_set_time.jd and sf_int[1] < sun_rise_time.jd-ob_exec_time/24./60./60. )
                                        or
                                        (sf_int[0] < sun_set_time.jd and sf_int[1] > sun_rise_time.jd-ob_exec_time/24./60./60. )
                                    ) :
                                        sf_int=[
                                            np.max([sf_int[0],sun_set_time.jd]),
                                            np.min([sf_int[1],sun_rise_time.jd-ob_exec_time/24./60./60.,sun_rise_time.jd-post_ob_exec_time/24./60./60.]),
                                        ]
                                        if sf_int[1] > sf_int[0]+min_start_before/24./60. :
                                            int_spans_nighttime=True                                    
                                            break
                                else :
                                    logging.error(f"telescope.sun_set_time(Time({sf_int[0]}, format='jd'), which={which}) did not return np.float64 ")
                        if (
                            int_spans_nighttime
                            and
                            ((sf_int[1]-sf_int[0])*24*60.*60. > ob_exec_time)
                            and
                            (sf_int[1]-sf_int[0])*24*60.*60. > min_ATI_length.to_value(u.second)
                        ) :
                            sf_ints+=[sf_int,]
                        else :
                            if not int_spans_nighttime :
                                logging.debug(
                                    'Interval does not span any part of the night, original interval = {}, SSSR of previous and next nights {}--{} and {}--{}'.format(
                                        original_sf_int,
                                        sssr[0][0].jd,
                                        sssr[0][1].jd,
                                        sssr[1][0].jd,
                                        sssr[1][1].jd,
                                    )
                                )
                            if ((sf_int[1]-sf_int[0])*24*60.*60. < ob_exec_time) :
                                logging.debug(
                                    'Checked Interval shorter [{:3.1f}sec] than OB execution time [{:3.1f}sec], original interval = {}, checked interval = {}'.format(
                                        (sf_int[1]-sf_int[0])*24*60.*60.,
                                        ob_exec_time,
                                        original_sf_int,
                                        sf_int,
                                    )
                                )
                            if ((sf_int[1]-sf_int[0])*24*60.*60. < min_ATI_length.to_value(u.second)) :
                                logging.debug(
                                    'Checked Interval shorter [{:3.1f}sec] than minimum ATI length time [{:3.1f}sec], original interval = {}, checked interval = {}'.format(
                                        (sf_int[1]-sf_int[0])*24*60.*60.,
                                        min_ATI_length.to_value(u.second),
                                        original_sf_int,
                                        sf_int,
                                    )
                                )
                pass
        ATCs=[Time(sf_int, format='jd') for sf_int in sf_ints]
        check_ATCs=True
    else :
        raise "Don't know how to compute Absolute Time Constraints."
 
    ob_ATCs=[]
    for i,ATC in enumerate(ATCs) :
        t=Time(ATC)
        t.format = 'isot'
        t.out_subfmt = 'date_hm'
        ob_ATCs+=[{
            'from': t[0].isot,
            'to':   t[1].isot,
        },]
        if check_ATCs :
            phase_range=''
            if options.ephem is not None :
                phase_range="  [Phases: {:5.3f} -- {:5.3f}]".format(
                    (((t[0]-Time(T0,format='jd'))/P).to_value(u.day)%1),
                    (((t[1]-Time(T0,format='jd'))/P).to_value(u.day)%1),
                )
            print("{:3d} {} -- {}  [OB_exectime={}, Int.duration={}]{}".format(
                i+1,
                ob_ATCs[-1]['from'],
                ob_ATCs[-1]['to'],
                datetime.timedelta(seconds=ob_exec_time),
                ((t[1]-t[0]).to_datetime()),
                phase_range,
            ))
    if check_ATCs :
        '''
        logging.warning("****************************************************************************************")
        logging.warning("****************************************************************************************")
        logging.warning("****************************************************************************************")
        logging.warning("Intervals via Orbital Ephemeris functionality is EXPERIMENTAL")
        logging.warning("Please check the above intervals carefully and only continue if you are sure they are what YOU require.")
        logging.warning("YOU, and YOU ALONE are responsible for the accuracy of these inetervals.")
        '''
        print("****************************************************************************************")
        print("****************************************************************************************")
        print("****************************************************************************************")
        print("Intervals via Orbital Ephemeris functionality is EXPERIMENTAL")
        print("Please check the above intervals carefully and only continue if you are sure they are what YOU require.")
        print("Remember that ATCs specify the intervals during which the OBs must be started.")
        print("While this code interprets the phase intervals as the intervals during which the OB must start AND finish.")
        print("Therefore the ending phase intervals of the ATCs listed above will always be")
        print("less than the phase intervals specified.")
        print("Ultimately YOU, and YOU ALONE, are responsible for the accuracy of these intervals.")
        if not options.NO_checkATCs :
            yorn = input("Continue [y/N] ")
            if yorn.lower() not in ['y',] :
                print("Please contact ESO User Support via a ticket at https://support.eso.org/tickets")
                print("to report/discuss the errors/problems in the above calculations.")
                print("Please include in the description the EXACT command line used to run the script.")
                sys.exit(0)
                #raise Exception("Aborted.")
    return ob_ATCs
# ------------------------------------------------------------------------------
def oneOB( api, obId ) :
    try :
        OB, _  = api.getOB(obId)
    except p2api.P2Error as e :
        ## Looks like this ID is not an OB...
        logging.error('OB %d could not be found...' %(obId))
        return
    except:
        raise
    ob_info = api.executionTime(obId)
    run_info,_=api.getRun(OB['runId'])

    telescope = Observer(location=p2api_utils.telescope_locations[run_info['telescope']])

    if OB['itemType'] not in ['OB',] :
        logging.warning('OB %d is not a science OB' %(obId))
        return

    if OB['obStatus'] not in ['P','-'] :
        logging.warning('OB status is %s, OB not modifiable' %(OB['obstatus']))
        return

    runId, _ = api.getRun(OB['runId'])
    ob_url=api.apiUrl+'/obsBlocks/'+str(obId)
    oneOB_sdt=datetime.datetime.now()
    ## For the moment only setting is supported,
    ## ToDo: implement support for adding to...
    logging.info("Setting Absolute Time Intervals for OBid = %d, OBname = '%s' @ %s..." % (OB['obId'],OB['name'],OB['instrument']))
    absTCs, atcVersion = api.getAbsoluteTimeConstraints(obId)

    ob_ATCs=get_ob_ATCs(
        telescope=telescope,
        ob_info=ob_info,
        run_info=run_info,
    )

    if not options.dryrun :
        api.saveAbsoluteTimeConstraints(
            obId,
            ob_ATCs,
            atcVersion,
        )
    oneOB_edt=datetime.datetime.now()
    logging.info(
        "Added %d Absolute Time Intervals for OBid = %d, OBname = '%s' @ %s done in %s."
        %(
            len(ob_ATCs), obId, OB['name'], OB['instrument'], str(oneOB_edt-oneOB_sdt)
        )
    )
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def main():

    ################################################################################
    # remove password from keyring...
    if options.pwremove and options.user is not None :
        keyring.delete_password('usd_p2api_interactive:www.eso.org', options.user)
        sys.exit(0)

    api=p2api_utils.get_api(options)
    obIds=p2api_utils.r_get_all_OBIds( api, options.ids.split(',') )

    if len(obIds) > 0 :
        if len(obIds) > 1 :
            sdt=datetime.datetime.now()
            logging.warning('Adding Absolute Time Constraints to %d OBs...' %( len(obIds) ))
        for obId in obIds :
            oneOB(api, obId, )
        if len(obIds) > 1 :
            edt=datetime.datetime.now()
            logging.info('Total elapsed time to process %d finding charts %s...' %(len(obIds),str(edt-sdt)))
    else :
        logging.error('No OBs found.')


if __name__ == '__main__' :
    main()
