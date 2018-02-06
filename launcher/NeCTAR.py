import Provision
import time
import threading
import Queue
import wx
import HTMLParser
import utilityFunctions
import boto
# This doesn't seem to affect all versions of the boto module, but some
# try to load endpoints.json. py2app does not include this in the 
# resources at a meaningful location
if boto.__dict__.has_key('ENDPOINTS_PATH'):
    import os.path
    if not os.path.isfile(boto.ENDPOINTS_PATH):
        boto.ENDPOINTS_PATH='endpoints.json'
from boto.ec2.connection import EC2Connection
from boto.ec2.regioninfo import *

class VMNameDialog(wx.Dialog):
    def __init__(self,*args,**kwargs):
        super(VMNameDialog, self).__init__(*args, **kwargs)
        self.SetSizer(wx.BoxSizer())
        p=wx.Panel(self)
        s=wx.FlexGridSizer(2,2)
        p.SetSizer(s)
        s.Add(wx.StaticText(p,wx.ID_ANY,label="VM Name"))
        s.Add(wx.TextCtrl(p,wx.ID_ANY,name='vmname'))
        ok=wx.Button(p,wx.ID_OK,'OK')
        cancel=wx.Button(p,wx.ID_CANCEL,'Cancel')
        ok.Bind(wx.EVT_BUTTON, self.onClose)
        cancel.Bind(wx.EVT_BUTTON, self.onClose)
        s.Add(ok)
        s.Add(cancel)
        self.GetSizer().Add(p)
        self.Fit()

    def onClose(self,e):
        self.EndModal(e.GetId())

    def getName(self):
        return self.FindWindowByName('vmname').GetValue()

class Provision(Provision.Provision):

    class ProjectParser(HTMLParser.HTMLParser):
        def __init__(self,*args,**kwargs):
            HTMLParser.HTMLParser.__init__(self)
            self.processing=False
            self.projects=[]
            self.href=None

        def handle_starttag(self,tag,attrs):
            if tag == 'ul':
                for attr in attrs:
                    if attr[0]=='id' and attr[1]=='tenant_list':
                        self.processing=True
            if self.processing and tag == 'a':
                for attr in attrs:
                        if attr[0]=='href':
                            self.href=attr[1]

        def handle_data(self,data):
            if self.processing:
                if self.href!=None:
                    self.projects.append((self.href,data))

        def handle_endtag(self,tag):
            self.href=None
            if tag == 'ul':
                self.processing=False
            pass

    def loginNeCTAR(self,**kwargs):
        import cvlsshutils.RequestsSessionSingleton
        import cvlsshutils.AAF_Auth
        # Use of a singleton here means that we should be able to do SSO on any AAF/Shibolleth web service. However we might have to guess the IdP.
        self.session=cvlsshutils.RequestsSessionSingleton.RequestsSessionSingleton().GetSession()
        destURL="https://dashboard.rc.nectar.org.au/project"
        #destURL="https://accounts.rc.nectar.org.au/rcshibboleth/"
        auth=cvlsshutils.AAF_Auth.AAF_Auth(self.session,destURL,postFirst="https://dashboard.rc.nectar.org.au/auth/login",progressDialog=self.progressDialog,parent=self.notify_window,aaf_idp=self.aaf_idp,aaf_username=self.aaf_username,**kwargs)
        wx.CallAfter(self.progressDialog.Show,False)
        auth.auth_cycle()
        wx.CallAfter(self.progressDialog.Show,True)
        self.updateDict=auth.getUpdateDict()
#        r=self.session.get('https://dashboard.rc.nectar.org.au/auth/login',verify=False)

    def getProjects(self):
        url='https://dashboard.rc.nectar.org.au/project/'
        r=self.session.get(url,verify=False)
        p=Provision.ProjectParser()
        p.feed(r.text)
        self.projects=p.projects

    def createAndShowModalDialog(self,q,dlgclass,progressDialog=None,event=None,*args,**kwargs):
        if progressDialog!=None:
            progressDialog.Show(False)
        dlg=dlgclass(*args,**kwargs)
        try:
            wx.EndBusyCursor()
        except:
            pass
        r=dlg.ShowModal()
        if progressDialog!=None:
            progressDialog.Show(True)
        try:
            wx.BeginBusyCursor()
        except:
            pass
        q.put((r,dlg))
        if event!=None:
            event.set()

    def okCallback(self,listSelectionItem):
        self.targetProject = listSelectionItem.GetText()
    def queryProject(self):
        cancelCallback=lambda x: self.cancel(x)
        grouplist=[]
        for t in self.projects:
            grouplist.append(t[1])
        q=Queue.Queue()


        msg="Please select from the list of projects"
        wx.CallAfter(self.createAndShowModalDialog,q,utilityFunctions.ListSelectionDialog,parent=self.notify_window, progressDialog=self.progressDialog, title=self.notify_window.GetParent().programName, headers=None, message=msg, noSelectionMessage="Please select a project from the list.", items=grouplist, okCallback=self.okCallback, cancelCallback = cancelCallback, style=wx.DEFAULT_DIALOG_STYLE, helpEmailAddress="")

        (r,dlg) = q.get()
        wx.CallAfter(dlg.Destroy)
        for t in self.projects:
            if t[1]==self.targetProject:
                switchURL="https://dashboard.rc.nectar.org.au/%s"%t[0]
        self.session.get(switchURL,verify=False)
    def getEC2Creds(self):
        import tempfile
        import os
        url="https://dashboard.rc.nectar.org.au/project/access_and_security/api_access/ec2/"
        self.ec2path = tempfile.mkdtemp()

        done=False
        while not done:
            try:
                r=self.session.get(url,verify=False,stream=True)
                done=True
            except:
                logger.debug("time out getting ec2 creds")
        with open(os.path.join(self.ec2path,"ec2.zip"),'w') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        import zipfile
        try:
            with zipfile.ZipFile(os.path.join(self.ec2path,"ec2.zip"),'r') as zf:
                for fn in zf.namelist():
                    with zf.open(fn,'r') as fin:
                        with open(os.path.join(self.ec2path,fn),'wb') as fout:
                            fout.write(fin.read())
        except Exception as e:
            raise Exception("Couldn't open zip file %s: %s"%(os.path.join(self.ec2path,"ec2.zip"),e))
        try:
            import re
            import os
            with open(os.path.join(self.ec2path,"ec2rc.sh"),'r') as f:
                for line in f.readlines():
                    match = re.search('export (?P<varname>\S+)=(?P<value>\S+)\s|$',line)
                    if match!=None and match.groupdict()['varname']!=None:
                        if match.groupdict()['varname'] == 'EC2_ACCESS_KEY':
                            self.ec2_access_key=match.groupdict()['value']
                        if match.groupdict()['varname'] == 'EC2_SECRET_KEY':
                            self.ec2_secret_key=match.groupdict()['value']
        except Exception as e:
            import traceback
            logger.debug(traceback.format_exc())
            logger.debug(e)
            raise e



    def removeEC2Creds(self):
        from logger.Logger import logger
        import shutil
        try:
            shutil.rmtree(self.ec2path, ignore_errors=True)
        except:
            logger.debug("unable to remove ec2 credentials")

    def connect(self):

        region = RegionInfo(name="NeCTAR", endpoint="nova.rc.nectar.org.au")
        self.connection = boto.connect_ec2(aws_access_key_id=self.ec2_access_key,
                    aws_secret_access_key=self.ec2_secret_key,
                    is_secure=True,
                    region=region,
                    validate_certs=False,
                    port=8773,
                    path="/services/Cloud")
                
    def getInstances(self,keyname=None):
        # Get a list of VMs that match a) the image name b) the flavour c) the keypair
        try:
            self.instances=[]
            reservations = self.connection.get_all_reservations()
            for res in reservations:
                for instance in res.instances:
                    if instance.image_id == self.imageid:
                        if keyname !=None and keyname == instance.key_name:
                            self.instances.append(instance)
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.debug(e)

    def getInstanceDetails(self):
        self.getInstances(keyname=self.ec2key.name)
        self.instance=None
        for i in self.instances:
            if i.tags.has_key('Name') and i.tags['Name'] == self.vmName:
                self.instance = i
            elif i.private_dns_name == self.vmName:
                self.instance = i
        if self.instance == None:
            return {}
        update={}
        update['loginHost']=self.instance.ip_address
        update['username']=self.username
        return update

    def queryConnect(self):
        pass


    def userCancel(self,error=""):
        self.progressDialog.Show(False)
        self.cancel(error)

    def cancel(self,error):
        from logger.Logger import logger
        logger.debug(error)
        wx.CallAfter(self.progressDialog.Show,False)
        self._canceled.set()

    def __init__(self,jobParams=None,keyModel=None,imageid=None,instanceFlavour=None,username=None,*args,**kwargs):
        super(self.__class__,self).__init__(*args,**kwargs)
        self.jobParams=jobParams
        self.keyModel=keyModel
        self._canceled=threading.Event()
        self.instance=None
        self.instances=[]
        self.bootNew=False
        self.imageid=imageid
        self.instanceFlavour=instanceFlavour
        self.username=username
        if self.jobParams.has_key('aaf_idp'):
            self.aaf_idp=self.jobParams['aaf_idp']
        else:
            self.aaf_idp=None
        if self.jobParams.has_key('aaf_username'):
            self.aaf_username=self.jobParams['aaf_username']
        else:
            self.aaf_username=None

    def createProgressDialog(self,q):
        import launcher_progress_dialog
        p=launcher_progress_dialog.LauncherProgressDialog(self.notify_window, wx.ID_ANY, "Creating VM", "", 4, True,self.userCancel)
        q.put(p)

    def getKeyPairByFP(self,kmfingerprint):
        # list the keypairs already associated with this tenant. If any of them matches the public key in the keymodel this is the one to use
        # If non of them match the pub key in the keymodel, upload the new pubkey
        keypairs=self.connection.get_all_key_pairs()
        for k in keypairs:
            if k.fingerprint==kmfingerprint:
                return k
        return None

    def getKeyPairByName(self,keyName):
        # list the keypairs already associated with this tenant. If any of them matches the public key in the keymodel this is the one to use
        # If non of them match the pub key in the keymodel, upload the new pubkey
        keypairs=self.connection.get_all_key_pairs()
        for k in keypairs:
            if k.name==keyName:
                return k
        return None

    def setKeyPair(self,keyName,pubKey):
        self.connection.import_key_pair(keyName,pubKey)
        keypairs=self.connection.get_all_key_pairs()
        for k in keypairs:
            if k.name==keyName:
                return k

    def queryExisting(self):
        import LauncherOptionsDialog
        import dialogtext
        from logger.Logger import logger
        dialogs=dialogtext.default()
        #  ask if the user would like to start a new VM or connect to an existing one.
        done=False
        okCallback=lambda x: setattr(self,'vmName',x.GetText())
        cancelCallback=lambda x: setattr(self,'vmName',None)
        self.vmName=None
        try:
            grouplist=[]
            for i in self.instances:
                if i.tags.has_key('Name'):
                    grouplist.append(i.tags['Name']) 
                else:
                    grouplist.append(i.private_dns_name)
            while not done:
                q=Queue.Queue()
                e=threading.Event()
                wx.CallAfter(self.createAndShowModalDialog,event=e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self.notify_window,message=dialogs.existingVM.message,ButtonLabels=dialogs.existingVM.ButtonLabels,title="",q=q)
                e.wait()
                (r,dlg)=q.get()
                if r==0:
                    done=True
                    self.bootNew=False
                if r==1:
                    e.clear()
                    msg="Please select a VM to connect to"
                    wx.CallAfter(self.createAndShowModalDialog,q,utilityFunctions.ListSelectionDialog,parent=self.notify_window, progressDialog=self.progressDialog, title=self.notify_window.GetParent().programName, headers=None, message=msg, noSelectionMessage="Please select a VM from the list or cancel.", items=grouplist, okCallback=okCallback, cancelCallback = cancelCallback, style=wx.DEFAULT_DIALOG_STYLE, helpEmailAddress="")
                    (r,dlg) = q.get()
                    if self.vmName!=None:
                        done=True
                    self.bootNew=False
                if r==2:
                    self.bootNew=True
                    done=True
                    e.clear()
        except Exception as e:
            logger.debug(traceback.format_exc())
            logger.debug(e)

    def bootVM(self):
        import time
        # as the user to name the VM, then boot with the supplied image name flavour availabilty_zone and keypair
        q=Queue.Queue()
        wx.CallAfter(self.createAndShowModalDialog,q,VMNameDialog,parent=self.notify_window, progressDialog=self.progressDialog, title=self.notify_window.GetParent().programName, style=wx.DEFAULT_DIALOG_STYLE )
        (r,dlg) = q.get()
        if r==wx.ID_OK:
            self.vmName=dlg.getName()
            # now we are ready to boot
            reservation=self.connection.run_instances(self.imageid,key_name=self.ec2key.name,instance_type=self.instanceFlavour,placement='monash-01',security_groups=['default'])
            self.instance=reservation.instances[0]
            status = self.instance.update()
            while status != 'running':
                time.sleep(1)
                status = self.instance.update()
            self.instance.add_tag('Name',self.vmName)
        else:
            raise Exception("User canceled the process of booting their own VM")

    def deleteInstance(self):
        self.connection.terminate_instances(instance_ids=[self.instance.id])

    def shutdown(self):
        import LauncherOptionsDialog
        import dialogtext
        dialogs=dialogtext.default()
        q=Queue.Queue()
        e=threading.Event()
        if (self.instance!=None):
            wx.CallAfter(self.createAndShowModalDialog,event=e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self.notify_window,message=dialogs.shutdownInstance.message,ButtonLabels=dialogs.shutdownInstance.ButtonLabels,title="",q=q)
            e.wait()
            (r,dlg)=q.get()
            if r==0:
                self.deleteInstance()

    def run(self,callback,failcallback):
        from logger.Logger import logger
        q=Queue.Queue()
        wx.CallAfter(self.createProgressDialog,q)
        self.progressDialog=q.get()
        logger.debug("Running NeCTAR Provisioning")
        try:
            wx.CallAfter(self.progressDialog.Update,0, "Logging into NeCTAR Dashboard")
            if not self._canceled.isSet():
                self.loginNeCTAR()
            wx.CallAfter(self.progressDialog.Update,1, "Getting a list of your NeCTAR Projects")
            if not self._canceled.isSet():
                self.getProjects()
            if not self._canceled.isSet():
                self.queryProject()
            wx.CallAfter(self.progressDialog.Update,2, "Getting Cloud Credentials")
            if not self._canceled.isSet():
                try:
                    self.getEC2Creds()
                    self.removeEC2Creds()
                    self.connect()
                except Exception as e:
                    import traceback
                    logger.debug(traceback.format_exc())
                    raise e

            if not self._canceled.isSet():
                self.ec2key=self.getKeyPairByFP(self.keyModel.getFingerprint())
                if self.ec2key==None:
                    tmpkey=self.getKeyPairByName("%s_%s"%(self.keyModel.sshpaths.keyFileName,self.ec2_access_key))
                    if tmpkey==None:
                        self.ec2key=self.setKeyPair("%s_%s"%(self.keyModel.sshpaths.keyFileName,self.ec2_access_key),self.keyModel.getPubKey())
                    else:
                        logger.debug("A keypair exists with my default name, but its fingerprint doesn't match. Deleting and recreating")
                        self.connection.delete_key_pair("%s_%s"%(self.keyModel.sshpaths.keyFileName,self.ec2_access_key))
                        self.ec2key=self.setKeyPair("%s_%s"%(self.keyModel.sshpaths.keyFileName,self.ec2_access_key),self.keyModel.getPubKey())
            wx.CallAfter(self.progressDialog.Update,3, "Getting a list of VMs you can connect to")
            if not self._canceled.isSet():
                self.getInstances(keyname=self.ec2key.name)
            if not self._canceled.isSet():
                if len(self.instances)>0:
                    self.queryExisting()
                else:
                    self.bootNew=True
            if not self._canceled.isSet():
                if self.bootNew==True:
                    wx.CallAfter(self.progressDialog.Update,3, "Booting a new Instance")
                    self.bootVM()
            if not self._canceled.isSet():
                self.updateDict.update(self.getInstanceDetails())
            wx.CallAfter(self.progressDialog.Show,False)
            callback()
        except Exception as e:
            import traceback
            logger.debug(traceback.format_exc())
            logger.debug(e)
            self.cancel(traceback.format_exc())
            failcallback()

