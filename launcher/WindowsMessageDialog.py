import wx

import IconPys.MASSIVElogoTransparent64x64

class LauncherMessageDialog(wx.Dialog):
    def __init__(self, parent, message, title, helpEmailAddress="help@massive.org.au",ButtonLabels=['OK'],**kw):
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP, **kw)

        self.helpEmailAddress=helpEmailAddress
        self.ButtonLabels=ButtonLabels
       
        if parent!=None:
            self.CenterOnParent()
        else:
            self.Centre()
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        topPanel=wx.Panel(self,wx.ID_ANY)
        topPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))


        iconAsBitmap = IconPys.MASSIVElogoTransparent64x64.getMASSIVElogoTransparent64x64Bitmap()
        icon = wx.StaticBitmap(topPanel, wx.ID_ANY, iconAsBitmap, size=(64,64))
        topPanel.GetSizer().Add(icon,flag=wx.ALL,border=5)


        #self.setTitle(title)

#        smallFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
#        smallFont.SetPointSize(11)

        messageWidth = 330
        self.messageLabel = wx.StaticText(topPanel, wx.ID_ANY, message)
        self.messageLabel.SetMinSize((messageWidth,-1))
        #self.messageLabel = wx.StaticText(self.dialogPanel, wx.ID_ANY, message)
        #self.messageLabel.SetForegroundColour((0,0,0))
#        self.messageLabel.SetFont(smallFont)
#        self.messageLabel.Wrap(messageWidth)
        topPanel.GetSizer().Add(self.messageLabel,flag=wx.EXPAND|wx.ALL,proportion=1,border=5)

        #buttonSize = wx.Size(72,22)
        bottomPanel=wx.Panel(self,wx.ID_ANY)
        bottomPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        buttonPanel = wx.Panel(bottomPanel,wx.ID_ANY)
        buttonPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        for label in ButtonLabels:
            #b = wx.Button(buttonPanel, wx.ID_ANY, label,size=buttonSize)
            b = wx.Button(buttonPanel, wx.ID_ANY, label)
            b.SetDefault()
            b.Bind(wx.EVT_BUTTON,self.onClose)
            buttonPanel.GetSizer().Add(b,flag=wx.ALL,border=5)
        buttonPanel.Fit()


        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.contactQueriesContactLabel = wx.StaticText(bottomPanel, label = "For queries, please contact:")
#        self.contactQueriesContactLabel.SetFont(smallFont)
#        self.contactQueriesContactLabel.SetForegroundColour(wx.Colour(0,0,0))
#        self.contactQueriesContactLabel.SetPosition(wx.Point(25,buttonPosition.y))
        bottomPanel.GetSizer().Add(self.contactQueriesContactLabel,flag=wx.ALIGN_CENTER|wx.ALL,border=5)

        self.contactEmailHyperlink = wx.HyperlinkCtrl(bottomPanel, id = wx.ID_ANY, label = self.helpEmailAddress, url = "mailto:" + self.helpEmailAddress)
#        self.contactEmailHyperlink.SetFont(smallFont) # Or maybe even smaller font?
        #hyperlinkPosition = wx.Point(self.contactQueriesContactLabel.GetPosition().x+self.contactQueriesContactLabel.GetSize().width+10,okButtonPosition.y)
#        hyperlinkPosition = wx.Point(self.contactQueriesContactLabel.GetPosition().x+self.contactQueriesContactLabel.GetSize().width,buttonPosition.y)
        bottomPanel.GetSizer().Add(self.contactEmailHyperlink,flag=wx.ALIGN_CENTER|wx.ALL,border=5)
        bottomPanel.GetSizer().Add(buttonPanel,flag=wx.ALIGN_CENTER|wx.LEFT,border=50)
        self.GetSizer().Add(topPanel,flag=wx.EXPAND,proportion=1)
        self.GetSizer().Add(bottomPanel)
        self.Fit()

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
        message = "You have requested 2880 CPU hours, but you only have 455.0 CPU hours remaining in your quota for project \"Desc002\"."
        dialog = LauncherMessageDialog(parent=None, message=message, title="Undefined program name")
        dialog.ShowModal()
        return True
if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
