import sys, os, time, re
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

from modify_envfile import get_ec2_addr

REPLACEMENT_RULES = [
        (
            re.compile(r"https?:\/\/.*?\/chp"),
            "{scheme}://{netloc}/chp"
        ),
        (
            re.compile(r"httpx:\/\/.*?\/chp"),
            "httpx://{netloc}/chp"
        ),
        (
            re.compile(r"https?:\/\/.*?\/app.html"),
            "{scheme}://{netloc}/app.html"
        ),
]

PATTERN_GROUPSCOPE = re.compile(r"COPY\s+?\S*?groupscope")

REPLACEMENT_GROUPSCOPE = (
        # special case
        re.compile(r"https?:\/\/.*\S"),
        "{scheme}://{netloc}"
)

def get_outfname(fname):
    abs_fname = os.path.abspath(fname)
    base_fname, head_fname = os.path.split(abs_fname)
    n, ext = os.path.splitext(head_fname)
    return os.path.join(base_fname, "{}_addr_replace.{}".format(n, ext))

def main(args):
    fname = args.fname
    outfname = args.outfname
    if not outfname:
        outfname = get_outfname(fname)
    logger.debug("writing to file: {}...".format(outfname))
    netloc = args.netloc
    if (not netloc) and (args.ec2 is True):
        netloc = get_ec2_addr()
    scheme = "https" if args.ssl is True else "http"
    out_lines = []
    with open(fname, 'r') as f:
        groupscope_flag = False
        for line in f:
            # look for a particular line that comes after "COPY public.groupscope" line
            if groupscope_flag is True:
                # alter this line and reset the flag
                line = re.sub(REPLACEMENT_GROUPSCOPE[0], REPLACEMENT_GROUPSCOPE[1].format(scheme=scheme, netloc=netloc), line)
                # outf.write(line)
                out_lines.append(line)
                groupscope_flag = False
                continue
            if PATTERN_GROUPSCOPE.search(line):
                # found the "COPY public.groupscope" line, act on it in next loop iteration
                # outf.write(line)
                out_lines.append(line)
                groupscope_flag = True
                continue
            for p, r in REPLACEMENT_RULES:
                # do this for every line but the above cases
                # this will do nothing to the line if none of the patterns match
                line = re.sub(p, r.format(scheme=scheme, netloc=netloc), line)
            # outf.write(line)
            out_lines.append(line)
    with open(outfname, 'w') as outf:
        for out_line in out_lines:
            outf.write(out_line)

if __name__ == "__main__":
    total_start = timer()
    logger = logging.getLogger(__name__)
    logger.info(" ".join(sys.argv))
    logger.info( '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) )
    import argparse
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("fname", type=str, help="input filename")
    parser.add_argument("-o", "--outfname", type=str, help="output filename")
    parser.add_argument("--netloc", type=str, help="netloc (public dns. e.g., example.com)")
    parser.add_argument("--ec2", action='store_true', help="if run on an AWS EC2 instance, automatically detect the public DNS of the instance and use that for the netloc")
    parser.add_argument("--ssl", action='store_true', help="use SSL (i.e., https://")
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
