import threading
import wx
import logging
from StringIO import StringIO
import HTMLParser
import os
import time
import subprocess
import inspect
import sys
import itertools
import wx.lib.mixins.listctrl as listmix
import zipfile
import json

from logger.Logger import logger

LAUNCHER_URL = "https://www.massive.org.au/userguide/cluster-instructions/massive-launcher"

TURBOVNC_BASE_URL = "http://www.sourceforge.net/projects/turbovnc/files"

def parseMessages(regexs,stdout,stderr):
    # compare each line of output against a list of regular expressions and build up a dictionary of messages to give the user
    messages={}
    for line  in itertools.chain(stdout.splitlines(True),stderr.splitlines(True)):
        for re in regexs:
            match = re.search(line)
            if (match):
                for key in match.groupdict().keys():
                    if messages.has_key(key):
                        messages[key]=messages[key]+match.group(key)
                    else:
                        messages[key]=match.group(key)
    return messages

class ListSelectionDialog(wx.Dialog):
    class ResizeListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
        def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
            wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
            listmix.ListCtrlAutoWidthMixin.__init__(self)


    def __init__(self, *args, **kw):
        if kw.has_key('parent'):
            self.parent=kw.get('parent')
            logger.debug("ListSelectionDialog: parent is not None.")
            logger.debug("ListSelectionDialog: parent class name is " + self.parent.__class__.__name__) 
        else:
            self.parent = None
            logger.debug("ListSelectionDialog: parent is None.")
        if kw.has_key('progressDialog'):
            self.progressDialog=kw.pop('progressDialog')
        else:
            self.progressDialog=None
        if kw.has_key('headers'):
            self.headers=kw.pop('headers')
        else:
            self.headers=None
        if kw.has_key('items'):
            self.items=kw.pop('items')
        else:
            self.items=None
        if kw.has_key('message'):
            self.message=kw.pop('message')
        else:
            self.message=None
        if kw.has_key('noSelectionMessage'):
            self.noSelectionMessage=kw.pop('noSelectionMessage')
        else:
            self.noSelectionMessage="Please select a valid item from the list.",
        if kw.has_key('okCallback'):
            self.okCallback=kw.pop('okCallback')
        else:
            logger.debug("okCallback set to none")
            self.okCallback=None
        if kw.has_key('cancelCallback'):
            self.cancelCallback=kw.pop('cancelCallback')
        else:
            logger.debug("cancelCallback set to none")
            self.cancelCallback=None
        if kw.has_key('helpEmailAddress'):
            self.helpEmailAddress=kw.pop('helpEmailAddress')
        else:
            logger.debug("helpEmailAddress set to none")
            self.helpEmailAddress="help@massive.org.au"
        super(ListSelectionDialog, self).__init__(*args, **kw)
        self.itemList=[]
       
        self.closedProgressDialog = False
        if self.progressDialog is not None:
            self.progressDialog.Show(False)
            self.closedProgressDialog = True

        self.CenterOnParent()

        if sys.platform.startswith("win"):
            _icon = wx.Icon('MASSIVE.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(_icon)

        if sys.platform.startswith("linux"):
            import MASSIVE_icon
            self.SetIcon(MASSIVE_icon.getMASSIVElogoTransparent128x128Icon())

        listSelectionDialogPanel = wx.Panel(self)
        listSelectionDialogSizer = wx.FlexGridSizer(rows=1, cols=1)
        self.SetSizer(listSelectionDialogSizer)
        listSelectionDialogSizer.Add(listSelectionDialogPanel, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)

        iconPanel = wx.Panel(listSelectionDialogPanel)

        import MASSIVE_icon
        iconAsBitmap = MASSIVE_icon.getMASSIVElogoTransparent128x128Bitmap()
        wx.StaticBitmap(iconPanel, wx.ID_ANY,
            iconAsBitmap,
            (0, 25),
            (iconAsBitmap.GetWidth(), iconAsBitmap.GetHeight()))

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lcSizer = wx.BoxSizer(wx.VERTICAL)
        rcSizer = wx.BoxSizer(wx.VERTICAL)


        contactPanel = wx.Panel(listSelectionDialogPanel)
        contactPanelSizer = wx.FlexGridSizer(rows=2, cols=1, vgap=5, hgap=5)
        contactPanel.SetSizer(contactPanelSizer)
        contactQueriesContactLabel = wx.StaticText(contactPanel, label = "For queries, please contact:")
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if sys.platform.startswith("darwin"):
            font.SetPointSize(11)
        else:
            font.SetPointSize(9)
        contactQueriesContactLabel.SetFont(font)

        contactEmailHyperlink = wx.HyperlinkCtrl(contactPanel, id = wx.ID_ANY, label = self.helpEmailAddress, url = "mailto:" + self.helpEmailAddress)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if sys.platform.startswith("darwin"):
            font.SetPointSize(11)
        else:
            font.SetPointSize(8)
        contactEmailHyperlink.SetFont(font)

        contactPanelSizer.Add(contactQueriesContactLabel, border=10, flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        contactPanelSizer.Add(contactEmailHyperlink, border=20, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)

        contactPanelSizer.Fit(contactPanel)

        listSelectionPanel = wx.Panel(listSelectionDialogPanel)
        listSelectionPanelSizer = wx.BoxSizer(wx.VERTICAL)
        listSelectionPanel.SetSizer(listSelectionPanelSizer)
        if (self.message!=None):
            messageText = wx.StaticText(parent=listSelectionPanel,id=wx.ID_ANY,label=self.message)
            listSelectionPanelSizer.Add(messageText,border=5,flag=wx.ALL^wx.EXPAND)
        if (self.headers!=None):
            self.listSelectionList=ListSelectionDialog.ResizeListCtrl(listSelectionPanel,-1,style=wx.LC_REPORT|wx.EXPAND)
        else:
            self.listSelectionList=ListSelectionDialog.ResizeListCtrl(listSelectionPanel,-1,style=wx.LC_REPORT|wx.EXPAND|wx.LC_NO_HEADER)
        col=0
        if (self.headers!=None):
            for hdr in self.headers:
                self.listSelectionList.InsertColumn(col,hdr,width=-1)
                col=col+1
        elif (self.items!=None):
            if (len(self.items)>0 and isinstance(self.items[0],list)):
                for i in self.items[0]:
                    self.listSelectionList.InsertColumn(col,"",width=-1)
            else:
                self.listSelectionList.InsertColumn(col,"",width=-1)
        if (self.items!=None):
            for item in self.items:
                if (isinstance(item,list)):
                    self.listSelectionList.Append(item)
                    #self.listSelectionList.InsertStringItem(0,item)
                else:
                    self.listSelectionList.Append([item])
        #self.listSelectionList=wx.ListView(listSelectionPanel,style=wx.LC_REPORT)
        listSelectionPanelSizer.Add(self.listSelectionList,proportion=1,border=10,flag=wx.EXPAND|wx.ALL)

        self.buttonsPanel = wx.Panel(listSelectionDialogPanel, wx.ID_ANY)
        self.buttonsPanelSizer = wx.FlexGridSizer(rows=1, cols=2, hgap=5, vgap=5)
        self.buttonsPanel.SetSizer(self.buttonsPanelSizer)

        self.cancelButton = wx.Button(self.buttonsPanel, wx.ID_ANY, 'Cancel')
        self.cancelButton.SetDefault()
        self.cancelButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        # Bottom border of 5 is a workaround for an OS X bug where bottom of button can be clipped.
        self.buttonsPanelSizer.Add(self.cancelButton, flag=wx.BOTTOM, border=5)

        self.okButton = wx.Button(self.buttonsPanel, wx.ID_ANY, ' OK ')
        self.okButton.SetDefault()
        self.okButton.Bind(wx.EVT_BUTTON, self.onClose)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        #self.okButton.Disable()
        # Bottom border of 5 is a workaround for an OS X bug where bottom of button can be clipped.
        self.buttonsPanelSizer.Add(self.okButton, flag=wx.BOTTOM, border=5)

        self.buttonsPanel.GetSizer().Fit(self.buttonsPanel)

        #self.listSelectionList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onFocus)
        self.listSelectionList.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onClose)

        lcSizer.Add(iconPanel,proportion=1,flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALIGN_LEFT)
        lcSizer.Add(contactPanel,proportion=0,flag=wx.ALIGN_LEFT|wx.ALIGN_BOTTOM)
        rcSizer.Add(listSelectionPanel,proportion=1,flag=wx.EXPAND)
        #rcSizer.Add(self.okButton,proportion=0,flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM|wx.BOTTOM,border=5)
        rcSizer.Add(self.buttonsPanel,proportion=0,flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM)
        sizer.Add(lcSizer,proportion=0,flag=wx.EXPAND)
        sizer.Add(rcSizer,proportion=1,flag=wx.EXPAND)
        listSelectionDialogPanel.SetSizer(sizer)
        sizer.Fit(listSelectionDialogPanel)
        self.GetSizer().Fit(self)

        self.listSelectionList.SetFocus()

    def setItems(self,items,headers=None):
        self.itemList=items
        if headers!=None:
            col=0
            for hdr in headers:
                self.listSelectionList.InsertColumn(col,hdr,width=-1)
                col=col+1
        for item in self.itemList:
            self.listSelectionList.Append(item)

    #def onFocus(self,e):
        #if (self.listSelectionList.GetSelectedItemCount()>0):
            #self.okButton.Enable()
        #else:
            #self.okButton.Disable()

    def onClose(self, e):
   
        logger.debug("ListSelectionDialog.onClose: button ID %s okButton ID %s cancelButton ID %s"%(e.GetId(),self.okButton.GetId(),self.cancelButton.GetId()))
        if (e.GetId() == self.cancelButton.GetId()):
            logger.debug("ListSelectionDialog.onClose: User canceled.")
            if self.cancelCallback != None:
                #self.cancelCallback("User canceled from ListSelectionDialog.")
                self.cancelCallback("")
            try:
                self.EndModal(e.GetId())
            except:
                pass
            self.Destroy()
            return

        if self.listSelectionList.GetFirstSelected()==-1:
            dlg = wx.MessageDialog(self.parent, 
                self.noSelectionMessage,
                "", 
                wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            self.listSelectionList.SetFocus()
            return

        itemnum=self.listSelectionList.GetFocusedItem()
        item=self.listSelectionList.GetItem(itemnum,0)
        if self.okCallback != None:
            logger.debug("ListSelectionDialog.onClose: calling okCallback")
            self.okCallback(item)
            logger.debug("ListSelectionDialog.onClose: okCallback returned, calling destroy")
        #self.Destroy()
        try:
            self.EndModal(e.GetId())
        except:
            pass

        if self.closedProgressDialog:
            logger.debug("ListSelectionDialog.onClose: Progress dialog was closed, seeing if it exists to open again")
            if self.progressDialog is not None:
                self.progressDialog.Show(True)


class HelpDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(HelpDialog, self).__init__(*args, **kw)

        self.callback=None
         
        if sys.platform.startswith("win"):
            _icon = wx.Icon('MASSIVE.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(_icon)

        if sys.platform.startswith("linux"):
            import MASSIVE_icon
            self.SetIcon(MASSIVE_icon.getMASSIVElogoTransparent128x128Icon())

        self.CenterOnParent()

        iconPanel = wx.Panel(self)

        import MASSIVE_icon
        iconAsBitmap = MASSIVE_icon.getMASSIVElogoTransparent128x128Bitmap()
        wx.StaticBitmap(iconPanel, wx.ID_ANY,
            iconAsBitmap,
            (0, 25),
            (iconAsBitmap.GetWidth(), iconAsBitmap.GetHeight()))

        sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5, hgap=5)


        contactPanel = wx.Panel(self)
        contactPanelSizer = wx.FlexGridSizer(rows=2, cols=1, vgap=5, hgap=5)
        contactPanel.SetSizer(contactPanelSizer)
        contactQueriesContactLabel = wx.StaticText(contactPanel, label = "For queries, please contact:")
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if sys.platform.startswith("darwin"):
            font.SetPointSize(11)
        else:
            font.SetPointSize(9)
        contactQueriesContactLabel.SetFont(font)

        contactEmailHyperlink = wx.HyperlinkCtrl(contactPanel, id = wx.ID_ANY, label = "help@massive.org.au", url = "mailto:help@massive.org.au")
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if sys.platform.startswith("darwin"):
            font.SetPointSize(11)
        else:
            font.SetPointSize(8)
        contactEmailHyperlink.SetFont(font)

#        contactPanelSizer.Add(wx.StaticText(contactPanel, wx.ID_ANY, ""))
        contactPanelSizer.Add(contactQueriesContactLabel, border=10, flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        contactPanelSizer.Add(contactEmailHyperlink, border=20, flag=wx.LEFT|wx.RIGHT|wx.BOTTOM)

        #contactPanelSizer.Add(wx.StaticText(contactPanel))
        contactPanelSizer.Fit(contactPanel)

        okButton = wx.Button(self, 1, ' OK ')
        okButton.SetDefault()
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)

        sizer.Add(iconPanel, flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALIGN_LEFT)
        sizer.Add(contactPanel)
        sizer.Add(okButton, flag=wx.RIGHT|wx.BOTTOM)
        #sizer.Add(wx.StaticText(self,label="       "))
        self.SetSizer(sizer)
        sizer.Fit(self)

    def setCallback(self,callback):
        self.callback=callback


    def addPanel(self,panel):
        self.GetSizer().Insert(1,panel,flag=wx.EXPAND)
        self.GetSizer().Fit(self)


    def OnClose(self, e):
        if self.callback != None:
            self.callback()
        try:
            self.EndModal(e.GetId())
        except:
            pass
        self.Destroy()


class MyHtmlParser(HTMLParser.HTMLParser):
    def __init__(self, valueString):
        HTMLParser.HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
        self.recordingLatestVersionNumber = 0
        self.latestVersionNumber = "0.0.0"
        self.htmlComments = ""
        self.valueString = valueString

    def handle_starttag(self, tag, attributes):
        if tag != 'span':
            return
        if tag == "span":
            if self.recordingLatestVersionNumber:
                self.recordingLatestVersionNumber += 1
                return
        foundLatestVersionNumberTag = False
        for name, value in attributes:
            if name == 'id' and value == self.valueString:
                foundLatestVersionNumberTag = True
                break
        else:
            return
        if foundLatestVersionNumberTag:
            self.recordingLatestVersionNumber = 1

    def handle_endtag(self, tag):
        if tag == 'span' and self.recordingLatestVersionNumber:
            self.recordingLatestVersionNumber -= 1

    def handle_data(self, data):
        if self.recordingLatestVersionNumber:
            #self.data.append(data)
            self.latestVersionNumber = data.strip()

    def handle_comment(self,data):
        self.htmlComments += data.strip()



def destroy_dialog(dialog):
    wx.CallAfter(dialog.Hide)
    wx.CallAfter(dialog.Show, False)

    while True:
        try:
            if dialog is None: break

            time.sleep(0.01)
            wx.CallAfter(dialog.Destroy)
            wx.Yield()
        except AttributeError:
            break
        except wx._core.PyDeadObjectError:
            break

def seconds_to_hours_minutes(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return int(h), int(m)


def die_from_login_thread(launcherMainFrame,error_message, display_error_dialog=True, submit_log=False):
    if (launcherMainFrame.progressDialog != None):
        wx.CallAfter(launcherMainFrame.progressDialog.Hide)
        wx.CallAfter(launcherMainFrame.progressDialog.Show, False)
        wx.CallAfter(launcherMainFrame.progressDialog.Destroy)
        launcherMainFrame.progressDialog = None

        while True:
            try:
                if launcherMainFrame.progressDialog is None: break

                time.sleep(0.01)
                wx.CallAfter(launcherMainFrame.progressDialog.Destroy)
                wx.Yield()
            except AttributeError:
                break
            except wx._core.PyDeadObjectError:
                break

    launcherMainFrame.progressDialog = None
    wx.CallAfter(launcherMainFrame.loginDialogStatusBar.SetStatusText, "")
    wx.CallAfter(launcherMainFrame.SetCursor, wx.StockCursor(wx.CURSOR_ARROW))

    if display_error_dialog:
        def error_dialog():
            dlg = wx.MessageDialog(launcherMainFrame, error_message,
                            "", wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            launcherMainFrame.loginThread.die_from_login_thread_completed = True

        launcherMainFrame.loginThread.die_from_login_thread_completed = False

        wx.CallAfter(error_dialog)
        while not launcherMainFrame.loginThread.die_from_login_thread_completed:
            time.sleep(0.1)

    wx.CallAfter(launcherMainFrame.logWindow.Show, False)
    wx.CallAfter(launcherMainFrame.logTextCtrl.Clear)
    wx.CallAfter(launcherMainFrame.massiveShowDebugWindowCheckBox.SetValue, False)
    wx.CallAfter(launcherMainFrame.cvlShowDebugWindowCheckBox.SetValue, False)

    logger.dump_log(launcherMainFrame,submit_log=submit_log)

def die_from_main_frame(launcherMainFrame,error_message):
    if (launcherMainFrame.progressDialog != None):
        wx.CallAfter(launcherMainFrame.progressDialog.Destroy)
        launcherMainFrame.progressDialog = None
    wx.CallAfter(launcherMainFrame.loginDialogStatusBar.SetStatusText, "")
    wx.CallAfter(launcherMainFrame.SetCursor, wx.StockCursor(wx.CURSOR_ARROW))

    def error_dialog():
        dlg = wx.MessageDialog(launcherMainFrame, "Error: " + error_message + "\n\n" + "The launcher cannot continue.\n",
                        "", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
#        launcherMainFrame.loginThread.die_from_main_frame_dialog_completed = True

#    launcherMainFrame.loginThread.die_from_main_frame_dialog_completed = False
    wx.CallAfter(error_dialog)
 
    while not launcherMainFrame.loginThread.die_from_main_frame_dialog_completed:
        time.sleep(0.1)
 
    logger.dump_log(launcherMainFrame,submit_log=True)
    os._exit(1)

def run_command(command,ignore_errors=False,log_output=True,callback=None,startupinfo=None,creationflags=0,timeout=120):
    stdout=""
    stderr=""
    if command != None:
        logger.debug('run_command: %s' % command)
        logger.debug('   called from %s:%d' % inspect.stack()[1][1:3])

        ssh_process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True,universal_newlines=True,startupinfo=startupinfo,creationflags=creationflags)

        #(stdout,stderr) = ssh_process.communicate(command)
        t=threading.Timer(timeout,ssh_process.kill)
        t.start()
        (stdout,stderr) = ssh_process.communicate()
        t.cancel()
        ssh_process.wait()
        if log_output:
            logger.debug('command stdout: %s' % repr(stdout))
            logger.debug('command stderr: %s' % repr(stderr))
        if not ignore_errors and len(stderr) > 0:
            error_message = 'Error running command: "%s" at line %d' % (command, inspect.stack()[1][2])
            logger.error('Nonempty stderr and ignore_errors == False; exiting the launcher with error dialog: ' + error_message)
            if (callback != None):
                callback(error_message)

    return stdout, stderr


def unzip(zipFilePath, destDir):

    zfile = zipfile.ZipFile(zipFilePath)

    for name in zfile.namelist():

        (dirName, fileName) = os.path.split(name)

        absoluteDirectoryPath = os.path.join(destDir, dirName)
        if not os.path.exists(absoluteDirectoryPath):
            os.mkdir(absoluteDirectoryPath)

        if fileName != '':
            fd = open(os.path.join(absoluteDirectoryPath, fileName), 'wb')
            fd.write(zfile.read(name))
            fd.close()

    zfile.close()
