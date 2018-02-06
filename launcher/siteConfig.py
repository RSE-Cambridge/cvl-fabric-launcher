import json
import sys
import os
import collections
import requests
from logger.Logger import logger
from threading import *
import Queue

def getMasterSites(url):
    logger.debug("Getting the master list of all known sites/HPC installations")
    r=requests.get(url,verify=False)
    if r.status_code==200:
        logger.debug("loading master sites %s"%r.text)
        return json.loads(r.text)
    else:
        logger.debug("Master site list unavailable status code %s"%r.status_code)
        return "%s"%r.status_code
    
class CancelException(Exception):
    pass
class TimeoutException(Exception):
    pass
class StatusCode(Exception):
    pass
    
class requestThread(Thread):
    def __init__(self,url,queue):
        super(requestThread,self).__init__()
        self.url=url
        self.queue=queue
        
    def run(self):
        import time
        try:
            req=requests.get(self.url,verify=False)
            if req.status_code == 200:
                self.queue.put([self.url,req.text])
            else:
                self.queue.put([self.url,None])
        except:
            self.queue.put([self.url,None])

# this thread will wait until either it has pulled nthreads items of the queue, or it has pulled a None object off the queue.
class waitThread(Thread):
    def __init__(self,qin,res,nthreads):
        super(waitThread,self).__init__()
        self.qin=qin
        self.res=res
        self.nthreads=nthreads

    def run(self):
        if self.nthreads > 0:
            r=self.qin.get()
            results=0
            while r!=None:
                results=results+1
                if r[1]!=None:
                    self.res[r[0]] = r[1]
                if results<self.nthreads:
                    r=self.qin.get()
                else:
                    r=None
        
# This thread will place a none object on the queue after a specified time to terminate the wait thread above
class timerThread(Thread):
    def __init__(self,q,time):
        super(timerThread,self).__init__()
        self.q=q
        self.time=time
    
    def run(self):
        import time
        time.sleep(self.time)
        self.q.put(None)

# This thread will allow the requstThreads to run indefinitly and write the output to the cache.
# It should only apply if the file didn't download within the time limit
class backgroundDownloadThread(Thread):
    def __init__(self,q,nthreads,path):
        super(backgroundDownloadThread,self).__init__()
        self.q=q
        self.nthreads=nthreads
        self.path=path

    def run(self):
        import os
        import hashlib
        nres=0
        while nres<self.nthreads:
            r=self.q.get()
            nres=nres+1
            if r[1]!=None:
                filename=os.path.join(self.path,hashlib.md5(r[0]).hexdigest())
                with open(filename,'w') as f:
                    logger.debug("retrieved site %s in a background download"%r[0])
                    f.write(r[1])

def getSites(prefs,path):
    import time
    logger.debug("getting a list of sites")
    siteTupleList=[]
    siteList=[]
    if prefs.has_section('configured_sites'):
        l=prefs.options('configured_sites')
        for s in l:
            if 'siteurl' in s:
                site=prefs.get('configured_sites',s)
                number=int(s[7:])
                enabled=prefs.get('configured_sites','siteenabled%i'%number)
                if enabled=='True':
                    siteTupleList.append((site,number))
    siteTupleList.sort(key=lambda t:t[1])
    for s in siteTupleList:
        siteList.append(s[0])

    r=collections.OrderedDict()
    q=Queue.Queue()
    backgroundQ=Queue.Queue()
    nthreads=0
    for site in siteList:
        requestThread(site,q).start()
        nthreads=nthreads+1
    timerThread(q,10).start()
    foundSites={}
    t=waitThread(q,foundSites,nthreads)
    t.start()
    t.join()

    
    nback=0
    for site in siteList:
        logger.debug("retrieving the config for %s"%site)
        try:
            import hashlib
            import os
            filename=os.path.join(path,hashlib.md5(site).hexdigest())
            if site in foundSites.keys():
                text=foundSites[site]
                with open(filename,'w') as f:
                    f.write(text)
                newSites=GenericJSONDecoder().decode(text)
            else:
                logger.debug("didn't download site %s within the time limit. Trying for the cache"%site)
                logger.debug("enqueing site %s for background download"%site)
                requestThread(site,backgroundQ).start()
                nback=nback+1
                with open(filename,'r') as f:
                    newSites=GenericJSONDecoder().decode(f)
            if (isinstance(newSites,list)):
                keyorder=newSites[0]
                # We don't want two sites to use the same name for two of their menu items, but if they do, we should alter the name of one of them.
                for key in keyorder:
                    nk = key
                    i=1
                    while nk in r.keys():
                        i=i+1
                        nk = key+" %s"%i
                    r[nk]=newSites[1][key]
        except Exception as e:
            try:
                with open(filename,'r') as f:
                    newSites=GenericJSONDecoder().decode(f.read())
                if (isinstance(newSites,list)):
                    keyorder=newSites[0]
                    for key in keyorder:
                        r[key]=newSites[1][key]
            except Exception as e:
                logger.debug("error retrieving the config for %s"%site)
                logger.debug("%s"%e)
    backgroundDownloadThread(backgroundQ,nback,path).start()
    return r
        
        

#    DEFAULT_SITES_JSON='defaultSites.json'
#    defaultSites={}
#    with open(DEFAULT_SITES_JSON,'r') as f:
#        defaultSites=GenericJSONDecoder().decode(f.read())
#    if (isinstance(defaultSites,list)):
#        keyorder=defaultSites[0]
#        r=collections.OrderedDict()
#        for key in keyorder:
#            r[key]=defaultSites[1][key]
#        defaultSites=r
#    return defaultSites

class sshKeyDistDisplayStrings(object):
    def __init__(self,**kwargs):
        self.passwdPrompt="Please enter your password"
        self.passwdPromptIncorrect="Sorry that password was incorrect. Please reenter"
        self.passphrasePrompt="Please enter the passphrase for you ssh key"
        self.passphrasePromptIncorrectl="Sorry, that passphrase was incorrect. Please enter the passphrase for your ssh key"
        self.newPassphraseEmptyForbidden="Sorry, you can't use an empty passphrase. Please enter a new passphrase"
        self.newPassphraseTooShort="Sorry, the passphrase must be at least six character long. Please enter a new passphrase"
        self.newPassphraseMismatch="Sorry, the passphrases don't match. Please enter a new passphrase"
        self.newPassphrase="Please enter a new passphrase"
        self.newPassphraseTitle="Please enter a new passphrase"
        self.temporaryKey="""
Would you like to use the launchers old behaviour (entering a password every time you start a new desktop) or try the new behaviour (creating an ssh key pair and entering a passphrase the first time you use the launcher after reboot.)

Passwords are recomended if this is a shared user account.

SSH Keys are recommended if you are the only person who uses this account.

This option can be changed from the Identity menu.
"""
        self.temporaryKeyYes="Use my password every time"
        self.temporaryKeyNo="Use my SSH Key"
        self.qdelQueuedJob="""It looks like you've been waiting for a job to start.
Do you want me to delete the job or leave it in the queue so you can reconnect later?
"""
        self.qdelQueuedJobQdel="Delete the job"
        self.qdelQueuedJobNOOP="Leave it in the queue (I'll reconnect later)"
        self.persistentMessage="Would you like to leave your current session running so that you can reconnect later?\nIt has {timestring} remaining."
        self.persistentMessageStop="Stop the desktop"
        self.persistentMessagePersist="Leave it running"
        self.reconnectMessage="An Existing Desktop was found. It has {timestring} remaining. Would you like to reconnect or kill it and start a new desktop?"
        self.reconnectMessageYes="Reconnect"
        self.reconnectMessageNo="New desktop"
        self.createNewKeyDialogNewPassphraseMismatch="Passphrases don't match"
        self.networkError="It looks like a network error has occured. You may be able to resume your work by logging in again."
        self.helpEmailAddress="help@massive.org.au"
        self.onFirstLoginFailure="An unknown error occured. Please contact your site help desk."
        self.selectProjectMessage="You don\'t appear to be a member of the project {project}.\n\nPlease select from one of the following:"
        for key,value in kwargs.iteritems():
            self.__dict__[key]=value

# JSON Encoder and Decoder based on
# http://broadcast.oreilly.com/2009/05/pymotw-json.html
# json - JavaScript Object Notation Serializer
# By Doug Hellmann
# May 24, 2009
# Compiled regular expressions don't seem to conform to the "normal" pattern of having an obj.__class__.__name__ and obj.__module__
# Thus I have added specical case handling for regular expressions -- Chris Hines

class GenericJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        import re
        if isinstance(obj,type(re.compile(''))):
            d={'__class__':'__regex__','pattern':obj.pattern}
        else:
            d = { '__class__':obj.__class__.__name__, '__module__':obj.__module__, }
            d.update(obj.__dict__)
        return d

class GenericJSONDecoder(json.JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            if class_name == '__regex__':
                import re
                pattern=d.pop('pattern')
                return re.compile(pattern)
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            try:
                inst = class_(**args)
            except Exception as e:
                raise e
        else:
            inst = d
        return inst

class cmdRegEx():
    def __init__(self,cmd=None,regex=None,requireMatch=True,loop=False,async=False,host='login',failFatal=True,formatFatal=False,*args,**kwargs):

        self.cmd=cmd
        if (not isinstance(regex,list)):
            self.regex=[regex]
        else:
            self.regex=regex
        self.loop=loop
        self.async=async
        self.requireMatch=requireMatch
        if regex==None:
            self.requireMatch=False
        self.host=host
        if (self.async):
            self.host='local'
        self.failFatal=failFatal
        self.formatFatal=formatFatal

    def getCmd(self,jobParam={}):
        if ('exec' in self.host):
            sshCmd = '{sshBinary} -A -T -o PasswordAuthentication=no -o ChallengeResponseAuthentication=no -o KbdInteractiveAuthentication=no -o PubkeyAuthentication=yes -o StrictHostKeyChecking=no -l {username} {execHost} '
            # set marker line - this allows to ignore any output before the actual command
            sshCmd = sshCmd + ' \'(echo -e \"\\n----- strudel stdout start -----\");\' ' + ' \'(perl -e \"print STDERR \\"\\n----- strudel stderr start -----\\n\\"\");\' '
			# INFO: If we echo partly to stderr here (using >&2) all output will be send to stderr on windows.
			#       This is because redirection of streams is done by the client (windows) and windows does not support multiple redirections in one connection.
			#       Hence, redirection cannot be used with windows:
			#         ' \'(>&2 echo -e \"\\n----- strudel stderr start -----\"); \' '  
			#       We must write to stderr directly:
			#         ' \'python -c \"import os; os.write(2, \\"\\n----- strudel stderr start -----\\")\";\' '
			#         ' \'perl -e \"print STDERR \\"\\n----- strudel stderr start -----\\"\";\' '
			#       We choose perl as it is almost garantied to be installed on server side
        elif ('local' in self.host):
            sshCmd = ''
        else:
            sshCmd = '{sshBinary} -A -T -o PasswordAuthentication=no -o ChallengeResponseAuthentication=no -o KbdInteractiveAuthentication=no -o PubkeyAuthentication=yes -o StrictHostKeyChecking=yes -l {username} {loginHost} '
            # set marker line - this allows to ignore any output before the actual command (read detailed comment above)
            sshCmd = sshCmd + ' \'(echo -e \"\\n----- strudel stdout start -----\");\' ' + ' \'(perl -e \"print STDERR \\"\\n----- strudel stderr start -----\\n\\"\");\' '
        cmd=self.cmd
        if sys.platform.startswith("win"):
            escapedChars={'ampersand':'^&','pipe':'^|'}
        else:
            escapedChars={'ampersand':'&','pipe':'|'}
        formatdict = jobParam.copy()
        formatdict.update(escapedChars)
        if self.formatFatal:
            try:
                string=sshCmd.format(**formatdict).encode('ascii')+cmd.format(**formatdict).encode('ascii')
            except:
                raise Exception("I was unable to determine all the parameters in the command %s"%sshCmd)
        else:
            retry=True
            while retry:
                try:
                    string=sshCmd.format(**formatdict).encode('ascii')+cmd.format(**formatdict).encode('ascii')
                    retry=False
                except KeyError as e:
                    update={}
                    for a in e.args:
                        update[a]=''
                    formatdict.update(update)
                    retry=True

        return string

    def cleanupCmdOutput(self, stdout, stderr):    
                                   
        def cleanupSingleOutput(output, marker_line):
            
            # remove any line in stdout above the marker line set in getCmd()             
            output = output.splitlines()
            try:
                ii=output.index(marker_line) # exception ValueError if not found
                if not output[ii+1:]: 
                    output.append("")
                output = os.linesep.join(output[ii+1:])
            except ValueError:
                print "marker string not found"
                output = os.linesep.join(output[:])
            return output                                            

        stdout = cleanupSingleOutput(stdout, "----- strudel stdout start -----" )
        stderr = cleanupSingleOutput(stderr, "----- strudel stderr start -----" )     
        
        return stdout, stderr

class siteConfig():
    
    def __init__(self,**kwargs):
        self.provision=None
        self.imageid=None
        self.instanceFlavour=None
        self.loginHost=None
        self.username=None
        self.authURL=None
        self.listAll=cmdRegEx(failFatal=False)
        self.running=cmdRegEx()
        self.stop=cmdRegEx(failFatal=False)
        self.stopForRestart=cmdRegEx(failFatal=False)
        self.execHost=cmdRegEx()
        self.startServer=cmdRegEx()
        self.runSanityCheck=cmdRegEx(failFatal=False)
        self.setDisplayResolution=cmdRegEx(failFatal=False)
        self.getProjects=cmdRegEx(failFatal=False)
        self.showStart=cmdRegEx(failFatal=False)
        self.vncDisplay=cmdRegEx()
        self.otp=cmdRegEx()
        self.directConnect=cmdRegEx()
        self.messageRegexs=[]
        self.webDavIntermediatePort=cmdRegEx(failFatal=False)
        self.webDavRemotePort=cmdRegEx(failFatal=False)
        self.openWebDavShareInRemoteFileBrowser=cmdRegEx(failFatal=False)
        self.displayWebDavInfoDialogOnRemoteDesktop=cmdRegEx(failFatal=False)
        self.webDavTunnel=cmdRegEx(failFatal=False)
        self.onConnectScript=cmdRegEx(failFatal=False)
        self.agent=cmdRegEx()
        self.tunnel=cmdRegEx()
        self.listReservations = cmdRegEx(failFatal=False)
        self.createReservation = cmdRegEx(failFatal=False)
        self.deleteReservation = cmdRegEx(failFatal=False)
        self.visibility={}
        self.relabel={}
        self.siteRanges= {'jobParams_hours':[1,336], 'jobParams_mem':[1,1024], 'jobParams_nodes':[1,10], 'jobParams_ppn':[1,12] }
        self.defaults={}
        self.displayStrings=sshKeyDistDisplayStrings()
        self.authorizedKeysFile=None
        self.oauthclient=None
        self.oauthclientpasswd=None
        self.onFirstLogin=None
        self.sitetz="Australia/Melbourne"
        for key,value in kwargs.iteritems():
            self.__dict__[key]=value
