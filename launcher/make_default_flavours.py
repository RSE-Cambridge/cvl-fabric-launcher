import re
import siteConfig
import sys
import collections


class sshKeyDistDisplayStringsNCI(siteConfig.sshKeyDistDisplayStrings):
    def __init__(self):
        super(sshKeyDistDisplayStringsNCI, self).__init__()
        self.passwdPrompt="""Please enter the password for your NCI account."""
        self.passwdPromptIncorrect="Sorry, that password was incorrect.\n"+self.passwdPrompt
        self.passphrasePrompt="Please enter the passphrase for your SSH key"
        self.passphrasePromptIncorrect="""Sorry, that passphrase was incorrect.
Please enter the passphrase for you SSH Key
If you have forgoten the passphrase for you key, you may need to delete it and create a new key.
You can find this option under the Identity menu.
"""
        self.newPassphrase="""It looks like this is the first time you're using Strudel on this
computer. To use ssh key authentication, Strudel will generate a local
passphrase protected key on your computer which is used to
authenticate you to the NCI computers.

Please enter a new passphrase (twice to avoid typos) to protect your local key. 
After you've done this, your passphrase will be the primary method of
authentication for the launcher."""
        self.newPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden."
        self.newPassphraseTooShort="Sorry, the passphrase must be at least six characters.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseTooShort="Passphrase is too short."
        self.newPassphraseMismatch="Sorry, the two passphrases you entered don't match.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseMismatch="Passphrases don't match!"
        self.newPassphraseTitle="Please enter a new passphrase"
        self.persistentMessage="Would you like to leave your current session running so that you can reconnect later?"
        self.reconnectMessage="An Existing Desktop was found. Would you like to reconnect or kill it and start a new desktop?"


class sshKeyDistDisplayStringsCVL(siteConfig.sshKeyDistDisplayStrings):
    def __init__(self):
        super(sshKeyDistDisplayStringsCVL, self).__init__()
        self.passwdPrompt="""Please enter the password for your CVL account.
This is the password you entered when you requested an account
at the website https://m2-web.massive.org.au/users"""
        self.passwdPromptIncorrect="Sorry, that password was incorrect.\n"+self.passwdPrompt
        self.passphrasePrompt="Please enter the passphrase for your SSH key"
        self.passphrasePromptIncorrect="""Sorry, that passphrase was incorrect.
Please enter the passphrase for you SSH Key
If you have forgoten the passphrase for you key, you may need to delete it and create a new key.
You can find this option under the Identity menu.
"""
        self.newPassphrase="""It looks like this is the first time you're using the CVL on this
computer. To use the CVL, the launcher will generate a local
passphrase protected key on your computer which is used to
authenticate you and set up your remote CVL environment.

Please enter a new passphrase (twice to avoid typos) to protect your local key. 
After you've done this, your passphrase will be the primary method of
authentication for the launcher.

WHY?

This new method of authentication allows you to create file system
mounts to remote computer systems, and in the future it will support
launching remote HPC jobs."""
        self.newPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden."
        self.newPassphraseTooShort="Sorry, the passphrase must be at least six characters.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseTooShort="Passphrase is too short."
        self.newPassphraseMismatch="Sorry, the two passphrases you entered don't match.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseMismatch="Passphrases don't match!"
        self.newPassphraseTitle="Please enter a new passphrase"
        self.persistentMessage="Would you like to leave your current session running so that you can reconnect later?"
        self.reconnectMessage="An Existing Desktop was found. Would you like to reconnect or kill it and start a new desktop?"

class sshKeyDistDisplayStringsMASSIVE(siteConfig.sshKeyDistDisplayStrings):
    def __init__(self):
        super(sshKeyDistDisplayStringsMASSIVE, self).__init__()
        self.passwdPrompt="""Please enter the password for your MASSIVE account."""
        self.passwdPromptIncorrect="Sorry, that password was incorrect.\n"+self.passwdPrompt
        self.passphrasePrompt="Please enter the passphrase for your SSH key"
        self.passphrasePromptIncorrect="""
Sorry, that passphrase was incorrect.
Please enter the passphrase for you SSH Key
If you have forgoten the passphrase for you key, you may need to delete it and create a new key.
You can find this option under the Identity menu.
"""
        self.newPassphrase="""It looks like this is the first time you're logging in to MASSIVE with this version of the launcher.
To make logging in faster and more secure, the launcher will generate a local
passphrase protected key on your computer which is used to
authenticate you and set up your MASSIVE desktop.

Please enter a new passphrase (twice to avoid typos) to protect your local key. 
After you've done this, your passphrase will be the primary method of
authentication for the launcher."""

        self.newPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseEmptyForbidden="Sorry, empty passphrases are forbidden."
        self.newPassphraseTooShort="Sorry, the passphrase must be at least 6 characters.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseTooShort="Passphrase is too short."
        self.newPassphraseMismatch="Sorry, the two passphrases you entered don't match.\n"+self.newPassphrase
        self.createNewKeyDialogNewPassphraseMismatch="Passphrases don't match!"
        self.newPassphraseTitle="Please enter a new passphrase"


class sshKeyDistDisplayStringsCQU(siteConfig.sshKeyDistDisplayStrings):
    def __init__(self):
        super(sshKeyDistDisplayStringsCQU, self).__init__()
        self.passwdPrompt="""Please enter the password for your CQU account."""
        self.passwdPromptIncorrect="Sorry, that password was incorrect.\n"+self.passwdPrompt

        self.persistentMessage="Would you like to leave your current session running so that you can reconnect later?"
        self.reconnectMessage="An Existing Desktop was found. Would you like to reconnect or kill it and start a new desktop?"

class sshKeyDistDisplayStringsBMRI(siteConfig.sshKeyDistDisplayStrings):
    def __init__(self):
        super(sshKeyDistDisplayStringsBMRI, self).__init__()
        self.passwdPrompt="""Please enter the password for your BMRI account."""
        self.passwdPromptIncorrect="Sorry, that password was incorrect.\n"+self.passwdPrompt

        self.persistentMessage="Would you like to leave your current session running so that you can reconnect later?"
        self.reconnectMessage="An Existing Desktop was found. Would you like to reconnect or kill it and start a new desktop?"




def getMassiveSiteConfig(loginHost):
    massivevisible={}
    massivevisible['usernamePanel']=True
    massivevisible['projectPanel']=True
    massivevisible['resourcePanel']=True
    massivevisible['resolutionPanel']='Advanced'
    massivevisible['cipherPanel']='Advanced'
    massivevisible['debugCheckBoxPanel']='Advanced'
    massivevisible['advancedCheckBoxPanel']=True
    massivevisible['label_hours']=True
    massivevisible['jobParams_hours']=True
    massivevisible['label_nodes']=True
    massivevisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    c.defaults['jobParams_ppn']=12
    c.defaults['jobParams_nodes']=1
    c.defaults['jobParams_hours']=4
    c.defaults['jobParams_mem']=48
    c.visibility=massivevisible
    displayStrings=sshKeyDistDisplayStringsMASSIVE()
    c.displayStrings.__dict__.update(displayStrings.__dict__)
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    c.loginHost=loginHost
    cmd = '\"module load xmlstarlet ; qstat -x | xml sel -t -m \\"/Data/Job[starts-with(Job_Owner/text(),\'{username}@\') and starts-with(Job_Name/text(),\'desktop\') and job_state/text()!=\'C\']\\" -v \\" concat(./Job_Id/text(),\' \',./Walltime/Remaining/text())  \\" -n - 2>/dev/null\"'
    regex='(?P<jobid>(?P<jobidNumber>[0-9]+).\S+) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)
    cmd='\"module load pbs ; module load maui ; qstat -f {jobidNumber} -x\"'
    regex='.*<job_state>R</job_state>.*'
    c.running = siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\'qdel -a {jobidNumber}\'')
    c.stopForRestart=siteConfig.cmdRegEx('qdel {jobidNumber} ; sleep 5\'')
    cmd='\"module load xmlstarlet ; qstat -x -f {jobid} | xml sel -t -m \\"/Data/Job/exec_host/text()\\" -c \\".\\" -n - | cut -f 1 -d \\"/\\"\"'
    regex='(?P<execHost>\S+)'
    c.execHost=siteConfig.cmdRegEx(cmd,regex)
    c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/request_visnode.sh {project} {hours} {nodes} True False False {resolution}\'","^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$")
    c.runSanityCheck=siteConfig.cmdRegEx("\'/usr/local/desktop/sanity_check.sh {launcher_version_number}\'")
    #c.getProjects=siteConfig.cmdRegEx('\"glsproject -A -q | grep \',{username},\|\s{username},\|,{username}\s\|\s{username}\s\' \"','^(?P<group>\S+)\s+.*$')
    c.getProjects=siteConfig.cmdRegEx('\"/usr/local/bin/glsproject_timeout -A -q | grep -P \'[,\s]{username}[,\s]\' \"','^(?P<group>\S+)\s+.*$')
    c.showStart=siteConfig.cmdRegEx("showstart {jobid}","Estimated Rsv based start .*?on (?P<estimatedStart>.*)")
    c.vncDisplay= siteConfig.cmdRegEx('"/usr/bin/ssh {execHost} \' module load turbovnc ; vncserver -list\'"','^(?P<vncDisplay>:[0-9]+)\s*(?P<vncPID>[0-9]+)\s*$')
    c.otp= siteConfig.cmdRegEx('"/usr/bin/ssh {execHost} \' module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\'"','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -l {username} {loginHost} \"/usr/bin/ssh -A {execHost} \\"echo agent_hello; bash \\"\"','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"echo DBUS_SESSION_BUS_ADDRESS=dummy_dbus_session_bus_address"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/bin/ssh {execHost} /usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='echo Mounting WebDAV...' # For CentOS 5 / KDE, we are not really "mounting", just displaying the WebDAV share in Konqueror.
    c.webDavMount=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/bin/konqueror webdav://{localUsername}:{vncPasswd}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    # The Window ID is not needed for MASSIVE.  We use the server-side script: /usr/local/desktop/close_webdav_window.sh which figures out which window to close.
    cmd='"echo DummyWebDavWindowID=-1"'
    regex='^DummyWebDavWindowID=(?P<webDavWindowID>.*)$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd='"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Konqueror with the URL:%sbr%s\\nwebdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}%sbr%s\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt;\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop = siteConfig.cmdRegEx(cmd)

    # Chris trying to avoid using the intermediate port:
    #cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {execHost}:{remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"'

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {intermediateWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "ssh -R {remoteWebDavPortNumber}:localhost:{intermediateWebDavPortNumber} {execHost} \'echo tunnel_hello; bash\'"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd = 'echo hello'
    regex = 'hello'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/local/desktop/close_webdav_window.sh webdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)

    return c

def getM3Config(loginHost,flavour=None):
# usage: vis_manager.py [-h]
#
#                       {showstart,isrunning,vncport,newsession,stop,sanitycheck,getprojects,exechost,listall}
#                       ...
#
# positional arguments:
#   {showstart,isrunning,vncport,newsession,stop,sanitycheck,getprojects,exechost,listall}
#     listall             lists all the users running vis jobs in the format of
#                         "sessionid timeleft (seconds)"
#     newsession          create a new desktop session and return an id or error
#                         message
#     isrunning           test if a vis session has started yet (returns "true"
#                         if it is)
#     exechost            return information about which node a vis session is
#                         running on
#     vncport             return the port on which the vnc server started
#     stop                stop a running vis session
#     getprojects         list the available projects for running sessions
#     showstart           get the estimate of when the vis session will start
#     sanitycheck         run a simple sanity check e.g. make sure the user has
#                         enough file system space to create files
#
# optional arguments:
#   -h, --help            show this help message and exit


    massivevisible={}
    massivevisible['usernamePanel']=True
    massivevisible['projectPanel']=True
    massivevisible['resourcePanel']=True
    massivevisible['resolutionPanel']='Advanced'
    massivevisible['cipherPanel']='Advanced'
    massivevisible['debugCheckBoxPanel']='Advanced'
    massivevisible['advancedCheckBoxPanel']=True
    massivevisible['label_hours']=True
    massivevisible['jobParams_hours']=True
    massivevisible['label_nodes']=True
    massivevisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    c.defaults['jobParams_ppn']=12
    c.defaults['jobParams_nodes']=1
    c.defaults['jobParams_hours']=4
    c.defaults['jobParams_mem']=48
    c.visibility=massivevisible
    displayStrings=sshKeyDistDisplayStringsMASSIVE()
    c.displayStrings.__dict__.update(displayStrings.__dict__)
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    c.loginHost=loginHost

    cmd = '\"/usr/local/desktop/vis_manager.py listall\"'
    regex='(?P<sessionid>[0-9]+) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)

    cmd='"/usr/local/desktop/vis_manager.py isrunning -s {sessionid}"'
    regex='true'
    c.running = siteConfig.cmdRegEx(cmd,regex)

    c.stop=siteConfig.cmdRegEx('/usr/local/desktop/vis_manager.py stop -s {sessionid}')
    c.stopForRestart=siteConfig.cmdRegEx('/usr/local/desktop/vis_manager.py stop -s {sessionid} --wait 4')

    cmd='\"/usr/local/desktop/vis_manager.py exechost -s {sessionid}\"'
    regex='(?P<execHost>\S+)'
    c.execHost=siteConfig.cmdRegEx(cmd,regex)

    if flavour:
        c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py newsession -p {project} -t {hours} -n {nodes} -r {resolution} -f %s\'"%flavour,"(?P<sessionid>[0-9]+)")
    else:
        c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py newsession -p {project} -t {hours} -n {nodes} -r {resolution} \'","(?P<sessionid>[0-9]+)")
 
    c.runSanityCheck=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py sanitycheck -l {launcher_version_number}\'")

    # getprojects         list the available projects for running sessions
    c.getProjects=siteConfig.cmdRegEx('\"/usr/local/desktop/vis_manager.py getprojects \"','(?P<group>.*)')

    # showstart           get the estimate of when the vis session will start
    # usage: vis_manager.py showstart [-h] -s SESSIONID
    # c.showStart=siteConfig.cmdRegEx("showstart {jobid}","Estimated Rsv based start .*?on (?P<estimatedStart>.*)")
    c.showStart=siteConfig.cmdRegEx("/usr/local/desktop/vis_manager.py showstart -s {sessionid}","(?P<estimatedStart>.*)")

    # vncport             return the port on which the vnc server started
    # usage: vis_manager.py vncport [-h] -s SESSIONID
    c.vncDisplay=siteConfig.cmdRegEx("/usr/local/desktop/vis_manager.py vncport -s {sessionid}",'^(?P<vncDisplay>:[0-9]+)')

    c.otp= siteConfig.cmdRegEx('/usr/local/desktop/vis_manager.py getpassword','(?P<vncPasswd>[0-9]+)\s*$')

    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -l {username} {loginHost} \"/usr/bin/ssh -A {execHost} \\"echo agent_hello; bash \\"\"','agent_hello',async=True)

    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"echo DBUS_SESSION_BUS_ADDRESS=dummy_dbus_session_bus_address"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/bin/ssh {execHost} /usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='echo Mounting WebDAV...' # For CentOS 5 / KDE, we are not really "mounting", just displaying the WebDAV share in Konqueror.
    c.webDavMount=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/bin/konqueror webdav://{localUsername}:{vncPasswd}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    # The Window ID is not needed for MASSIVE.  We use the server-side script: /usr/local/desktop/close_webdav_window.sh which figures out which window to close.
    cmd='"echo DummyWebDavWindowID=-1"'
    regex='^DummyWebDavWindowID=(?P<webDavWindowID>.*)$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd='"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Konqueror with the URL:%sbr%s\\nwebdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}%sbr%s\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt;\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop = siteConfig.cmdRegEx(cmd)

    # Chris trying to avoid using the intermediate port:
    #cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {execHost}:{remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"'

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {intermediateWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "ssh -R {remoteWebDavPortNumber}:localhost:{intermediateWebDavPortNumber} {execHost} \'echo tunnel_hello; bash\'"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd = 'echo hello'
    regex = 'hello'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/local/desktop/close_webdav_window.sh webdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)

    return c

def getRaijinSiteConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsNCI()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['ppnLabel']=False
    c.visibility['jobParams_ppn']=False
    c.visibility['ssh_key_mode_panel']='Advanced'
    c.visibility['copyid_mode_panel']=False
    c.loginHost='raijin.nci.org.au'
    c.directConnect=False
    cmd='\"module load pbs ; qstat -f {jobidNumber} \"'
    regex='.*job_state = R.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"module load pbs ; qdel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"module load pbs ; qdel {jobidNumber}\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/passwdfile\'','^(?P<vncPasswd>\S+)$')
    cmd='\" mkdir ~/.vnc ; rm -f ~/.vnc/passwdfile ; touch ~/.vnc/passwdfile ; chmod 600 ~/.vnc/passwdfile ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/passwdfile ;  echo \\\" module load x11vnc ; x11vnc -usepw -create -shared -forever\\\" | qsub -q %s -l ncpus={nodes} -N desktop_{username} -l walltime={hours}:00 -o .vnc/ -e .vnc/ \"'%queue
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay=siteConfig.cmdRegEx('\'qcat {jobidNumber}\'','PORT=59(?P<vncDisplay>[0-9]+)')
    cmd='\"module load pbs ; qstat -f {jobidNumber} | grep exec_host\"'
    regex='^\s*exec_host = (?P<execHost>r[0-9]+)\/.*$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"module load pbs ; qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+\S+\s+(?P<jobname>desktop_\S+)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+(?P<elapTime>\S+)\s*$',requireMatch=False)
    return c

def getMassiveCentos6SiteConfig(loginHost,flavour=None):
# usage: vis_manager.py [-h]
#
#                       {showstart,isrunning,vncport,newsession,stop,sanitycheck,getprojects,exechost,listall}
#                       ...
#
# positional arguments:
#   {showstart,isrunning,vncport,newsession,stop,sanitycheck,getprojects,exechost,listall}
#     listall             lists all the users running vis jobs in the format of
#                         "sessionid timeleft (seconds)"
#     newsession          create a new desktop session and return an id or error
#                         message
#     isrunning           test if a vis session has started yet (returns "true"
#                         if it is)
#     exechost            return information about which node a vis session is
#                         running on
#     vncport             return the port on which the vnc server started
#     stop                stop a running vis session
#     getprojects         list the available projects for running sessions
#     showstart           get the estimate of when the vis session will start
#     sanitycheck         run a simple sanity check e.g. make sure the user has
#                         enough file system space to create files
#
# optional arguments:
#   -h, --help            show this help message and exit


    massivevisible={}
    massivevisible['usernamePanel']=True
    massivevisible['projectPanel']=True
    massivevisible['resourcePanel']=True
    massivevisible['resolutionPanel']='Advanced'
    massivevisible['cipherPanel']='Advanced'
    massivevisible['debugCheckBoxPanel']='Advanced'
    massivevisible['advancedCheckBoxPanel']=True
    massivevisible['label_hours']=True
    massivevisible['jobParams_hours']=True
    massivevisible['label_nodes']=True
    massivevisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    c.defaults['jobParams_ppn']=12
    c.defaults['jobParams_nodes']=1
    c.defaults['jobParams_hours']=4
    c.defaults['jobParams_mem']=48
    c.visibility=massivevisible
    displayStrings=sshKeyDistDisplayStringsMASSIVE()
    c.displayStrings.__dict__.update(displayStrings.__dict__)
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    c.loginHost=loginHost

    # listall             lists all the users running vis jobs in the format of "sessionid timeleft (seconds)"
    # usage: vis_manager.py listall [-h]
    # cmd = '\"module load xmlstarlet ; qstat -x | xml sel -t -m \\"/Data/Job[starts-with(Job_Owner/text(),\'{username}@\') and starts-with(Job_Name/text(),\'desktop\') and job_state/text()!=\'C\']\\" -v \\" concat(./Job_Id/text(),\' \',./Walltime/Remaining/text())  \\" -n - 2>/dev/null\"'
    cmd = '\"/usr/local/desktop/vis_manager.py listall\"'
    # regex='(?P<jobid>(?P<jobidNumber>[0-9]+).\S+) (?P<remainingWalltime>.*)$'
    regex='(?P<sessionid>[0-9]+) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)

    # isrunning           test if a vis session has started yet (returns "true" if it is)
    # usage: vis_manager.py isrunning [-h] -s SESSIONID
    # cmd='\"module load pbs ; module load maui ; qstat -f {jobidNumber} -x\"'
    cmd='"/usr/local/desktop/vis_manager.py isrunning -s {sessionid}"'
    # regex='.*<job_state>R</job_state>.*'
    regex='true'
    c.running = siteConfig.cmdRegEx(cmd,regex)

    # stop                stop a running vis session
    # usage: vis_manager.py stop [-h] -s SESSIONID [-w WAIT]
    # c.stop=siteConfig.cmdRegEx('\'qdel -a {jobidNumber}\'')
    c.stop=siteConfig.cmdRegEx('/usr/local/desktop/vis_manager.py stop -s {sessionid}')
    # c.stopForRestart=siteConfig.cmdRegEx('qdel {jobidNumber} ; sleep 5\'')
    c.stopForRestart=siteConfig.cmdRegEx('/usr/local/desktop/vis_manager.py stop -s {sessionid} --wait 4')

    # exechost            return information about which node a vis session is running on
    # usage: vis_manager.py exechost [-h] -s SESSIONID
    # cmd='\"module load xmlstarlet ; qstat -x -f {jobid} | xml sel -t -m \\"/Data/Job/exec_host/text()\\" -c \\".\\" -n - | cut -f 1 -d \\"/\\"\"'
    cmd='\"/usr/local/desktop/vis_manager.py exechost -s {sessionid}\"'
    regex='(?P<execHost>\S+)'
    c.execHost=siteConfig.cmdRegEx(cmd,regex)

    # newsession          create a new desktop session and return an id or error message
    # usage: vis_manager.py newsession [-h] -p PROJECT -t HOURS [-f FLAVOUR] [-n NODES] [-r RESOLUTION]
    # c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/request_visnode.sh {project} {hours} {nodes} True False False {resolution}\'","^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$")
    if flavour:
        c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py newsession -p {project} -t {hours} -n {nodes} -r {resolution} -f %s\'"%flavour,"(?P<sessionid>[0-9]+)")
    else:
        c.startServer=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py newsession -p {project} -t {hours} -n {nodes} -r {resolution} \'","(?P<sessionid>[0-9]+)")
 
    # sanitycheck         run a simple sanity check e.g. make sure the user has enough file system space to create files
    # usage: vis_manager.py sanitycheck [-h] -l LAUNCHERVERSION
    # c.runSanityCheck=siteConfig.cmdRegEx("\'/usr/local/desktop/sanity_check.sh {launcher_version_number}\'")
    c.runSanityCheck=siteConfig.cmdRegEx("\'/usr/local/desktop/vis_manager.py sanitycheck -l {launcher_version_number}\'")

    # getprojects         list the available projects for running sessions
    # usage: vis_manager.py getprojects [-h]
    #c.getProjects=siteConfig.cmdRegEx('\"glsproject -A -q | grep \',{username},\|\s{username},\|,{username}\s\|\s{username}\s\' \"','^(?P<group>\S+)\s+.*$')
    # older c.getProjects=siteConfig.cmdRegEx('\"/usr/local/bin/glsproject_timeout -A -q | grep -P \'[,\s]{username}[,\s]\' \"','^(?P<group>\S+)\s+.*$')
    # old c.getProjects=siteConfig.cmdRegEx('\"/usr/local/bin/glsproject_timeout -A -q | grep -P \'[,\s]{username}[,\s]\' \"','^(?P<group>\S+)\s+.*$')
    c.getProjects=siteConfig.cmdRegEx('\"/usr/local/desktop/vis_manager.py getprojects \"','(?P<group>.*)')

    # showstart           get the estimate of when the vis session will start
    # usage: vis_manager.py showstart [-h] -s SESSIONID
    # c.showStart=siteConfig.cmdRegEx("showstart {jobid}","Estimated Rsv based start .*?on (?P<estimatedStart>.*)")
    c.showStart=siteConfig.cmdRegEx("/usr/local/desktop/vis_manager.py showstart -s {sessionid}","(?P<estimatedStart>.*)")

    # vncport             return the port on which the vnc server started
    # usage: vis_manager.py vncport [-h] -s SESSIONID
    c.vncDisplay= siteConfig.cmdRegEx('"/usr/bin/ssh {execHost} \' module load turbovnc ; vncserver -list\'"','^(?P<vncDisplay>:[0-9]+)\s*(?P<vncPID>[0-9]+)\s*$')

    c.otp= siteConfig.cmdRegEx('"/usr/bin/ssh {execHost} \' module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\'"','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')

    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -l {username} {loginHost} \"/usr/bin/ssh -A {execHost} \\"echo agent_hello; bash \\"\"','agent_hello',async=True)

    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"echo DBUS_SESSION_BUS_ADDRESS=dummy_dbus_session_bus_address"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/bin/ssh {execHost} /usr/local/desktop/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='echo Mounting WebDAV...' # For CentOS 5 / KDE, we are not really "mounting", just displaying the WebDAV share in Konqueror.
    c.webDavMount=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/bin/konqueror webdav://{localUsername}:{vncPasswd}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    # The Window ID is not needed for MASSIVE.  We use the server-side script: /usr/local/desktop/close_webdav_window.sh which figures out which window to close.
    cmd='"echo DummyWebDavWindowID=-1"'
    regex='^DummyWebDavWindowID=(?P<webDavWindowID>.*)$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd='"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Konqueror with the URL:%sbr%s\\nwebdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}%sbr%s\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt;\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop = siteConfig.cmdRegEx(cmd)

    # Chris trying to avoid using the intermediate port:
    #cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {execHost}:{remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"'

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {intermediateWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} "ssh -R {remoteWebDavPortNumber}:localhost:{intermediateWebDavPortNumber} {execHost} \'echo tunnel_hello; bash\'"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd = 'echo hello'
    regex = 'hello'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'DISPLAY={vncDisplay} /usr/local/desktop/close_webdav_window.sh webdav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)

    return c

def getRaijinSiteConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsNCI()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['ppnLabel']=False
    c.visibility['jobParams_ppn']=False
    c.visibility['ssh_key_mode_panel']='Advanced'
    c.visibility['copyid_mode_panel']=False
    c.loginHost='raijin.nci.org.au'
    c.directConnect=False
    cmd='\"module load pbs ; qstat -f {jobidNumber} \"'
    regex='.*job_state = R.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"module load pbs ; qdel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"module load pbs ; qdel {jobidNumber}\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/passwdfile\'','^(?P<vncPasswd>\S+)$')
    cmd='\" mkdir ~/.vnc ; rm -f ~/.vnc/passwdfile ; touch ~/.vnc/passwdfile ; chmod 600 ~/.vnc/passwdfile ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/passwdfile ;  echo \\\" module load x11vnc ; x11vnc -usepw -create -shared -forever\\\" | qsub -q %s -l ncpus={nodes} -N desktop_{username} -l walltime={hours}:00 -o .vnc/ -e .vnc/ \"'%queue
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay=siteConfig.cmdRegEx('\'qcat {jobidNumber}\'','PORT=59(?P<vncDisplay>[0-9]+)')
    cmd='\"module load pbs ; qstat -f {jobidNumber} | grep exec_host\"'
    regex='^\s*exec_host = (?P<execHost>r[0-9]+)\/.*$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"module load pbs ; qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+\S+\s+(?P<jobname>desktop_\S+)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+(?P<elapTime>\S+)\s*$',requireMatch=False)
    return c

def getRaijinLoginSiteConfig(loginnode):
    c = getCVLSiteConfig(" ")
    c.visibility['resourcePanel']=False
    c.visibility['ssh_key_mode_panel']='Advanced'
    c.visibility['copyid_mode_panel']=False
    c.loginHost=loginnode
    c.directConnect=False
    cmd='\" pid=\"\'$\'\"( cat ~/.vnc/{loginHost}.log | grep pid | rev | cut -f 1 -d \\\" \\\" | rev ) ; ps -p \"\'$\'\"pid -o pid,pgrp,user --no-headers 2>/dev/null\"'
    regex='(?P<pid>[0-9]+)\s+(?P<pgrp>[0-9]+)\s+{username}'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    # For reasons I don't understand Xvfb does not inherit the process group of x11vnc
    c.stop=siteConfig.cmdRegEx('\"kill -- -{pgrp} ; pkill -U {username} Xvfb\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"kill -- -{pgrp} ; pkill -U {username} Xvfb\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/passwdfile\'','^(?P<vncPasswd>\S+)$')
    cmd='\" mkdir ~/.vnc 2>/dev/null ; rm -f ~/.vnc/{loginHost}.log ; rm -f ~/.vnc/passwdfile ; touch ~/.vnc/passwdfile ; chmod 600 ~/.vnc/passwdfile ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/passwdfile ; module load x11vnc ; x11vnc -usepw -create -shared -forever > .vnc/{loginHost}.log 2>{ampersand}1 {ampersand} echo started\"'
    c.startServer=siteConfig.cmdRegEx(cmd,"started")
    c.vncDisplay=siteConfig.cmdRegEx('\'cat ~/.vnc/{loginHost}.log\'','PORT=59(?P<vncDisplay>[0-9]+)')
    c.execHost = siteConfig.cmdRegEx()
    c.listAll=siteConfig.cmdRegEx('\"pid=\"\'$\'\"( cat ~/.vnc/{loginHost}.log 2>/dev/null | grep pid | rev | cut -f 1 -d \\\" \\\" | rev ) ; ps -p \"\'$\'\"pid -o pid,pgrp,user --no-headers 2>/dev/null\"','(?P<pid>[0-9]+)\s+(?P<pgrp>[0-9]+)\s+{username}',requireMatch=False)
    return c

def getSiteConfigSlurm(loginhost,partition):
    cvlvisible={}
    cvlvisible['usernamePanel']=True
    cvlvisible['resourcePanel']='Advanced'
    cvlvisible['resolutionPanel']='Advanced'
    cvlvisible['cipherPanel']='Advanced'
    cvlvisible['debugCheckBoxPanel']='Advanced'
    cvlvisible['advancedCheckBoxPanel']=True
    cvlvisible['label_hours']=True
    cvlvisible['jobParams_hours']=True
    cvlvisible['label_ppn']=True
    cvlvisible['jobParams_ppn']=True
    cvlvisible['label_nodes']=True
    cvlvisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    cvlstrings = sshKeyDistDisplayStringsCVL()
    c.displayStrings.__dict__.update(cvlstrings.__dict__)
    c.visibility=cvlvisible
    c.directConnect=True
    c.authURL=None
    c.loginHost=loginhost
    c.defaults['jobParams_ppn']=1
    c.defaults['jobParams_hours']=48
    c.defaults['jobParams_mem']=4


    cmd = '\"squeue -u {username} -o \\"%i %L\\" | tail -n -1\"'
    regex='(?P<jobid>(?P<jobidNumber>[0-9]+)) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)


    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    
    #cmd='\"squeue -j {jobidNumber} -o "%N" | tail -n -1 | cut -f 1 -d \',\' | xargs -iname getent hosts name | cut -f 1 -d \' \' \"'
    cmd='\"scontrol show job {jobidNumber} | grep BatchHost | cut -f 2 -d \'=\' | xargs -iname getent hosts name | cut -f 1 -d \' \' \"'

    regex='^(?P<execHost>.*)$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"groups | sed \'s@ @\\n@g\'\"' # '\'groups | sed \'s\/\\\\ \/\\\\\\\\n\/g\'\''
    regex='^\s*(?P<group>\S+)\s*$'
    c.getProjects = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"scontrol show job {jobidNumber}\"'
    regex='JobState=RUNNING'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    cmd="\"mkdir ~/.vnc ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; module load turbovnc ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ; export PATH=\"\'$\'\"PATH:/bin ; echo -e \'#!/bin/bash\\n vncserver -geometry {resolution} ; sleep 36000 \' |  sbatch -p %s -N {nodes} --mincpus {ppn} --time={hours}:00:00 -J desktop_{username} -o .vnc/slurm-%%j.out \""%partition
#    cmd="\" echo -e \'#!/bin/bash\\n/usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  sbatch -p %s -N {nodes} --mincpus {ppn} --time={hours}:00:00 -J desktop_{username} -o .vnc/slurm-%%j.out \""%partition
    regex="^Submitted batch job (?P<jobid>(?P<jobidNumber>[0-9]+))$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"scancel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"scancel {jobidNumber}\"')
    #c.vncDisplay= siteConfig.cmdRegEx('\"cat .vnc/slurm-{jobidNumber}.out\"' ,'^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.vncDisplay= siteConfig.cmdRegEx('\"cat .vnc/slurm-{jobidNumber}.out\"' ,'^.*?desktop is \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -l {username} {loginHost} \"/usr/bin/ssh -A {execHost} \\"echo agent_hello; bash \\"\"','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=yes -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    #c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {execHost} "echo agent_hello; bash "','agent_hello',async=True)
    #c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"/usr/bin/ssh {execHost} \'export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh\'"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    # Below, I initially tried to respect the user's Nautilus setting of always_use_location_entry and change it back after launching Nautilus,
    # but doing so changes this setting in already-running Nautilus windows, and I want the user to see Nautilus's location bar when showing 
    # them the WebDav share.  So now, I just brutally change the user's Nautilus location-bar setting to always_use_location_entry.
    # Note that we might end up mounting WebDAV in a completely different way (e.g. using wdfs), but for now I'm trying to make the user
    # experience similar on MASSIVE and the CVL.  On MASSIVE, users are not automatically added to the "fuse" group, but they can still 
    # access a WebDAV share within Konqueror.  The method below for the CVL/Nautilus does require fuse membership, but it ends up looking
    # similar to MASSIVE/Konqueror from the user's point of view.  

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\""
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree\'"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Nautilus File Browser, using the location:\\n\\ndav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\n\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop=siteConfig.cmdRegEx(cmd)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {execHost} "echo tunnel_hello; bash"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    #cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};DISPLAY={vncDisplay} timeout 3 gvfs-mount -u \".gvfs/WebDAV on localhost\"\'"'
    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav\'"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    cmd = '"/usr/bin/ssh {execHost} \'module load keyutility ; mountUtility.py\'"'
    #c.onConnectScript = siteConfig.cmdRegEx(cmd)
    return c

def getCVLSiteConfigSlurm(partition):
    cvlvisible={}
    cvlvisible['usernamePanel']=True
    cvlvisible['resourcePanel']='Advanced'
    cvlvisible['resolutionPanel']='Advanced'
    cvlvisible['cipherPanel']='Advanced'
    cvlvisible['debugCheckBoxPanel']='Advanced'
    cvlvisible['advancedCheckBoxPanel']=True
    cvlvisible['label_hours']=True
    cvlvisible['jobParams_hours']=True
    cvlvisible['label_ppn']=True
    cvlvisible['jobParams_ppn']=True
    cvlvisible['label_nodes']=True
    cvlvisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    cvlstrings = sshKeyDistDisplayStringsCVL()
    c.displayStrings.__dict__.update(cvlstrings.__dict__)
    c.visibility=cvlvisible
    c.directConnect=True
    c.authURL=None
    c.loginHost='118.138.233.195'
    c.defaults['jobParams_ppn']=1
    c.defaults['jobParams_hours']=48
    c.defaults['jobParams_mem']=4


    cmd = '\"squeue -u {username} -o \\"%i %L\\" | tail -n -1\"'
    regex='(?P<jobid>(?P<jobidNumber>[0-9]+)) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)


    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    
    #cmd='\"squeue -j {jobidNumber} -o "%N" | tail -n -1 | cut -f 1 -d \',\' | xargs -iname getent hosts name | cut -f 1 -d \' \' \"'
    cmd='\"scontrol show job {jobidNumber} | grep BatchHost | cut -f 2 -d \'=\' | xargs -iname getent hosts name | cut -f 1 -d \' \' \"'

    regex='^(?P<execHost>.*)$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"groups | sed \'s@ @\\n@g\'\"' # '\'groups | sed \'s\/\\\\ \/\\\\\\\\n\/g\'\''
    regex='^\s*(?P<group>\S+)\s*$'
    c.getProjects = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"scontrol show job {jobidNumber}\"'
    regex='JobState=RUNNING'
    c.running=siteConfig.cmdRegEx(cmd,regex)
 #   cmd="\"mkdir ~/.vnc ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; module load turbovnc ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ; echo -e \'#!/bin/bash\\n/usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  sbatch -p %s -N {nodes} -n {ppn} --time={hours}:00:00 -J desktop_{username} -o .vnc/slurm-%%j.out \""%partition
    cmd="\" echo -e \'#!/bin/bash\\n/usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  sbatch -p %s -N {nodes} --mincpus {ppn} --time={hours}:00:00 -J desktop_{username} -o .vnc/slurm-%%j.out \""%partition
    regex="^Submitted batch job (?P<jobid>(?P<jobidNumber>[0-9]+))$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"scancel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"scancel {jobidNumber}\"')
    c.vncDisplay= siteConfig.cmdRegEx('\"cat .vnc/slurm-{jobidNumber}.out\"' ,'^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$',host='exec')
    cmd= '\"module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\"'
    regex='^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$'
    c.otp=siteConfig.cmdRegEx(cmd,regex,host='exec')
#    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {execHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"/usr/bin/ssh {execHost} \'export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh\'"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    # Below, I initially tried to respect the user's Nautilus setting of always_use_location_entry and change it back after launching Nautilus,
    # but doing so changes this setting in already-running Nautilus windows, and I want the user to see Nautilus's location bar when showing 
    # them the WebDav share.  So now, I just brutally change the user's Nautilus location-bar setting to always_use_location_entry.
    # Note that we might end up mounting WebDAV in a completely different way (e.g. using wdfs), but for now I'm trying to make the user
    # experience similar on MASSIVE and the CVL.  On MASSIVE, users are not automatically added to the "fuse" group, but they can still 
    # access a WebDAV share within Konqueror.  The method below for the CVL/Nautilus does require fuse membership, but it ends up looking
    # similar to MASSIVE/Konqueror from the user's point of view.  

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\""
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree\'"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Nautilus File Browser, using the location:\\n\\ndav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\n\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop=siteConfig.cmdRegEx(cmd)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {execHost} "echo tunnel_hello; bash"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    #cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};DISPLAY={vncDisplay} timeout 3 gvfs-mount -u \".gvfs/WebDAV on localhost\"\'"'
    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav\'"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    cmd = '"/usr/bin/ssh {execHost} \'module load keyutility ; mountUtility.py\'"'
    #c.onConnectScript = siteConfig.cmdRegEx(cmd)
    return c

def getCVLSiteConfigXML(queue):
    cvlvisible={}
    cvlvisible['usernamePanel']=True
    cvlvisible['resourcePanel']='Advanced'
    cvlvisible['resolutionPanel']='Advanced'
    cvlvisible['cipherPanel']='Advanced'
    cvlvisible['debugCheckBoxPanel']='Advanced'
    cvlvisible['advancedCheckBoxPanel']=True
    cvlvisible['label_hours']=True
    cvlvisible['jobParams_hours']=True
    cvlvisible['label_ppn']=True
    cvlvisible['jobParams_ppn']=True
    cvlvisible['label_nodes']=True
    cvlvisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    cvlstrings = sshKeyDistDisplayStringsCVL()
    c.displayStrings.__dict__.update(cvlstrings.__dict__)
    c.visibility=cvlvisible
    c.loginHost='login.cvl.massive.org.au'
    c.directConnect=True
    c.authURL="https://autht.massive.org.au/cvl/"
    c.loginHost='login.cvl.massive.org.au'
    c.defaults['jobParams_ppn']=1
    c.defaults['jobParams_hours']=48
    c.defaults['jobParams_mem']=4


    cmd = '\"module load pbs ; qstat -x | xmlstarlet sel -t -m \\"/Data/Job[starts-with(Job_Owner/text(),\'{username}@\') and starts-with(Job_Name/text(),\'desktop\') and job_state/text()!=\'C\']\\" -v \\" concat(./Job_Id/text(),\' \',./Walltime/Remaining/text())  \\" -n - 2>/dev/null\"'
    regex='(?P<jobid>(?P<jobidNumber>[0-9]+).\S+) (?P<remainingWalltime>.*)$'
    c.listAll=siteConfig.cmdRegEx(cmd,regex,requireMatch=False)


    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    cmd='\"module load pbs ; qstat -f {jobidNumber} | grep exec_host | sed \'s/\ \ */\ /g\' | cut -f 4 -d \' \' | cut -f 1 -d \'/\' | xargs -iname hostn name | grep address | sed \'s/\ \ */\ /g\' | cut -f 3 -d \' \' | xargs -iip echo execHost ip; qstat -f {jobidNumber}\"'
    regex='^\s*execHost (?P<execHost>\S+)\s*$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"groups | sed \'s@ @\\n@g\'\"' # '\'groups | sed \'s\/\\\\ \/\\\\\\\\n\/g\'\''
    regex='^\s*(?P<group>\S+)\s*$'
    c.getProjects = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"module load pbs ; module load maui ; qstat -f {jobidNumber} -x\"'
    regex='.*<job_state>R</job_state>.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    cmd="\"module load pbs ; module load maui ; echo \'module load pbs ; /usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  qsub -q %s -l nodes=1:ppn=1 -l walltime={hours}:00:00 -N desktop_{username} -o .vnc/ -e .vnc/ \""%queue
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"module load pbs ; module load maui ; qdel -a {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"module load pbs ; module load maui ; qdel {jobidNumber}\"')
    c.vncDisplay= siteConfig.cmdRegEx('\"cat /var/spool/torque/spool/{jobidNumber}.*\"' ,'^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$',host='exec')
    cmd= '\"module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\"'
    regex='^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$'
    c.otp=siteConfig.cmdRegEx(cmd,regex,host='exec')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {execHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"/usr/bin/ssh {execHost} \'export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh\'"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    # Below, I initially tried to respect the user's Nautilus setting of always_use_location_entry and change it back after launching Nautilus,
    # but doing so changes this setting in already-running Nautilus windows, and I want the user to see Nautilus's location bar when showing 
    # them the WebDav share.  So now, I just brutally change the user's Nautilus location-bar setting to always_use_location_entry.
    # Note that we might end up mounting WebDAV in a completely different way (e.g. using wdfs), but for now I'm trying to make the user
    # experience similar on MASSIVE and the CVL.  On MASSIVE, users are not automatically added to the "fuse" group, but they can still 
    # access a WebDAV share within Konqueror.  The method below for the CVL/Nautilus does require fuse membership, but it ends up looking
    # similar to MASSIVE/Konqueror from the user's point of view.  

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\""
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree\'"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Nautilus File Browser, using the location:\\n\\ndav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\n\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop=siteConfig.cmdRegEx(cmd)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {execHost} "echo tunnel_hello; bash"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    #cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};DISPLAY={vncDisplay} timeout 3 gvfs-mount -u \".gvfs/WebDAV on localhost\"\'"'
    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav\'"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    cmd = '"/usr/bin/ssh {execHost} \'module load keyutility ; mountUtility.py\'"'
    c.onConnectScript = siteConfig.cmdRegEx(cmd)
    return c

def getCVLSiteConfig(queue):
    cvlvisible={}
    cvlvisible['usernamePanel']=True
    cvlvisible['resourcePanel']='Advanced'
    cvlvisible['resolutionPanel']='Advanced'
    cvlvisible['cipherPanel']='Advanced'
    cvlvisible['debugCheckBoxPanel']='Advanced'
    cvlvisible['advancedCheckBoxPanel']=True
    cvlvisible['label_hours']=True
    cvlvisible['jobParams_hours']=True
    cvlvisible['label_ppn']=True
    cvlvisible['jobParams_ppn']=True
    cvlvisible['label_nodes']=True
    cvlvisible['jobParams_nodes']=True
    c = siteConfig.siteConfig()
    cvlstrings = sshKeyDistDisplayStringsCVL()
    c.displayStrings.__dict__.update(cvlstrings.__dict__)
    c.visibility=cvlvisible
    c.authURL="https://autht.massive.org.au/cvl/"
    c.loginHost='login.cvl.massive.org.au'
    c.defaults['jobParams_ppn']=1
    c.defaults['jobParams_hours']=48
    c.defaults['jobParams_mem']=4
    c.directConnect=True
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    cmd='\"module load pbs ; qstat -f {jobidNumber} | grep exec_host | sed \'s/\ \ */\ /g\' | cut -f 4 -d \' \' | cut -f 1 -d \'/\' | xargs -iname hostn name | grep address | sed \'s/\ \ */\ /g\' | cut -f 3 -d \' \' | xargs -iip echo execHost ip; qstat -f {jobidNumber}\"'
    regex='^\s*execHost (?P<execHost>\S+)\s*$'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    cmd='\"groups | sed \'s@ @\\n@g\'\"' # '\'groups | sed \'s\/\\\\ \/\\\\\\\\n\/g\'\''
    regex='^\s*(?P<group>\S+)\s*$'
    c.getProjects = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"module load pbs ; qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+(?P<queue>%s)\s+(?P<jobname>desktop_\S+)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+(?P<elapTime>\S+)\s*$'%queue,requireMatch=False)
    cmd='\"module load pbs ; module load maui ; qstat -f {jobidNumber} -x\"'
    regex='.*<job_state>R</job_state>.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    cmd="\"module load pbs ; module load maui ; echo \'module load pbs ; /usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  qsub -q %s -l nodes=1:ppn=1 -l walltime={hours}:00:00 -N desktop_{username} -o .vnc/ -e .vnc/ \""%queue
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\"module load pbs ; module load maui ; qdel -a {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"module load pbs ; module load maui ; qdel {jobidNumber}\"')
    c.vncDisplay= siteConfig.cmdRegEx('\"cat /var/spool/torque/spool/{jobidNumber}.*\"' ,'^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$',host='exec')
    cmd= '\"module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\"'
    regex='^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$'
    c.otp=siteConfig.cmdRegEx(cmd,regex,host='exec')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {execHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"/usr/bin/ssh {execHost} \'export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh\'"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<intermediateWebDavPortNumber>[0-9]+)$'
    c.webDavIntermediatePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex,host='exec')

    # Below, I initially tried to respect the user's Nautilus setting of always_use_location_entry and change it back after launching Nautilus,
    # but doing so changes this setting in already-running Nautilus windows, and I want the user to see Nautilus's location bar when showing 
    # them the WebDav share.  So now, I just brutally change the user's Nautilus location-bar setting to always_use_location_entry.
    # Note that we might end up mounting WebDAV in a completely different way (e.g. using wdfs), but for now I'm trying to make the user
    # experience similar on MASSIVE and the CVL.  On MASSIVE, users are not automatically added to the "fuse" group, but they can still 
    # access a WebDAV share within Konqueror.  The method below for the CVL/Nautilus does require fuse membership, but it ends up looking
    # similar to MASSIVE/Konqueror from the user's point of view.  

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\""
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh {execHost} \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree\'"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    cmd = '"/usr/bin/ssh {execHost} \'echo -e \\"You can access your local home directory in Nautilus File Browser, using the location:\\n\\ndav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\n\\nYour one-time password is {vncPasswd}\\" > ~/.vnc/\\$(hostname){vncDisplay}-webdav.txt\'"'
    c.displayWebDavInfoDialogOnRemoteDesktop=siteConfig.cmdRegEx(cmd)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {execHost} "echo tunnel_hello; bash"'
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    #cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};DISPLAY={vncDisplay} timeout 3 gvfs-mount -u \".gvfs/WebDAV on localhost\"\'"'
    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav\'"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"/usr/bin/ssh {execHost} \'export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}\'"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    cmd = '"/usr/bin/ssh {execHost} \'module load keyutility ; mountUtility.py\'"'
    c.onConnectScript = siteConfig.cmdRegEx(cmd)
    return c

def getOtherTurboVNCConfig(configName):
    Visible={}
    Visible['usernamePanel']=True
    Visible['projectPanel']=False
    Visible['loginHostPanel']=True
    Visible['resourcePanel']=False
    Visible['resolutionPanel']='Advanced'
    Visible['cipherPanel']='Advanced'
    Visible['debugCheckBoxPanel']='Advanced'
    Visible['advancedCheckBoxPanel']=True
    Visible['optionsDialog']=False
    c = siteConfig.siteConfig()
    c.visibility=Visible
    c.listAll=siteConfig.cmdRegEx('\'module load turbovnc ; vncserver -list\'','^(?P<vncDisplay>:[0-9]+)\s+[0-9]+\s*$',requireMatch=False)
    c.startServer=siteConfig.cmdRegEx('\"/usr/local/bin/vncsession --vnc turbovnc --geometry {resolution}\"','^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.stop=siteConfig.cmdRegEx('\'module load turbovnc ; vncserver -kill {vncDisplay}\'')
    c.stopForRestart=siteConfig.cmdRegEx('\'module load turbovnc ; vncserver -kill {vncDisplay}\'')
    c.otp= siteConfig.cmdRegEx('\'module load turbovnc ; vncpasswd -o -display localhost{vncDisplay}\'','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {loginHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} \'echo tunnel_hello; bash\''
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\"" 
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    return c

def getTurboVNCConfigOzViz(configName):
    Visible={}
    Visible['usernamePanel']=True
    Visible['projectPanel']=False
    Visible['loginHostPanel']=True
    Visible['resourcePanel']=False
    Visible['resolutionPanel']='Advanced'
    Visible['cipherPanel']='Advanced'
    Visible['debugCheckBoxPanel']='Advanced'
    Visible['advancedCheckBoxPanel']=True
    Visible['optionsDialog']=False
    c = siteConfig.siteConfig()
    c.visibility=Visible
    c.listAll=siteConfig.cmdRegEx('\'/opt/TurboVNC/bin/vncserver -list\'','^(?P<vncDisplay>:[0-9]+)\s+[0-9]+\s*$',requireMatch=False)
    c.startServer=siteConfig.cmdRegEx('\"/opt/TurboVNC/bin/vncserver -geometry {resolution}\"','^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.stop=siteConfig.cmdRegEx('\'/opt/TurboVNC/bin/vncserver -kill {vncDisplay}\'')
    c.stopForRestart=siteConfig.cmdRegEx('\'/opt/TurboVNC/bin/vncserver -kill {vncDisplay}\'')
    c.otp= siteConfig.cmdRegEx('\'/opt/TurboVNC/bin/vncpasswd -o -display localhost{vncDisplay}\'','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {loginHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} \'echo tunnel_hello; bash\''
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)
    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\""
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\""
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    return c

##### EPCC VNC Defnitions (LFS Scheduler) ######
def getEPCCSiteConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsCQU()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['label_ppn']=True
    c.visibility['jobParams_ppn']=True
    c.visibility['label_mem']=True
    c.visibility['jobParams_mem']=True
    c.visibility['label_nodes']=False
    c.visibility['jobParams_nodes']=False
    c.visibility['label_hours']=False
    c.visibility['jobParams_hours']=False
    c.loginHost='indy0.epcc.ed.ac.uk'
    c.directConnect=False
    cmd='\"bjobs {jobidNumber} \"'
    regex='.*RUN.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\" bkill {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"bkill {jobidNumber} ; sleep 5\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    cmd='\" mkdir ~/.vnc ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ;  echo \\\" vncserver -geometry {resolution} ; sleep 10000000000\\\" | bsub  -n {ppn} -J INTERACT  -o ~/.vnc/ -e ~/.vnc/\"'
    regex="^Job <(?P<jobid>(?P<jobidNumber>[0-9]+))>.*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay=siteConfig.cmdRegEx('\'cat ~/.vnc/{execHost}*.log\'','port 59(?P<vncDisplay>[0-9]+)')
    cmd='\" bjobs -l {jobidNumber} | grep Started\"'
    regex='^.*Started on <(?P<execHost>[a-z]+[0-9]+)>.*'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"bjobs -u {username} | tail -n +2\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+))\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(?P<jobname>INTERACT)\s+.*$',requireMatch=False)
    c.relabel={}
    c.relabel['label_ppn']='CPUs'
    c.siteRanges={}
    c.siteRanges['jobParams_ppn']=[1,16]
    return c

##### CQU VNC Definitions #####

def getCQUVNCSession():
    import re
    Visible={}
    Visible['usernamePanel']=True
    Visible['projectPanel']=False
    Visible['loginHostPanel']=True
    Visible['resourcePanel']=False
    Visible['resolutionPanel']='Advanced'
    Visible['cipherPanel']='Advanced'
    Visible['debugCheckBoxPanel']='Advanced'
    Visible['advancedCheckBoxPanel']=True
    Visible['optionsDialog']=False
    c = siteConfig.siteConfig()
    c.visibility=Visible

    s = sshKeyDistDisplayStringsCQU()
    c.displayStrings.__dict__.update(s.__dict__)

    siteConfigDict={}
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    c.listAll=siteConfig.cmdRegEx('\'ls ~/.vnc/`hostname`*pid\'','^\S+(?P<vncDisplay>:[0-9]+).pid$',requireMatch=False)
    c.startServer=siteConfig.cmdRegEx('\" /apps/samples/sys-files/startup-checker.sh ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ; vncserver -geometry {resolution}\"','^.*?desktop is \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.stop=siteConfig.cmdRegEx('\'vncserver -kill {vncDisplay}\'')
    c.stopForRestart=siteConfig.cmdRegEx('\'vncserver -kill {vncDisplay}\'')
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {loginHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} \'echo tunnel_hello; bash\''
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\"" 
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    return c

def getCQUGPUConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsCQU()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['label_ppn']=True
    c.visibility['jobParams_ppn']=True
    c.visibility['label_mem']=True
    c.visibility['jobParams_mem']=True
    c.visibility['label_nodes']=False
    c.visibility['jobParams_nodes']=False
    c.visibility['label_hours']=False
    c.visibility['jobParams_hours']=False
    c.loginHost='isaac.cqu.edu.au'
    c.directConnect=False
    cmd='\"qstat -f {jobidNumber} \"'
    regex='.*job_state = R.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\" qdel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"qdel {jobidNumber}\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    cmd='\" /apps/samples/sys-files/startup-checker.sh ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ;  echo \\\" /apps/samples/sys-files/remove-old-vnc-pids.sh ; vncserver -geometry {resolution} ; sleep 10000000000\\\" | qsub  -l ncpus={ppn},mem={mem}g,ngpus=1 -N INTERACT  -o .vnc/ -e .vnc/ \"'
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay=siteConfig.cmdRegEx('\'cat ~/.vnc/{execHost}*.log\'','port 59(?P<vncDisplay>[0-9]+)')
    cmd='\" qstat -f {jobidNumber} | grep exec_host\"'
    regex='^\s*exec_host = (?P<execHost>[a-z]+[0-9]+)'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+\S+\s+(?P<jobname>INTERACT)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+(?P<elapTime>\S+)\s*$',requireMatch=False)
    c.relabel={}
    c.relabel['label_ppn']='CPUs'
    c.siteRanges={}
    c.siteRanges['jobParams_ppn']=[1,16]
    return c


def getCQUStandardVNCConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsCQU()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['label_ppn']=True
    c.visibility['jobParams_ppn']=True
    c.visibility['label_mem']=True
    c.visibility['jobParams_mem']=True
    c.visibility['label_nodes']=False
    c.visibility['jobParams_nodes']=False
    c.visibility['label_hours']=False
    c.visibility['jobParams_hours']=False
    c.loginHost='isaac.cqu.edu.au'
    c.directConnect=False
    cmd='\"qstat -f {jobidNumber} \"'
    regex='.*job_state = R.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\" qdel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"qdel {jobidNumber}\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:{execHost}:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    cmd='\" /apps/samples/sys-files/startup-checker.sh ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ;  echo \\\" /apps/samples/sys-files/remove-old-vnc-pids.sh ; vncserver -geometry {resolution} ; sleep 10000000000\\\" | qsub  -l ncpus={ppn},mem={mem}g -N STANDARD  -o .vnc/ -e .vnc/ \"'
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay=siteConfig.cmdRegEx('\'cat ~/.vnc/{execHost}*.log\'','port 59(?P<vncDisplay>[0-9]+)')
    cmd='\" qstat -f {jobidNumber} | grep exec_host\"'
    regex='^\s*exec_host = (?P<execHost>[a-z]+[0-9]+)'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+\S+\s+(?P<jobname>STANDARD)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+(?P<elapTime>\S+)\s*$',requireMatch=False)
    c.relabel={}
    c.relabel['label_ppn']='CPUs'
    c.siteRanges={}
    c.siteRanges['jobParams_ppn']=[1,64]
    return c

def getBMRIVNCConfig(queue):
    c = getCVLSiteConfig(queue)
    s = sshKeyDistDisplayStringsBMRI()
    c.displayStrings.__dict__.update(s.__dict__)
    c.visibility['resourcePanel']=True
    c.visibility['label_ppn']=False
    c.visibility['jobParams_ppn']=False
    c.visibility['label_mem']=False
    c.visibility['jobParams_mem']=False
    c.visibility['label_nodes']=False
    c.visibility['jobParams_nodes']=False
    c.visibility['label_hours']=True
    c.visibility['jobParams_hours']=True
    c.loginHost='172.18.30.64'
    c.directConnect=False
    cmd='\"qstat -f {jobidNumber} \"'
    regex='.*job_state = R.*'
    c.running=siteConfig.cmdRegEx(cmd,regex)
    c.stop=siteConfig.cmdRegEx('\" qdel {jobidNumber}\"')
    c.stopForRestart=siteConfig.cmdRegEx('\"qdel {jobidNumber}\"')
    c.agent=siteConfig.cmdRegEx()
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)
    #c.otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
    c.otp= siteConfig.cmdRegEx('"/usr/bin/ssh {execHost} \' /opt/TurboVNC/bin/vncpasswd -o -display localhost{vncDisplay}\'"','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')
    cmd='\" /usr/local/bin/check_cache.py; echo \\\"/opt/TurboVNC/bin//vncserver -geometry {resolution} -rfbwait 120000 -otpauth -deferupdate 1 ; sleep 1000000 \\\" | qsub  -l ncpus={ppn},mem={mem}g,walltime={hours}:00:00 -N desktop -q %s  -o .vnc/ -e .vnc/ \"'%queue
    regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
    c.startServer=siteConfig.cmdRegEx(cmd,regex)
    c.vncDisplay= siteConfig.cmdRegEx('\"/usr/bin/ssh {execHost} \' /opt/TurboVNC/bin/vncserver -list\'\"','^(?P<vncDisplay>:[0-9]+)\s*(?P<vncPID>[0-9]+)\s*$')
    #c.vncDisplay= siteConfig.cmdRegEx('\"/usr/bin/ssh {execHost} \'cat ~/.vnc/\\`hostname\\`*.log\'\"','port 59(?P<vncDisplay>[0-9]+)')
    #c.vncDisplay=siteConfig.cmdRegEx('\'cat ~/.vnc/{execHost}*.log\'','port 59(?P<vncDisplay>[0-9]+)')
    cmd = '\" qstat -f {jobidNumber} | grep exec_host | sed \'s/\ \ */\ /g\' | cut -f 4 -d \' \' | cut -f 1 -d \'/\' | xargs -iname hostn name | grep address | sed \'s/\ \ */\ /g\' | cut -f 3 -d \' \' | xargs -iip echo execHost ip; qstat -f {jobidNumber}\"'
    regex='^\s*execHost (?P<execHost>.*)'
    c.execHost = siteConfig.cmdRegEx(cmd,regex)
    c.listAll=siteConfig.cmdRegEx('\"qstat -u {username} | tail -n +6\"','^\s*(?P<jobid>(?P<jobidNumber>[0-9]+).\S+)\s+\S+\s+\S+\s+(?P<jobname>desktop)\s+(?P<sessionID>\S+)\s+(?P<nodes>\S+)\s+(?P<tasks>\S+)\s+(?P<mem>\S+)\s+(?P<reqTime>\S+)\s+(?P<state>[^C])\s+\S+\s*$',requireMatch=False)
    c.relabel={}
    c.relabel['label_ppn']='CPUs'
    c.siteRanges={}
    c.siteRanges['jobParams_ppn']=[1,64]
    c.onFirstLogin="/usr/local/bin/check_cache.py"
    c.onConnectScript=siteConfig.cmdRegEx()
    return c

##### End of CQU VNC Definitions #####



def getGenericVNCSession():
    import re
    Visible={}
    Visible['usernamePanel']=True
    Visible['projectPanel']=False
    Visible['loginHostPanel']=True
    Visible['resourcePanel']=False
    Visible['resolutionPanel']='Advanced'
    Visible['cipherPanel']='Advanced'
    Visible['debugCheckBoxPanel']='Advanced'
    Visible['advancedCheckBoxPanel']=True
    Visible['optionsDialog']=False
    c = siteConfig.siteConfig()
    c.visibility=Visible

    siteConfigDict={}
    c.messageRegexs=[re.compile("^INFO:(?P<info>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^WARN:(?P<warn>.*(?:\n|\r\n?))",re.MULTILINE),re.compile("^ERROR:(?P<error>.*(?:\n|\r\n?))",re.MULTILINE)]
    #c.listAll=siteConfig.cmdRegEx('\'vncserver -list\'','^(?P<vncDisplay>:[0-9]+)\s+[0-9]+\s*$',requireMatch=False)
    c.listAll=siteConfig.cmdRegEx('\'ls ~/.vnc/`hostname`*pid\'','^\S+(?P<vncDisplay>:[0-9]+).pid$',requireMatch=False)
    #c.startServer=siteConfig.cmdRegEx('\"vncserver -geometry {resolution}\"','^.*?started on display \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.startServer=siteConfig.cmdRegEx('\" mkdir ~/.vnc 2>/dev/null ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ; vncserver -geometry {resolution}\"','^.*?desktop is \S+(?P<vncDisplay>:[0-9]+)\s*$')
    c.stop=siteConfig.cmdRegEx('\'vncserver -kill {vncDisplay}\'')
    c.stopForRestart=siteConfig.cmdRegEx('\'vncserver -kill {vncDisplay}\'')
    #c.otp= siteConfig.cmdRegEx('\'vncpasswd -o -display localhost{vncDisplay}\'','^\s*Full control one-time password: (?P<vncPasswd>[0-9]+)\s*$')
    c.otp= siteConfig.cmdRegEx('\'echo "vncpasswd:" `cat ~/.vnc/clearpass`\'','^vncpasswd: (?P<vncPasswd>\S+)$')
    c.agent=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -l {username} {loginHost} "echo agent_hello; bash "','agent_hello',async=True)
    c.tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -l {username} {loginHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

    cmd='"export DISPLAY={vncDisplay};timeout 15 /usr/local/bin/cat_dbus_session_file.sh"'
    regex='^DBUS_SESSION_BUS_ADDRESS=(?P<dbusSessionBusAddress>.*)$'
    c.dbusSessionBusAddress=siteConfig.cmdRegEx(cmd,regex)

    cmd='\"/usr/local/bin/get_ephemeral_port.py\"'
    regex='^(?P<remoteWebDavPortNumber>[0-9]+)$'
    c.webDavRemotePort=siteConfig.cmdRegEx(cmd,regex)

    cmd='{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -R {remoteWebDavPortNumber}:localhost:{localWebDavPortNumber} -l {username} {loginHost} \'echo tunnel_hello; bash\''
    regex='tunnel_hello'
    c.webDavTunnel=siteConfig.cmdRegEx(cmd,regex,async=True)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};echo \\\\\\\"import pexpect;child = pexpect.spawn('gvfs-mount dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}');child.expect('Password: ');child.sendline('{vncPasswd}');child.expect(pexpect.EOF);child.close();print 'gvfs-mount returned ' + str(child.exitstatus)\\\\\\\" {pipe} python\\\"\"" 
    regex='^gvfs-mount returned (?P<webDavMountingExitCode>.*)$'
    c.webDavMount=siteConfig.cmdRegEx(cmd,regex)

    cmd="\"/usr/bin/ssh -oStrictHostKeyChecking=no localhost \\\"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};/usr/bin/gconftool-2 --type=Boolean --set /apps/nautilus/preferences/always_use_location_entry true {ampersand}{ampersand} DISPLAY={vncDisplay} xdg-open dav://{localUsername}@localhost:{remoteWebDavPortNumber}/{homeDirectoryWebDavShareName}\\\"\"" 
    c.openWebDavShareInRemoteFileBrowser=siteConfig.cmdRegEx(cmd)

    cmd='"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress}; DISPLAY={vncDisplay} xwininfo -root -tree"'
    regex= '^\s+(?P<webDavWindowID>\S+)\s+"{homeDirectoryWebDavShareName}.*Browser.*$'
    c.webDavWindowID=siteConfig.cmdRegEx(cmd,regex)

    # 1. I'm using gvfs-mount --unmount-scheme dav for now, to unmount all GVFS WebDAV mounts,
    #    because using "gvfs-mount --unmount " on a specific mount point from a Launcher
    #    subprocess doesn't seem to work reliably, even though it works fine outside of the 
    #    Launcher.
    # 2. I'm using timeout with gvfs-mount, because sometimes the process never exits
    #    when unmounting, even though the unmounting operation is complete.
    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay};timeout 1 gvfs-mount --unmount-scheme dav"'
    c.webDavUnmount=siteConfig.cmdRegEx(cmd)

    cmd = '"export DBUS_SESSION_BUS_ADDRESS={dbusSessionBusAddress};export DISPLAY={vncDisplay}; wmctrl -F -i -c {webDavWindowID}"'
    c.webDavCloseWindow=siteConfig.cmdRegEx(cmd)
    return c



import utilityFunctions
import json
########################################################################################
# M3
########################################################################################

defaultSites=collections.OrderedDict()

defaultSites['M3 Early Adopters']  = getM3Config("m3-login.massive.org.au")
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=False,indent=4,separators=(',', ': '))
with open('m3_flavours_20160812.json','w') as f:
    f.write(jsons)

########################################################################################
# MASSIVE
########################################################################################

defaultSites=collections.OrderedDict()

defaultSites['m2 Desktop on m2-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login1.massive.org.au")
defaultSites['m2 Highmem Desktop (192G) on m2-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login1.massive.org.au","highmem")
defaultSites['m2 Desktop on m2-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login2.massive.org.au")
defaultSites['m2 Highmem Desktop (192G) on m2-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login2.massive.org.au","highmem")
defaultSites['m1 Desktop on m1-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m1-login1.massive.org.au")
defaultSites['m1 Desktop on m1-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m1-login2.massive.org.au")
#defaultSites['m1 Old Centos 5 Desktop on m1-login1.massive.org.au']  = getMassiveSiteConfig("m1-login1.massive.org.au")

# defaultSites['Centos 6 Desktop on m2-login3.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login3.massive.org.au")

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=False,indent=4,separators=(',', ': '))
with open('massive_flavours_20150417.json','w') as f:
    f.write(jsons)

########################################################################################
# MASSIVE using AS
########################################################################################

defaultSites=collections.OrderedDict()
defaultSites['m1 Beamline Desktop on m1-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m1-login1.massive.org.au")
defaultSites['m1 Beamline Desktop on m1-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m1-login2.massive.org.au")
defaultSites['m2 Desktop on m2-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login1.massive.org.au")
defaultSites['m2 Highmem Desktop (192G) on m2-login1.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login1.massive.org.au","highmem")
defaultSites['m2 Desktop on m2-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login2.massive.org.au")
defaultSites['m2 Highmem Desktop (192G) on m2-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login2.massive.org.au","highmem")

# defaultSites['Desktop on m1-login1.massive.org.au']  = getMassiveSiteConfig("m1-login1.massive.org.au")
# defaultSites['Desktop on m2-login1.massive.org.au'] = getMassiveSiteConfig("m2-login1.massive.org.au")
# defaultSites['Centos 6 Desktop on m2-login3.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login3.massive.org.au")
# defaultSites['Centos 6 Desktop on m1-login2.massive.org.au']  = getMassiveCentos6SiteConfig("m1-login2.massive.org.au")
# defaultSites['Centos 6 Highmem Desktop on m2-login3.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login3.massive.org.au","highmem")

for s in defaultSites.keys():
    defaultSites[s].authURL='https://autht.massive.org.au/ASync'
    defaultSites[s].oauthclient='strudel'
    defaultSites[s].oauthclientpasswd=''
    defaultSites[s].visibility['usernamePanel']=False
    defaultSites[s].visibility['projectPanel']=False

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=False,indent=4,separators=(',', ': '))
with open('massive_as_flavours_20150417.json','w') as f:
    f.write(jsons)
########################################################################################
# MASSIVE using AS Portal
########################################################################################

defaultSites=collections.OrderedDict()
defaultSites['Desktop on m1-login2.massive.org.au']  = getMassiveSiteConfig("m1-login2.massive.org.au") 
defaultSites['Desktop on m2-login2.massive.org.au'] = getMassiveSiteConfig("m2-login2.massive.org.au") 
defaultSites['Desktop on m1-login1.massive.org.au']  = getMassiveSiteConfig("m1-login1.massive.org.au") 
defaultSites['Desktop on m2-login1.massive.org.au'] = getMassiveSiteConfig("m2-login1.massive.org.au")
defaultSites['Centos 6 Desktop (For Eval Users) on m2-login3.massive.org.au']  = getMassiveCentos6SiteConfig("m2-login3.massive.org.au")


for s in defaultSites.keys():
    defaultSites[s].authURL='https://autht.massive.org.au/ASync'
    defaultSites[s].oauthclient='massive_imbl'
    defaultSites[s].oauthclientpasswd='m1mo4MedicBL'

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=False,indent=4,separators=(',', ': '))
with open('massive_as_portal_flavours_20141203.json','w') as f:
    f.write(jsons)


########################################################################################
# CVL with AAF 
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['CVL Desktop']=  getCVLSiteConfigXML("batch")
defaultSites['Huygens on the CVL']= getCVLSiteConfigXML("huygens")
defaultSites['CVL GPU node']= getCVLSiteConfigXML("vis")
multicpu=getCVLSiteConfigXML("multicpu")
cmd="\"module load pbs ; module load maui ; echo \'module load pbs ; /usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  qsub -q multicpu -l nodes=1:ppn=16 -l walltime={hours}:00:00 -N desktop_{username} -o .vnc/ -e .vnc/ \""
regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"
multicpu.startServer=siteConfig.cmdRegEx(cmd,regex)
defaultSites['CVL 16 core node']=multicpu
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('cvl_aaf_flavours_20140419.json','w') as f:
    f.write(jsons)

    
########################################################################################
# BPA with password
########################################################################################
cmd="\"module load pbs ; module load maui ; module load turbovnc ; mkdir ~/.vnc/ 2>/dev/null ; rm -f ~/.vnc/clearpass ; touch ~/.vnc/clearpass ; chmod 600 ~/.vnc/clearpass ; passwd=\"\'$\'\"( dd if=/dev/urandom bs=1 count=8 2>/dev/null | md5sum | cut -b 1-8 ) ; echo \"\'$\'\"passwd > ~/.vnc/clearpass ; cat ~/.vnc/clearpass | vncpasswd -f > ~/.vnc/passwd ; chmod 600 ~/.vnc/passwd ; echo \' /opt/TurboVNC/bin/vncserver -geometry {resolution} -xstartup /usr/local/bin/xstartup ; /usr/local/bin/git_clone_or_pull.sh https://github.com/swcarpentry/bc.git ; cd bc/novice/python ; ipython notebook --no-browser & sleep 36000000 \' |  qsub -q %s -l nodes=1:ppn=2 -l walltime={hours}:00:00 -N desktop_{username} -o .vnc/ -e .vnc/ \""%'carpentry'
regex="^(?P<jobid>(?P<jobidNumber>[0-9]+)\.\S+)\s*$"

defaultSites=collections.OrderedDict()

defaultSites['SWC Desktop']=  getCVLSiteConfigXML("carpentry")
defaultSites['SWC Desktop'].authURL=None
defaultSites['SWC Desktop'].defaults['jobParams_ppn']=2
defaultSites['SWC Desktop'].defaults['jobParams_nodes']=1
defaultSites['SWC Desktop'].defaults['jobParams_hours']=4
defaultSites['SWC Desktop'].startServer=siteConfig.cmdRegEx(cmd,regex)
defaultSites['SWC Desktop'].otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
defaultSites['SWC Desktop'].tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -L 8888:localhost:8888 -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

defaultSites['SWC Desktop with AAF']=  getCVLSiteConfigXML("carpentry")
defaultSites['SWC Desktop with AAF'].authURL="https://autht.massive.org.au/cvl/"
defaultSites['SWC Desktop with AAF'].defaults['jobParams_ppn']=2
defaultSites['SWC Desktop with AAF'].defaults['jobParams_nodes']=1
defaultSites['SWC Desktop with AAF'].defaults['jobParams_hours']=4
defaultSites['SWC Desktop with AAF'].startServer=siteConfig.cmdRegEx(cmd,regex)
defaultSites['SWC Desktop with AAF'].otp= siteConfig.cmdRegEx('\'cat ~/.vnc/clearpass\'','^(?P<vncPasswd>\S+)$')
defaultSites['SWC Desktop with AAF'].tunnel=siteConfig.cmdRegEx('{sshBinary} -A -c {cipher} -t -t -oStrictHostKeyChecking=no -L {localPortNumber}:localhost:{remotePortNumber} -L 8888:localhost:8888 -l {username} {execHost} "echo tunnel_hello; bash"','tunnel_hello',async=True)

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('bpa.json','w') as f:
    f.write(jsons)

########################################################################################
# Other
########################################################################################
defaultSites=collections.OrderedDict()
c=getOtherTurboVNCConfig("")
c.visibility['loginHostPanel']=False
c.loginHost='118.138.255.32'
defaultSites['NeCTAR GPU']=c

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('fixed_gpu_flavour.json','w') as f:
    f.write(jsons)

########################################################################################
# Other
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['Other']=getGenericVNCSession()
defaultSites['Other TurboVNC']=getOtherTurboVNCConfig("")
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('other_flavour.json','w') as f:
    f.write(jsons)

########################################################################################
# OzViz
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['TurboVNC OzViz']=getTurboVNCConfigOzViz("")
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('ozviz_flavour.json','w') as f:
    f.write(jsons)

##### BMRI Host Definitions ####
defaultSites=collections.OrderedDict()
standard=getBMRIVNCConfig("batch")
standard.authURL=None
gpu=getBMRIVNCConfig("viznode")
gpu.authURL=None
defaultSites['BMRI Viznode']=gpu
defaultSites['BMRI Standard']=standard
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('bmri.json','w') as f:
    f.write(jsons)

##### CQU Host Definitions #####

defaultSites=collections.OrderedDict()
gpu=getCQUGPUConfig("")
gpu.authURL=None
standard=getCQUStandardVNCConfig("")
standard.authURL=None
newton=getCQUVNCSession()
newton.authURL=None
newton.visibility['loginHostPanel']=False
newton.loginHost="newton.cqu.edu.au"
isaac=getCQUVNCSession()
isaac.authURL=None
isaac.visibility['loginHostPanel']=False
isaac.loginHost="isaac.cqu.edu.au"
defaultSites['HPC Login Node - Isaac']=isaac
defaultSites['HPC Login Node - Newton']=newton
defaultSites['GPU Interactive Session']=gpu
defaultSites['Standard Interactive Session']=standard
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('cqu-v2.json','w') as f:
    f.write(jsons)

##### CQU Host Definitions #####

########################################################################################
# NCI
########################################################################################
defaultSites=collections.OrderedDict()
raijinExpress=getRaijinSiteConfig('express')
defaultSites['Raijin (Express Queue)'] = raijinExpress
defaultSites['Raijin (Login node raijin1)'] = getRaijinLoginSiteConfig('raijin1.nci.org.au')
defaultSites['Raijin (Login node raijin2)'] = getRaijinLoginSiteConfig('raijin2.nci.org.au')
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('nci_flavours.json','w') as f:
    f.write(jsons)

########################################################################################
# CVL Desktopdev
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['CVL DesktopDev']=  getCVLSiteConfigXML("desktopdev")
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('cvl_dev_flavours.json','w') as f:
    f.write(jsons)

########################################################################################
# CVL Slurm
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['CVL Default']=  getCVLSiteConfigSlurm("batch")
defaultSites['CVL Large Node']=  getCVLSiteConfigSlurm("compute")
defaultSites['CVL Vis Node']=  getCVLSiteConfigSlurm("vis")
defaultSites['CVL Huygens']=  getCVLSiteConfigSlurm("huygens")
defaultSites['CVL Large Node'].defaults['jobParams_ppn']=16
defaultSites['CVL Large Node'].siteRanges['jobParams_ppn']=[1,64]
for s in defaultSites.keys():
    defaultSites[s].authURL=None

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('m2cvl.json','w') as f:
    f.write(jsons)
########################################################################################
# CVL Slurm AAF
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['CVL Default']=  getCVLSiteConfigSlurm("batch")
defaultSites['CVL Large Node']=  getCVLSiteConfigSlurm("compute")
defaultSites['CVL Vis Node']=  getCVLSiteConfigSlurm("vis")
defaultSites['CVL Huygens']=  getCVLSiteConfigSlurm("huygens")
defaultSites['CVL Large Node'].defaults['jobParams_ppn']=16
defaultSites['CVL Large Node'].siteRanges['jobParams_ppn']=[1,64]
for s in defaultSites.keys():
    defaultSites[s].authURL="https://autht.massive.org.au/m2cvl/"
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('m2cvl_aaf.json','w') as f:
    f.write(jsons)

########################################################################################
# CVL Reservations
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['CVL Default']=  getCVLSiteConfigSlurm("batch")
regex="^\s*ReservationName=(?P<name>\S+) (?P<desc>.*)$"
defaultSites['CVL Default'].listReservations = siteConfig.cmdRegEx(cmd="/opt/slurm-14.11.1/bin/scontrol show res | grep -B 2 Users={username} |   sed 's/--/BBBBBBB/' | tr '\\n' ' ' | sed 's/BBBBBBB/\\n/'",regex=[regex])
defaultSites['CVL Default'].createReservation = siteConfig.cmdRegEx(cmd="sudo /opt/slurm-14.11.1/bin/scontrol create reservation starttime={starttime} duration={duration} users={username} account=cvl NodeCnt={nodes} ReservationName={resname}")
defaultSites['CVL Default'].deleteReservation = siteConfig.cmdRegEx(cmd="sudo /opt/slurm-14.11.1/bin/scontrol delete ReservationName={ReservationName}")
defaultSites['CVL Default'].visibility['manageResButton'] = True
defaultSites['CVL Default'].sitetz="UTC"
partition="batch"
cmd="\" echo -e \'#!/bin/bash\\n/usr/local/bin/vncsession --vnc turbovnc --geometry {resolution} ; sleep 36000000 \' |  sbatch -p %s -N {nodes} --time={hours}:00:00 -J desktop_{username} -o .vnc/slurm-%%j.out --reservation={resname}\""%partition
regex="^Submitted batch job (?P<jobid>(?P<jobidNumber>[0-9]+))$"
defaultSites['CVL Default'].startServer=siteConfig.cmdRegEx(cmd,regex)

keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('m2cvl_reservations.json','w') as f:
    f.write(jsons)

########################################################################################
# Generic Slurm
########################################################################################
defaultSites=collections.OrderedDict()
c=getSiteConfigSlurm("monarch.erc.monash.edu.au","highspeed,highcore")
c.defaults['jobParams_hours']=24
c.defaults['jobParams_ppn']=4
defaultSites['MonARCH CentOS 7 General']=c
c=getSiteConfigSlurm("monarch.erc.monash.edu.au","highcore")
c.defaults['jobParams_hours']=24
c.defaults['jobParams_ppn']=4
defaultSites['MonARCH CentOS 7 (Highcore)']=c
c=getSiteConfigSlurm("monarch.erc.monash.edu.au","highspeed")
c.defaults['jobParams_hours']=24
c.defaults['jobParams_ppn']=4
defaultSites['MonARCH CentOS 7 (Highspeed)']=c
c=getSiteConfigSlurm("monarch.erc.monash.edu.au","ubuntu")
c.defaults['jobParams_hours']=24
c.defaults['jobParams_ppn']=4
defaultSites['MonARCH Ubuntu 14.04']=c
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('monarch_20160304.json','w') as f:
    f.write(jsons)

########################################################################################
# Generic Slurm
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['GenericDesktops']=  getCVLSiteConfigSlurm("batch")
defaultSites['GenericDesktops'].loginHost="{{ loginNode }}"
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('generic_slurm_flavours.json','w') as f:
    f.write(jsons)

########################################################################################
# EPCC with lsf
########################################################################################
defaultSites=collections.OrderedDict()
defaultSites['Indy Desktop']=  getEPCCSiteConfig("")
defaultSites['Indy Desktop'].authURL=None
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('epcc_flavours.json','w') as f:
    f.write(jsons)


########################################################################################
# NeCTAR VM
########################################################################################
defaultSites=collections.OrderedDict()
NeCTARconfig=getGenericVNCSession()
NeCTARconfig.loginHost=None
NeCTARconfig.imageid='ami-00002fa3'
NeCTARconfig.username='ec2-user'
NeCTARconfig.instanceFlavour='m1.small'
NeCTARconfig.provision='NeCTAR'
NeCTARconfig.visibility['usernamePanel']=False
NeCTARconfig.visibility['loginHostPanel']=False

defaultSites['NeCTAR CentOS 6.5 VM']=NeCTARconfig
keys=defaultSites.keys()
jsons=json.dumps([keys,defaultSites],cls=siteConfig.GenericJSONEncoder,sort_keys=True,indent=4,separators=(',', ': '))
with open('other_nectar.json','w') as f:
    f.write(jsons)
