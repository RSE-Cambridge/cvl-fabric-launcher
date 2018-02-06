import wx
import sys
import wx.lib.mixins.listctrl as listmix
import wx.calendar
import wx.lib.masked.timectrl
import threading
import Queue
import utilityFunctions

class newReservationDialog(wx.Dialog):
    def __init__(self,parent,queue,*args,**kwargs):
        super(newReservationDialog,self).__init__(parent,*args,**kwargs)
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        p = wx.Panel(parent=self,id=wx.ID_ANY)
        textSizer=wx.BoxSizer(wx.HORIZONTAL)
        p.SetSizer(textSizer)
        t=wx.StaticText(parent=p,id=wx.ID_ANY,label="Reservation Name:")
        textSizer.Add(t)
        self.name=wx.TextCtrl(parent=p,id=wx.ID_ANY)
        textSizer.Add(self.name,proportion=1,flag=wx.EXPAND)
        mainSizer.Add(p)


        self.calctrl=wx.calendar.CalendarCtrl(parent=self,id=wx.ID_ANY,name='startdate')
        self.calctrl.SetMinSize((300,-1))
        mainSizer.Add(self.calctrl,flag=wx.EXPAND)
        now = wx.DateTime.Now()
        self.timectrl=wx.lib.masked.timectrl.TimeCtrl(parent=self,style = wx.TE_PROCESS_TAB,fmt24hr=True,limited=False)
        self.timectrl.SetValue(now)
        #self.timectrl=wx.TimePickerCtrl(parent=self,displaySeconds=False,fmt24hr=True)
        
        mainSizer.Add(self.timectrl,flag=wx.EXPAND)
        self.queue=queue
        p = wx.Panel(parent=self)
        p.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        mainSizer.Add(p)

        b = wx.Button(p,wx.ID_OK,"OK")
        #b.SetMinSize((-1,42))
        b.Bind(wx.EVT_BUTTON,self.onOK)
        p.GetSizer().Add(b)
        b = wx.Button(p,wx.ID_CANCEL,"Done")
        #b.SetMinSize((-1,42))
        b.Bind(wx.EVT_BUTTON,self.onClose)
        p.GetSizer().Add(b)
        self.GetSizer().Fit(self)
        self.Layout()

    def onOK(self,evt):
        date=self.calctrl.GetDate()
        time=self.timectrl.GetValue(as_wxDateTime=True)
        name=self.name.GetValue()
        try:
            import dateutil.tz
            import datetime
            tzlocal=dateutil.tz.tzlocal()
            startdate=datetime.datetime(year=date.GetYear(),month=date.GetMonth()+1,day=date.GetDay(),hour=time.GetHour(),minute=time.GetMinute(),second=time.GetSecond(),tzinfo=tzlocal)
            print "startdate is %s"%startdate
        except:
            import datetime
            startdate=datetime.datetime(year=date.GetYear(),month=date.GetMonth()+1,day=date.GetDay(),hour=time.GetHour(),minute=time.GetMinute(),second=time.GetSecond())
            print "startdate is %s"%startdate
        print "onOK, startdate is %s"%startdate
        self.queue.put((name,startdate))
        self.EndModal(evt.GetEventObject().GetId())
    def onClose(self,evt):
        self.EndModal(evt.GetEventObject().GetId())

class reservationList(wx.ListCtrl,listmix.ListCtrlAutoWidthMixin):
    def __init__(self,*args,**kwargs):
        wx.ListCtrl.__init__(self, *args,**kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0,"Name")
        self.InsertColumn(1,"Description")
        self.setResizeColumn(2)
        self.SetMinSize((1200,-1))

class reservation(object):
    def __init__(self,name,desc):
        super(reservation,self).__init__()
        self.name=name
        self.desc=desc

class reservationsDialog(wx.Dialog):
    def __init__(self,siteConfig,jobParams,rqueue,startupinfo=None,creationflags=None,reservations=None,buttons=['OK','Cancel'],*args,**kwargs):
        super(reservationsDialog,self).__init__(*args,**kwargs)
        mainSizer=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        self.rqueue=rqueue
        self.siteConfig=siteConfig
        self.jobParams=jobParams
        self.startupinfo=startupinfo
        self.creationflags=creationflags
        
        nactive=0
        nfuture=0
        self.summary=wx.StaticText(self,wx.ID_ANY,label="Currently 0 active reserverations 0 future reservations")
        mainSizer.Add(self.summary,flag=wx.ALL,border=5)
        self.resList=reservationList(self,wx.ID_ANY,style=wx.LC_REPORT|wx.EXPAND)
        mainSizer.Add(self.resList,proportion=1,flag=wx.EXPAND)
        self.jobParams=jobParams
        buttonPanel=wx.Panel(parent=self)
        buttonSizer=wx.BoxSizer(wx.HORIZONTAL)
        buttonPanel.SetSizer(buttonSizer)
        self.buttonList=[]
        self.enableButtonList=[]
        self.disableButtonList=[]
        for b in buttons:
            wxb = wx.Button(buttonPanel,wx.ID_ANY,b)
            if b=='OK':
                wxb.Bind(wx.EVT_BUTTON,self.onOK)
                self.enableButtonList.append(wxb)
                self.disableButtonList.append(wxb)
            if b == 'Delete':
                wxb.Bind(wx.EVT_BUTTON,self.onDelete)
                self.enableButtonList.append(wxb)
                self.disableButtonList.append(wxb)
            if b == 'New':
                wxb.Bind(wx.EVT_BUTTON,self.onNew)
            if b == 'Cancel':
                wxb.Bind(wx.EVT_BUTTON,self.onClose)
            buttonPanel.GetSizer().Add(wxb)
        mainSizer.Add(buttonPanel)
        if 'OK' in buttons:
            self.resList.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onOK)
        self.resList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.enableButtons)
        self.resList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.disableButtons)
        self.reservations=[reservation(name='1',desc='one'),reservation(name='2',desc='two')]
        
        self.disableButtons()
        self.Fit()
        self.Layout()
        t=threading.Thread(target=self.updateReservationList)
        t.start()

    
    def enableButtons(self,event):
        for b in self.enableButtonList:
            b.Enable()

    def disableButtons(self,event=None):
        for b in self.disableButtonList:
            b.Disable()

    def updateReservationsGUI(self):
        nactive=0
        nfuture=0
        self.summary.SetLabel("Currently %s active reserverations %s future reservations"%(nactive,nfuture))
        self.resList.DeleteAllItems()
        for r in self.reservations:
            idx = self.resList.GetItemCount()
            print r.name
            print r.desc
            self.resList.InsertStringItem(idx,r.name)
            self.resList.SetStringItem(idx,1,r.desc)

    def onItemSelected(self,evt):
        itemNumber=self.resList.GetFirstSelected()
        self.rqueue.put(self.reservations[itemNumber])
        self.EndModal(wx.ID_OK)

    def onDelete(self,evt):
        i=self.resList.GetFirstSelected()
        reservation=self.reservations[i]
        wx.BeginBusyCursor()
        if i >=0:
            print "item %i selected"%i
            self.resList.Select(i,on=0)
            self.resList.DeleteItem(i)
            self.disableButtons()
            t=threading.Thread(target=self.deleteReservation(reservation))
            t.setDaemon(True)
            t.start()

    def failureDialog(self):
        dlg=wx.Dialog("An unsepficied error occured")
        dlg.ShowModal()

    def updateReservationList(self):
        import re
        cmdRegex = self.siteConfig.listReservations
        (stdout, stderr) = utilityFunctions.run_command(cmdRegex.getCmd(self.jobParams),ignore_errors=True, callback=lambda: wx.CallAfter(self.failureDialog), startupinfo=self.startupinfo, creationflags=self.creationflags) 
        print "running command %s"%cmdRegex.getCmd(self.jobParams)
        print stdout
        print stderr
        self.reservations=[]
        for line in stdout.splitlines():
            for regex in cmdRegex.regex:
                match = re.search(regex,line)
                #match = re.search(regex.format(**self.jobParams).encode('ascii'),line)
                print "didn't find a reservation on that line"
                print
                print
                if (match):
                    r=reservation(match.groupdict()['name'],match.groupdict()['desc'])
                    self.reservations.append(r)
                    print "found a reservation %s"%line
                    print 
                    print
            print "updateReservationList %s"%line
        wx.CallAfter(self.tryEndBusy)
        self.updateReservationsGUI()


    def deleteReservation(self,reservation):
        cmdRegex = self.siteConfig.deleteReservation
        params=self.jobParams.copy()
        params['resname']=reservation.name
        (stdout, stderr) = utilityFunctions.run_command(cmdRegex.getCmd(params),ignore_errors=True, callback=lambda: wx.CallAfter(self.failureDialog), startupinfo=self.startupinfo, creationflags=self.creationflags) 
        self.updateReservationList()

    def tryEndBusy(self):
        try:
            wx.EndBusyCursor()
        except:
            pass

    def showDialog(self,msg,q):
        import sys
        if sys.platform.startswith("darwin"):
            from MacMessageDialog import LauncherMessageDialog
        elif sys.platform.startswith("win"):
            from WindowsMessageDialog import LauncherMessageDialog
        elif sys.platform.startswith("linux"):
            from LinuxMessageDialog import LauncherMessageDialog
        dlg = LauncherMessageDialog(self, msg, "", helpEmailAddress=self.siteConfig.displayStrings.helpEmailAddress )
        dlg.ShowModal()
        dlg.Destroy()
        q.put(None)

    def createReservation(self,resname,startdate,duration):
        print "in create reservation, name is %s"%resname
        if resname=="" or resname==None:
            resname = self.jobParams['username']
        cmdRegex=self.siteConfig.createReservation
        formatdict=self.jobParams.copy()
        res={}
        print formatdict
        try:
            import dateutil
            import dateutil.tz
            sitetz=dateutil.tz.gettz(self.siteConfig.sitetz)
            offset=startdate.utcoffset()
            if offset==None:
                offset=0
            utc = (startdate - startdate.utcoffset()).replace(tzinfo=sitetz)
            startdate=sitetz.fromutc(utc)
            print "converted startdate to correc tz"
            print "startdate is now %s"%startdate
        except Exception as e:
            import traceback
            print "failed to convert tz"
            print traceback.format_exc()
            print e
            pass
        startdatestring=startdate.strftime("%Y-%m-%dT%H:%M:%S")
        print startdate
        print startdatestring
        formatdict.update({"starttime":startdatestring,"duration":duration,"resname":resname})
        (stdout, stderr) = utilityFunctions.run_command(cmdRegex.getCmd(formatdict),ignore_errors=True, callback=lambda: wx.CallAfter(self.failureDialog), startupinfo=self.startupinfo, creationflags=self.creationflags) 
        if stderr!="" and stderr !=None:
            q=Queue.Queue()
            wx.CallAfter(self.showDialog,stderr,q)
            q.get()
        self.updateReservationList()

    def onNew(self,evt):
        duration="%s:00:00"%self.jobParams['hours']
        outq=Queue.Queue()
        dlg=newReservationDialog(self,queue=outq)
        if dlg.ShowModal() == wx.ID_OK:
            (name,startdate)=outq.get()
            t=threading.Thread(target=self.createReservation,args=[name,startdate,duration])
            t.setDaemon(True)
            t.start()
            wx.BeginBusyCursor()

    def onOK(self,evt):
        itemNumber=self.resList.GetFirstSelected()
        self.rqueue.put(self.reservations[itemNumber])
        self.EndModal(wx.ID_OK)

    def onClose(self,evt):
        self.EndModal(evt.GetEventObject().GetId())

    def onCancel(self,evt):
        self.EndModal(evt.GetEventObject().GetId())

