#! /usr/bin/env python
# -*- coding: utf-8 -*-

# $Id: generate_finding_charts.py 267033 2021-09-16 11:08:57Z jpritcha $
from __future__ import print_function

_VERSION_ = "$Revision: 267033 $"
from ..p2api import __version__
_VERSION_ = __version__

import sys                            # interaction with Python interpreter
from optparse import OptionParser     # for parsing command line arguments
from optparse import OptionGroup

import logging

import keyring
import datetime
import json
import requests

import p2api
import p2api.utils.p2api_utils as p2api_utils
################################################################################

################################################################################
class get_options:
  "get command line options"

  def __init__(self, vers="0.0"):
    # define options and arguments
    parser = OptionParser(version="%prog "+vers, formatter=p2api_utils.IndentedHelpFormatterWithNL())

    group = OptionGroup(parser, "Input OB(s)")
    group.add_option("-i", "--ids", dest="ids", metavar="Ids", help="List of OB IDs [required]", default=None)
    group.add_option("--obsdate", dest="obsdate", metavar="OBS_DATE", help="Set the obsdate [optional]", default=None)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Image display parameters",
"""\
The following parameters affect the way the 'default' images are displayed in the FCs.
They correspond directly to the corresponding parameters of the APLPY FITSFigure.show_grayscale method, see:
  https://aplpy.readthedocs.io/en/stable/api/aplpy.FITSFigure.html#aplpy.FITSFigure.show_grayscale
for details.
"""
    )
    group.add_option("--pmax", dest="pmax", metavar="PMAX", help="pmax to apply to the display of first FC [optional]", type='float', default=None)
    group.add_option("--pmin", dest="pmin", metavar="PMIN", help="pmin to apply to the display of first FC [optional]", type='float', default=None)
    group.add_option("--stretch", dest="stretch", metavar="STRETCH", help="Stretch to apply to the display of first FC [optional]\n", default=None)
    group.add_option("--exponent", dest="exponent", metavar="EXPONENT", help="Exponent if stretch='power' [optional]\n", default=None)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Custom Image/Survey",
"""\
The following parameters affect the way the 'default' images are displayed in the FCs.
They correspond directly to the corresponding parameters without 'c_' prefixes of the APLPY FITSFigure.show_grayscale method, see:
  https://aplpy.readthedocs.io/en/stable/api/aplpy.FITSFigure.html#aplpy.FITSFigure.show_grayscale
for details.
"""
    )
    group.add_option("--survey", dest="survey", metavar="SURVEY", help="An alternative SkyView survey to use. Use --supported_surveys to see which surveys are supported. [optional]", default=None)
    group.add_option("--bkg_image", dest="bkg_image", metavar="BK_IMAGE", help="A custom background image to use [optional]", default=None)
    group.add_option("--bkg_lam", dest="bkg_lam", metavar="BK_LAM", help="Description of the WL coverage of the custom background image/survey [optional]", default=None)
    group.add_option("--c_pmax", dest="c_pmax", metavar="PMAX", help="pmax to apply to the display of first FC [optional]", type='float', default=None)
    group.add_option("--c_pmin", dest="c_pmin", metavar="PMIN", help="pmin to apply to the display of first FC [optional]", type='float', default=None)
    group.add_option("--c_stretch", dest="c_stretch", metavar="STRETCH", help="Stretch to apply to the display of first FC [optional]\n", default=None)
    group.add_option("--c_exponent", dest="c_exponent", metavar="EXPONENT", help="Exponent if stretch='power' [optional]\n", default=None)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Gaia pseudo images parameters",
        "The following parameters affect the way the Gaia pseudo images (if any) are constructed."
    )
    group.add_option("--GAIA_im_IQ", dest="GAIA_im_IQ", metavar="FWHM",
        help="FWHM to use for any Gaia images that will be generated [optional]",
        type='float',
        default=None
    )
    group.add_option("--GAIA_im_noise", dest="GAIA_im_noise", metavar="NOISE",
        help=
"""\
GAIA_im_noise is a dimensionless factor, with the noise computed via the numpy method random.normal(loc,scale) with loc=0.0 and:
    scale=GAIA_im_noise*<brightest_flux_value>
with <brightest_flux_value> being the maximum pixel value in the noiseless pseudo image.
The default value is (as at 2020-01): 1e-6
Together with pmin and pmax this parameter gives (some) control over the relative appearance of stars of different brightness, and can thus be helpful to (for example) highlight faint, but not insignificant, field star(s).
[optional] default=1e-6
""",
        type='float', default=None
    )
    group.add_option("--c_GAIA_im_IQ", dest="c_GAIA_im_IQ", metavar="FWHM",
        help="Same as --GAIA_im_IQ but for any Gaia pseudo images associated with the custom FC.",
        type='float',
        default=None
    )
    group.add_option("--c_GAIA_im_noise", dest="c_GAIA_im_noise", metavar="NOISE",
        help="Same as --GAIA_im_noise but for any Gaia pseudo images associated with the custom FC.",
        type='float',
        default=None
    )
    parser.add_option_group(group)

    group = OptionGroup(parser, "p2 server selection, options and password management")
    group.add_option("--env", dest="env", help="Use the %s environment [optional], default = production" %("|".join(p2api.API_URL.keys())), default='production')
    group.add_option("-u", "--user", dest="user", metavar="USER", help="the User Portal account of the user to use, e.g. ASMITHSONIAN [required for production (not required for demo)]", default=None)
    group.add_option("-S", "--PWstore", dest="pwstore", metavar="PWSTORE", help="Store the password in the keyring, default=False", action="store_true", default=False)
    group.add_option("-R", "--PWreenter", dest="pwreenter", metavar="PWREENTER", help="Reenter the password, thus overriding any PW in the keyring, default=False", action="store_true", default=False)
    group.add_option("-Z", "--PWremove", dest="pwremove", metavar="PWREMOVE", help="Remove any password from the keyring, default=False", action="store_true", default=False)
    parser.add_option_group(group)

    group = OptionGroup(parser, "help...")
    group.add_option("--supported_surveys", dest="supSurs", metavar="Ids", help="Report the list of supported surveys",  action="store_true", default=False)
    parser.add_option_group(group)

    group = OptionGroup(parser, "Verbosity...",
                    "All optional")
    group.add_option("-D", "--debug", dest="debug", help="Write out debugging info [optional]", action="store_true", default=False)
    #group.add_option("-v", "--verbose", dest="vbose", help="Write out verbose info [optional]", action="store_true", default=False)
    group.add_option("-q", "--quiet", dest="quiet", help="Write out minimal info [optional]", action="store_true", default=False)
    parser.add_option_group(group)

    # parse arguments
    (options, args) = parser.parse_args()

    if not options.ids and not options.supSurs :
        parser.print_help()
        sys.exit(2)

    self.ids = options.ids
    self.obsdate = options.obsdate

    self.pmin = options.pmin
    self.pmax = options.pmax
    self.stretch = options.stretch
    self.exponent = options.exponent
    self.GAIA_im_IQ = options.GAIA_im_IQ
    self.GAIA_im_noise = options.GAIA_im_noise

    self.survey = options.survey
    self.bkg_image = options.bkg_image
    self.bkg_lam = options.bkg_lam
    self.c_pmin = options.c_pmin
    self.c_pmax = options.c_pmax
    self.c_stretch = options.c_stretch
    self.c_exponent = options.c_exponent
    self.c_GAIA_im_IQ = options.c_GAIA_im_IQ
    self.c_GAIA_im_noise = options.c_GAIA_im_noise

    self.user = options.user
    self.env = options.env
    self.pwstore = options.pwstore
    self.pwreenter = options.pwreenter
    self.pwremove = options.pwremove

    self.supSurs = options.supSurs

    self.debug = options.debug
    #self.vbose = options.vbose
    self.quiet = options.quiet

    logFMT = "%(asctime)s %(module)15s[%(process)5d] [%(levelname)s] %(message)s"
    logLVL=logging.INFO
    #if options.vbose:
    #  logLVL=logging.INFO
    if options.debug:
      logLVL=logging.DEBUG
    if options.quiet:
      logLVL=logging.WARN
    logging.basicConfig(level=logLVL, format=logFMT)

options = get_options(_VERSION_)
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
    
    if OB['itemType'] not in ['OB',] :
        logging.warning('OB %d is not a science OB' %(obId))
        return

    if OB['obStatus'] not in ['P','-'] :
        logging.warning('OB status is %s, OB not modifiable' %(OB['obstatus']))
        return

    runId, _ = api.getRun(OB['runId'])
    ob_url=api.apiUrl+'/obsBlocks/'+str(obId)
    oneOB_sdt=datetime.datetime.now()
    logging.info("Creating finding charts for OBid = %d, OBname = '%s' @ %s..." % (OB['obId'],OB['name'],OB['instrument']))
    data = api.generateFindingChart(
        obId,
        obs_date=options.obsdate,
        stretch=options.stretch,
        exponent=options.exponent,
        pmin=options.pmin,
        pmax=options.pmax,
        GAIA_im_IQ=options.GAIA_im_IQ,
        GAIA_im_noise=options.GAIA_im_noise,
        survey=options.survey,
        bkg_image=options.bkg_image,
        bkg_lam=options.bkg_lam,
        c_stretch=options.c_stretch,
        c_exponent=options.c_exponent,
        c_pmin=options.c_pmin,
        c_pmax=options.c_pmax,
        c_GAIA_im_IQ=options.c_GAIA_im_IQ,
        c_GAIA_im_noise=options.c_GAIA_im_noise,
    )
    oneOB_edt=datetime.datetime.now()
    logging.info("Finding chart for OBid = %d, OBname = '%s' @ %s done in %s." % (obId, OB['name'], OB['instrument'], str(oneOB_edt-oneOB_sdt)))
    if data is not None :
        try :
            jwarn=json.loads(r.content.decode('utf-8'))
            if 'warnings' in jwarn.keys() :
                logging.warning(jwarn['warnings'])
        except :
            pass
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def main():

    ################################################################################
    # remove passowrd from keyring...
    if options.pwremove and options.user is not None :
        keyring.delete_password('usd_p2api_interactive:www.eso.org', options.user)
        sys.exit(0)
    
    ################################################################################
    if options.supSurs :
        r = requests.get('%s/supported_surveys' %(p2api.P2FC_URL[options.env]))
        if r.status_code in [200,201,204] :
            print(r.text)
        else:
            raise(r.text)
        sys.exit(0)

    #login to the API
    api=p2api_utils.get_api(options)
    obIds=p2api_utils.r_get_all_OBIds( api, options.ids.split(',') )

    if len(obIds) > 0 :
        if len(obIds) > 1 :
            sdt=datetime.datetime.now()
            logging.warning('Submitting %d OBs for FC generation...' %( len(obIds) ))
        for obId in obIds :
            oneOB(api, obId)
        if len(obIds) > 1 :
            edt=datetime.datetime.now()
            logging.info('Total elapsed time to process %d finding charts %s...' %(len(obIds),str(edt-sdt)))
    else :
        logging.error('No OBs found.')

if __name__ == '__main__' :
    main()
