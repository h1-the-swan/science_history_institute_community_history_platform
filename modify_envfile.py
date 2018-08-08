#!/usr/bin/env python3

import sys, os, time
try: 
    from urllib.parse import urlparse
except ImportError:
    from urllib import urlparse
from datetime import datetime
from timeit import default_timer as timer
try:
    from humanfriendly import format_timespan
except ImportError:
    def format_timespan(seconds):
        return "{:.2f} seconds".format(seconds)

import logging
logging.basicConfig(format='%(asctime)s %(name)s.%(lineno)d %(levelname)s : %(message)s',
        datefmt="%H:%M:%S",
        level=logging.INFO)
# logger = logging.getLogger(__name__)
logger = logging.getLogger('__main__').getChild(__name__)

DOTENV_FILENAME = '.env'

RULES = {
    'FRONT_APP_URL': "{scheme}://{netloc}",
    'HYPOTHESIS_SERVICE': "{scheme}://{netloc}",
    'SIDEBAR_APP_URL': "{scheme}://{netloc}/app.html",
    'HYPOTHESIS_CLIENT_URL': "{scheme}://{netloc}/_h_client/hypothesis",
    'WEBSOCKET_URL': "{ws_scheme}://{netloc}/ws",
}

class EnvfileSettings(object):
    def __init__(self, scheme=None, netloc='example.com', ws_scheme=None, ssl=False):
        if ssl is True:
            if not scheme:
                scheme = 'https'
            if not ws_scheme:
                ws_scheme = 'wss'
        self.scheme = scheme or 'http'
        self.netloc = netloc or 'example.com'
        self.ws_scheme = ws_scheme or 'ws'

    def as_dict(self):
        """
        :returns: dict

        """
        return {
            'scheme': self.scheme,
            'netloc': self.netloc,
            'ws_scheme': self.ws_scheme,
        }
        

def change_lines(fname, rules, settings, sep='='):
    out_lines = []
    with open(fname, 'r') as f:
        for line in f:
            linesplit = line.strip().split(sep)
            k = linesplit[0]
            if k in rules:
                v = rules[k].format(**settings.as_dict())
                out_lines.append("{k}{sep}{v}\n".format(k=k, sep=sep, v=v))
            else:
                # copy without changing
                out_lines.append(line)
    return out_lines

def get_ec2_addr():
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
    import requests
    metadata_url = "http://169.254.169.254/latest/meta-data/"
    r = requests.get(metadata_url + 'public-hostname')
    if r.status_code == 200:
        logger.debug("AWS EC2 public hostname: {}".format(r.text))
        return r.text
    else:
        raise RuntimeError("Non-200 status code (code {}) when querying for AWS instance metadata: {}".format(r.status_code, r.text))

def main(args):
    fname = DOTENV_FILENAME
    if args.backup is True:
        from shutil import copyfile
        abs_fname = os.path.abspath(fname)
        fname_split = os.path.split(abs_fname)
        backup_fname = os.path.join(fname_split[0], "backup_{}".format(fname_split[1]))
        logger.debug("creating backup file: {}".format(backup_fname))
        copyfile(abs_fname, backup_fname)
    netloc = args.netloc
    if (not netloc) and (args.ec2 is True):
        netloc = get_ec2_addr()

    settings = EnvfileSettings(netloc=netloc, ssl=args.ssl)

    out_lines = change_lines(fname, RULES, settings)
    logger.debug('Overwriting file {}...'.format(fname))
    with open(fname, 'w') as outf:
        for line in out_lines:
            outf.write(line)


if __name__ == "__main__":
    total_start = timer()
    logger = logging.getLogger(__name__)
    logger.info(" ".join(sys.argv))
    logger.info( '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) )
    import argparse
    parser = argparse.ArgumentParser(description="modify the .env environment variable file for deploying on a remote server")
    parser.add_argument("--backup", action='store_true', help="keep a backup of the original .env file")
    parser.add_argument("--netloc", type=str, help="netloc (public dns. e.g., example.com)")
    parser.add_argument("--ec2", action='store_true', help="if run on an AWS EC2 instance, automatically detect the public DNS of the instance and use that for the netloc")
    parser.add_argument("--ssl", action='store_true', help="use SSL (i.e., https:// and wss://)")
    parser.add_argument("--debug", action='store_true', help="output debugging info")
    global args
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('debug mode is on')
    else:
        logger.setLevel(logging.INFO)
    main(args)
    total_end = timer()
    logger.info('all finished. total time: {}'.format(format_timespan(total_end-total_start)))
