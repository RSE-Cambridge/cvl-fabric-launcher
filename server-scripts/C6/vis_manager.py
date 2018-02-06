#!/usr/bin/python -E
import subprocess
import datetime
import os
import time
import socket
from subprocess import call
import re


def listAll(args):
    submithost = socket.gethostname()
    mX = submithost[:2]
    partition = mX + "-vis-c6"
    username = os.path.expandvars('$USER')
    total_seconds = 0
    cmd = ["/usr/local/slurm/latest/bin/squeue", "--user=" + username, "--partition=" + partition, "-o", "%i %L"]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if not 'JOBID TIME_LEFT' in line:
            jobidstring = line.split(' ')[0]
            timestring = line.replace("-", ":").split(' ')[1]
            # print line
            # print timestring,
            # print len (timestring) # note the string is in the format 1:00:50:16/n
            # for i in range (0,len (timestring)):
            #     print str(i) + " " + timestring[i]
            if len(timestring) >= 10:
                pt = datetime.datetime.strptime(timestring, '%d:%H:%M:%S\n')
                total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600 + pt.day * 86400
            elif len(timestring) >= 7:
                pt = datetime.datetime.strptime(timestring, '%H:%M:%S\n')
                total_seconds = pt.second + pt.minute * 60 + pt.hour * 3600
            elif len(timestring) >= 4:
                pt = datetime.datetime.strptime(timestring, '%M:%S\n')
                total_seconds = pt.second + pt.minute * 60
            elif len(timestring) >= 1:
                pt = datetime.datetime.strptime(timestring, '%S\n')
                total_seconds = pt.second
            print jobidstring + " " + str(total_seconds)
    retval = p.wait()


def newSession(args):
    submithost = socket.gethostname()
    mX = submithost[:2]
    partition = mX + "-vis-c6"
    qos = "vis_" + mX
    vncdir = os.path.expandvars('$HOME/.vnc/')
    cmd = ["mkdir", "-p", vncdir]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()
    # set resolution if requested (Note - there is not error checking at the moment!)
    turbovncserver_conf = os.path.expandvars('$HOME/.vnc/turbovncserver.conf')
    if args.resolution:
        # copy template to users home dir
        cmd = ["cp", "-f", "/usr/local/desktop/turbovncserver.conf", turbovncserver_conf]
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line
        retval = p.wait()
        # update screen resolution
        cmd = ["sed", "-i", "s/VISMANAGERgeometry/$geometry = \"" + args.resolution + "\"/", turbovncserver_conf]
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line
        retval = p.wait()
    # let user know that multinode sessions are for particular tasks
    if args.nodes > 1:
        print "INFO: You have requested more than one vis node. This should only be used rarely for parallel vis jobs e.g. ParaView and XLI Workflow. Applications like MATLAB will not run faster with more nodes and you may prevent others using desktop sessions "

    # TODO: things that will help the user
    #       - if system reserved for outage adjust walltime if too long and inform user
    #       - if high mem busy suggest low mem
    #       = warning if not enough allocation or low allcoation
    #       - warning if overquota

    # start session
    # check if user has a custom sbatch_vis_session script (used for reservations etc)
    if os.path.isfile(os.path.expandvars('$HOME/.vnc/sbatch_vis_session')):
        sbatch_vis_session = os.path.expandvars('$HOME/.vnc/sbatch_vis_session')
    else:
        sbatch_vis_session = "/usr/local/desktop/sbatch_vis_session"

    slurm_out = os.path.expandvars('$HOME/.vnc/slurm-%j.out')

    # set up the cmmand based on flavour requested
    if args.flavour == "any":
        cmd = ["/usr/local/slurm/latest/bin/sbatch", "--qos=" + qos, "--partition=" + partition,
               "--account=" + args.project, \
               "--time=" + str(args.hours) + ":00:00", "--nodes=" + str(args.nodes), \
               "--output=" + slurm_out, "--error=" + slurm_out, sbatch_vis_session]
    elif args.flavour == "highmem":
        cmd = ["/usr/local/slurm/latest/bin/sbatch", "--qos=" + qos, "--partition=" + partition,
               "--account=" + args.project, \
               "--time=" + str(args.hours) + ":00:00", "--nodes=" + str(args.nodes), \
               "--output=" + slurm_out, "--error=" + slurm_out, "--mem=192000", sbatch_vis_session]

    # additional options
    # if account is listed in the beamline reservation use that reservation
    reservationname="beamline"
    reservation_cmd=["/usr/local/slurm/latest/bin/scontrol","show","--oneliner","reservation=" + reservationname]
    p = subprocess.Popen(reservation_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line =  p.stdout.readline()
    reservation_dict = dict( (n,v) for n,v in (a.split('=') for a in line.split() ) )
    retval = p.wait()
    if partition == "m1-vis-c6" and args.project in reservation_dict['Accounts']:
        # print "account found in reservation - inserting reservationname before sbatch script"
        sbatch_vis_session = cmd.pop()
        cmd.append("--reservation=" + reservationname)
        cmd.append(sbatch_vis_session)

    # print cmd
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if 'Submitted batch job' in line:
            print line.split(' ')[3],
        else:
            print "ERROR: " + line
    retval = p.wait()


def isRunning(args):
    cmd = ["/usr/local/slurm/latest/bin/squeue", "-j", args.sessionid, "-o", "%i %t %R"]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if 'JOBID' in line:
            continue
        if args.sessionid in line:
            state = line.split(' ')[1]
            # R = Running
            if state == 'R':
                print "true"
            # CG = Cancelled
            elif state == 'CG':
                continue
            # Jobid no longer exists there for is not running ;)
            elif line == 'slurm_load_jobs error: Invalid job id specified':
                continue
            else:
                print "ERROR: " + line
    retval = p.wait()


def execHost(args):
    cmd = ["/usr/local/slurm/latest/bin/squeue", "-j" + args.sessionid, "-o", "%N"]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if 'NODELIST' in line:
            continue
        nodelist = line.translate(None, '[]')
        firstnode = re.split(r'-|,', nodelist)[0]
        print firstnode
    retval = p.wait()


def vncPort(args):
    slurm_out_dir = os.path.expandvars('$HOME/.vnc/')
    slurm_out = slurm_out_dir + "slurm-" + args.sessionid + ".out"
    cmd = ["grep", "-o", "^:[^\S]", slurm_out]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def stopsession(args):
    cmd = ["/usr/local/slurm/latest/bin/scancel", args.sessionid]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if args.wait:
        time.sleep(args.wait)
    for line in p.stdout.readlines():
        print line,
    retval = p.wait()


def getProjects(args):
    userid = os.path.expandvars('$USER')
    cmd = ["/usr/local/slurm/latest/bin/sshare", "--parsable", "--users=" + userid]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        user = line.split('|')[1]
        if userid.lower() == user:
            project = line.split('|')[0]
            if project.lstrip(' ') == "cvl":
                pass
            else:
                print project.lstrip(' ')
    retval = p.wait()


def showStart(args):
    cmd = ["/usr/local/slurm/latest/bin/scontrol", "show", "job", args.sessionid]
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if 'StartTime' in line:
            if 'StartTime=Unknown' in line:
                StartTime = "Unknown"
            else:
                StartTime = line.split(' ')[3]
                StartTime = StartTime.split('=')[1]
                StartTime = StartTime.split('T')[1] + " " + StartTime.split('T')[0]
            print "StartTime " + StartTime
    retval = p.wait()


def sanityCheck(args):
    print "Running with launcher version: " + args.launcherversion


#    print "INFO: Tuesday 12th Mar - we are currently experiencing issues with the scheduler. Desktop sessions may fail to start. We are working on the issue now"
    # print "INFO: m2-login1 is experiencing issues. If you are unable to login in using m2-login1 please use m2-login2 instead"
# if int(args.launcherversion) < 20150418:
#      print "INFO: " + args.launcherversion

def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    listallSP = subparser.add_parser('listall',
                                     help='lists all the users running vis jobs in the format of "sessionid timeleft (seconds)"')
    listallSP.set_defaults(func=listAll)

    newsessionSP = subparser.add_parser('newsession',
                                        help='create a new desktop session and return an id or error message')
    newsessionSP.set_defaults(func=newSession)
    newsessionSP.add_argument("-p", "--project", required=True,
                              help='the project allocation to run the session against')
    newsessionSP.add_argument("-t", "--hours", type=int, required=True,
                              help='the number of hours the session is to run for')
    newsessionSP.add_argument("-f", "--flavour", default="any", choices=['any', 'highmem'],
                              help='the preferred type of session required (default any, available any,lowmem,highmem)')
    newsessionSP.add_argument("-n", "--nodes", type=int, default=1, help='the number of nodes (default 1)')
    newsessionSP.add_argument("-r", "--resolution", help='sets the display resolution (e.g. 1024x768)')

    isrunningSP = subparser.add_parser('isrunning',
                                       help='test if a vis session has started yet (returns "true" if it is)')
    isrunningSP.set_defaults(func=isRunning)
    isrunningSP.add_argument("-s", "--sessionid", required=True, help='the session id to check')

    exechostSP = subparser.add_parser('exechost',
                                      help='return information about which node a vis session is running on')
    exechostSP.set_defaults(func=execHost)
    exechostSP.add_argument("-s", "--sessionid", required=True, help='the session id to locate')

    vncportSP = subparser.add_parser('vncport', help='return the port on which the vnc server started')
    vncportSP.set_defaults(func=vncPort)
    vncportSP.add_argument("-s", "--sessionid", required=True, help='the session to test')

    stopSP = subparser.add_parser('stop', help='stop a running vis session')
    stopSP.set_defaults(func=stopsession)
    stopSP.add_argument("-s", "--sessionid", required=True, help='the session to stop')
    stopSP.add_argument("-w", "--wait", type=int, help='Wait up to the specified number of seconds before returning')

    getprojectsSP = subparser.add_parser('getprojects', help='list the available projects for running sessions')
    getprojectsSP.set_defaults(func=getProjects)

    showstartSP = subparser.add_parser('showstart', help='get the estimate of when the vis session will start')
    showstartSP.set_defaults(func=showStart)
    showstartSP.add_argument("-s", "--sessionid", required=True, help='the session to check')

    sanitycheckSP = subparser.add_parser('sanitycheck',
                                         help='run a simple sanity check e.g. make sure the user has enough file system space to create files')
    sanitycheckSP.add_argument("-l", "--launcherversion", required=True, help='the session to test')
    sanitycheckSP.set_defaults(func=sanityCheck)

    if (len(sys.argv) < 2):
        args = parser.parse_args(['--help'])
    else:
        args = parser.parse_args()
    if args.func == None:
        sanityCheck(args)
    else:
        args.func(args)


if __name__ == '__main__':
    main()
