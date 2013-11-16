
import argparse
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

def get_args():
    """Parse sys.argv"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--run-name',
                        type=str,
                        default = '',
                        help='ID to apply to run.')

    parser.add_argument('-q', '--queue',
                        type=str,
                        default = '',
                        help='Run to submit job to.')

    parser.add_argument('-n','--nodes',
                        type=int,
                        default=1,
                        help='Number of nodes.')

    parser.add_argument('-p','--ppn',
                        type=int,
                        default=16,
                        help='Number of cores.')

    parser.add_argument('-w','--walltime',
                        type=str,
                        default='01:00:00',
                        help="Allotted Time. Format: 'HH:MM:SS'")

    parser.add_argument('-a','--account',
                        type=str,
                        default='cac100',
                        help='Account to assign minutes to')

    parser.add_argument('-e','--email',
                        type=str,
                        default='ngcrawford@gmail.com',
                        help='Email address.')

    parser.add_argument('cmd',
                        type=str,
                        default='normal',
                        help='Linux command to run.')

    args = parser.parse_args()
    return args


def generate_shscript(args):

    """ Generate sh script input file"""

    header = """#!/bin/bash
    #PBS -q {0}
    #PBS -l nodes={1}:ppn={2}:native
    #PBS -l walltime={3}
    #PBS -N {4}
    #PBS -o {4}.out
    #PBS -e {4}.err
    #PBS -A {5}
    #PBS -M {6}
    #PBS -m abe
    #PBS -V

    """.format(args.queue, args.nodes, args.ppn, args.walltime,
               args.run_name, args.account, args.email)

    f = NamedTemporaryFile(delete=False)
    f.write(header + args.cmd)
    f.seek(0)

    # for i in f:
    #     print i.strip()
    return f.name

def submit_job(shscript_path):
    """Submit the job."""

    cli = "qsub {}".format(shscript_path)
    cli_parts = cli.split()
    ft = Popen(cli_parts, stdin=PIPE, stderr=PIPE, stdout=PIPE).communicate()
    print 'Submitted:', cli

args = get_args()
shscript_path = generate_shscript(args)
submit_job(shscript_path)
