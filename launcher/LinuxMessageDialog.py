import wx

import IconPys.MASSIVElogoTransparent64x64

class LauncherMessageDialog(wx.Dialog):
    def __init__(self, parent, message, title, helpEmailAddress="help@massive.org.au",ButtonLabels=['OK'],**kw):
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP|wx.RESIZE_BORDER, **kw)

        self.helpEmailAddress=helpEmailAddress
        self.ButtonLabels=ButtonLabels
       
        if parent!=None:
            self.CenterOnParent()
        else:
            self.Centre()
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        leftPanel=wx.Panel(self,wx.ID_ANY)
        leftPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        rightPanel=wx.Panel(self,wx.ID_ANY)
        rightPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))


        iconAsBitmap = IconPys.MASSIVElogoTransparent64x64.getMASSIVElogoTransparent64x64Bitmap()
        icon = wx.StaticBitmap(leftPanel, wx.ID_ANY, iconAsBitmap, size=(64,64))
        leftPanel.GetSizer().Add(icon,flag=wx.ALL,border=5)


        #:wself.setTitle(title)

        messageWidth = 330
        bfont=wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        bfont.SetWeight(wx.FONTWEIGHT_BOLD)
        self.messageLabel = wx.StaticText(rightPanel, wx.ID_ANY, message)
        self.messageLabel.SetFont(bfont)
        rightPanel.GetSizer().Add(self.messageLabel,flag=wx.EXPAND|wx.ALL,proportion=1,border=5)

        bottomPanel=wx.Panel(rightPanel,wx.ID_ANY)
        bottomPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        buttonPanel = wx.Panel(bottomPanel,wx.ID_ANY)
        buttonPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        for label in ButtonLabels:
            b = wx.Button(buttonPanel, wx.ID_ANY, label)
            b.SetDefault()
            b.Bind(wx.EVT_BUTTON,self.onClose)
            buttonPanel.GetSizer().Add(b,flag=wx.ALL,border=5)
        buttonPanel.Fit()


        self.Bind(wx.EVT_CLOSE, self.onClose)

        p=wx.Panel(bottomPanel,wx.ID_ANY)
        p.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        bottomPanel.GetSizer().Add(p,flag=wx.ALIGN_LEFT)
        self.contactQueriesContactLabel = wx.StaticText(p, label = "For queries, please contact:")
        p.GetSizer().Add(self.contactQueriesContactLabel,flag=wx.ALIGN_CENTER|wx.ALL)

        self.contactEmailHyperlink = wx.HyperlinkCtrl(p, id = wx.ID_ANY, label = self.helpEmailAddress, url = "mailto:" + self.helpEmailAddress)
        p.GetSizer().Add(self.contactEmailHyperlink,flag=wx.ALIGN_CENTER|wx.ALL,border=5)
        bottomPanel.GetSizer().Add(buttonPanel,flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        bottomPanel.Fit()
        w=max(bottomPanel.GetSize()[0],330)
        self.messageLabel.Wrap(w)

        rightPanel.GetSizer().Add(bottomPanel,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        self.GetSizer().Add(leftPanel)
        self.GetSizer().Add(rightPanel,flag=wx.EXPAND,proportion=1)
        self.GetSizer().Fit(self)

    def onClose(self, event):
        obj=event.GetEventObject()
        if (isinstance(obj,wx.Button)):
            label=obj.GetLabel()
            ln=0
            for i in self.ButtonLabels:
                if (label==i):
                    self.EndModal(ln)
                else:
                    ln=ln+1
        else:
            self.EndModal(-1)

class MyApp(wx.App):
    def OnInit(self):
        message = "You have requested 2880 CPU hours, but you only have 455.0 CPU hours remaining in your quota for project \"Desc002\". Much long text\n asdf asdf asdf asdf asdf asdf asdf asdfasdfajkl; ajkl;sadf ajskl;asd asjkl;a ajkl;a aj kl;as ajkl;dfsa jakl;sdf jiopwerqjl k;cvxaj kl;asihjwelrqj kl;samcvkl;uzlxk asjdfkl; "
        dialog = LauncherMessageDialog(parent=None, message=message, title="Undefined program name",ButtonLabels=["OK"])
        dialog.ShowModal()
        message = "You have requested 2880 CPU hours, but you only have 455.0 CPU hours remaining in your quota for project \"Desc002\". Much long text\n asdf asdf asdf asdf asdf asdf asdf asdfasdfajkl; ajkl;sadf ajskl;asd asjkl;a ajkl;a aj kl;as ajkl;dfsa jakl;sdf jiopwerqjl k;cvxaj kl;asihjwelrqj kl;samcvkl;uzlxk asjdfkl; "
        dialog = LauncherMessageDialog(parent=None, message=message, title="Undefined program name",ButtonLabels=["OK","Cancel","Do the other thing","Use more buttons","Bring about world peace"])
        b=dialog.ShowModal()
        return True
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
