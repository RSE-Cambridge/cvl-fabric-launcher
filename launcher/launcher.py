# MASSIVE/CVL Launcher - easy secure login for the MASSIVE Desktop and the CVL
#
# Copyright (c) 2012-2013, Monash e-Research Centre (Monash University, Australia)
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# In addition, redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# -  Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#
# -  Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
#
# -  Neither the name of the Monash University nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. SEE THE
# GNU GENERAL PUBLIC LICENSE FOR MORE DETAILS.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Enquiries: help@massive.org.au

# launcher.py
"""
A wxPython GUI to provide easy login to the MASSIVE Desktop.
It can be run using "python launcher.py", assuming that you
have an appropriate (32-bit or 64-bit) version of Python 
installed (*), wxPython, and the dependent Python modules 
listed in the DEPENDENCIES file.

(*) wxPython 2.8.x on Mac OS X doesn't support 64-bit mode.

The py2app module is required to build the "MASSIVE Launcher.app"
application bundle on Mac OS X, which can be built as follows:

   python create_mac_bundle.py py2app

To build a DMG containing the app bundle and a symbolic link to
Applications, you can run:

   python package_mac_version.py <version_number>

See: https://confluence-vre.its.monash.edu.au/display/CVL/MASSIVE+Launcher+Mac+OS+X+build+instructions

The PyInstaller module, bundled with the Launcher code is used
to build the Windows and Linux executables. The Windows setup wizard
(created with InnoSetup) can be built using:

   package_windows_version.bat C:\path\to\code\signing\certificate.pfx <certificate_password>

assuming that you have InnoSetup installed and that you have signtool.exe installed for
code signing.

See: https://confluence-vre.its.monash.edu.au/display/CVL/MASSIVE+Launcher+Windows+build+instructions

If you want to build a stand-alone Launcher binary for Mac or Windows
without using a code-signing certificate, you can do so by commenting
out the code-signing functionality in package_mac_version.py and in
package_windows_version.bat.  In other words, sorry, this is not 
possible at present without modifying the packaging scripts.

A self-contained Linux binary distribution can be built using
PyInstaller, as described on the following wiki page.

See: https://confluence-vre.its.monash.edu.au/display/CVL/MASSIVE+Launcher+Linux+build+instructions

"""


# Make sure that the Launcher doesn't attempt to write to
# "MASSIVE Launcher.exe.log", because it might not have
# permission to do so.
import sys
if sys.platform.startswith("win"):
    sys.stderr = sys.stdout

if sys.platform.startswith("win"):
    import _winreg
import subprocess
import wx
import time
import traceback
import threading
import os
import HTMLParser
import urllib2
import launcher_version_number
import xmlrpclib
import appdirs
import ConfigParser
import datetime
import shlex
import inspect
import requests
from StringIO import StringIO
import logging
import LoginTasks
from utilityFunctions import *
import cvlsshutils.sshKeyDist
import cvlsshutils
import launcher_progress_dialog
from menus.IdentityMenu import IdentityMenu
import tempfile
from cvlsshutils.KeyModel import KeyModel
import siteConfig
import Queue

if sys.platform.startswith("darwin"):
    from MacMessageDialog import LauncherMessageDialog
elif sys.platform.startswith("win"):
    from WindowsMessageDialog import LauncherMessageDialog
elif sys.platform.startswith("linux"):
    from LinuxMessageDialog import LauncherMessageDialog
from logger.Logger import logger
import collections
import optionsDialog
import LauncherOptionsDialog

from utilityFunctions import LAUNCHER_URL
import dialogtext
dialogs=dialogtext.default()

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        super(FileDrop,self).__init__()
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        if len(filenames)!=1:
            pass
        else:
            self.window.loadSession(None,filenames[0])


class LauncherMainFrame(wx.Frame):
    PERM_SSH_KEY=0
    TEMP_SSH_KEY=1


    def shouldSave(self,item):
        # I should be able to use a python iterator here
        shouldSave=False
        for ctrl in self.savedControls:
            if isinstance(item,ctrl) and 'jobParams' in item.GetName():
                shouldSave=True
        return shouldSave

# Use this method to read a specifig section of the preferences file
    def loadConfig(self):
        assert self.prefs == None
        try:
            self.prefs=ConfigParser.SafeConfigParser(allow_no_value=True)
        except:
            # For compatibility with older ConfigParser on Centos6
            self.prefs=ConfigParser.SafeConfigParser()
        if (os.path.exists(launcherPreferencesFilePath)):
            with open(launcherPreferencesFilePath,'r') as o:
                self.prefs.readfp(o)

    def getPrefsSection(self,section):
        assert self.prefs != None
        options = {}
        if self.prefs.has_section(section):
            optionsList =  self.prefs.items(section)
            for option in optionsList:
                key = option[0]
                value = option[1]
                if value=='True':
                    value = True
                if value=='False':
                    value = False
                options[key] = value
        return options

    def setPrefsSection(self,section,options):
        assert self.prefs != None
        if not self.prefs.has_section(section):
            self.prefs.add_section(section)
        for key in options.keys():
            self.prefs.set(section,key,"%s"%options[key])
        pass
    
    def loadSiteDefaults(self,configName):
        try:
            site=self.sites[configName]
            for key in site.defaults:
                logger.debug("setting default value for %s"%key)
                try:
                    self.FindWindowByName(key).SetValue(int(site.defaults[key]))
                except ValueError as e:
                    try:
                        self.FindWindowByName(key).SetValue(site.defaults[key])
                    except Exception as e:
                        raise e
        except Exception as e:
            logger.debug("unable to set the default values for the site: %s"%e)

# Use this method to a) Figure out if we have a default site b) load the parameters for that site.
    def loadPrefs(self,window=None,site=None):
        assert self.prefs != None
        if window==None:
            window=self
        if (site==None):
            siteConfigComboBox=self.FindWindowByName('jobParams_configName')
            try:
                site=siteConfigComboBox.GetValue()
            except:
                pass
        if (site != None):
            if self.prefs.has_section(site):
                for item in window.GetChildren():
                    if self.shouldSave(item):
                        name=item.GetName()
                        if self.prefs.has_option(site,name):
                            val=self.prefs.get(site,name)
                            try: # Most wx Controls expect a string in SetValue, but at least SpinCtrl expects an int.
                                item.SetValue(val)
                            except TypeError:
                                item.SetValue(int(val))
                            except AttributeError:
                                item.SetSelection(int(val))
                    else:
                        self.loadPrefs(window=item,site=site)

    def savePrefsEventHandler(self,event):
        threading.Thread(target=self.savePrefs).start()
        event.Skip()
        
    def savePrefs(self,window=None,section=None):
        assert self.prefs!=None
        specialSections=['Global Preferences','configured_sites']
        write=False
        # If we called savePrefs without a window specified, its the root of recussion
        if (window==None and not section in specialSections):
            write=True
            window=self
        if (section in specialSections):
            write=True
            window=None
        if (section==None):
            try:
                configName=self.FindWindowByName('jobParams_configName').GetValue()
                if (configName!=None):
                    if (not self.prefs.has_section("Launcher Config")):
                        self.prefs.add_section("Launcher Config")
                    self.prefs.set("Launcher Config","siteConfigDefault",'%s'%configName)
                    self.savePrefs(section=configName)
            except:
                pass
        elif (section!=None):
            if (not self.prefs.has_section(section)):
                self.prefs.add_section(section)
            try:
                for item in window.GetChildren():
                    if self.shouldSave(item):
                        try:
                            self.prefs.set(section,item.GetName(),'%s'%item.GetValue())
                        except AttributeError:
                            self.prefs.set(section,item.GetName(),'%s'%item.GetSelection())
                    else:
                        self.savePrefs(section=section,window=item)
            except:
                pass
        if (write):
            with open(launcherPreferencesFilePath,'w') as o:
                self.prefs.write(o)



    def __init__(self, parent, id, title):

        super(LauncherMainFrame,self).__init__(parent, id, title, style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER )
        dt=FileDrop(self)
        self.SetDropTarget(dt)
        self.programName=title
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.SetAutoLayout(0)

        self.savedControls=[]
        self.savedControls.append(wx.TextCtrl)
        self.savedControls.append(wx.ComboBox)
        self.savedControls.append(wx.SpinCtrl)
        self.savedControls.append(wx.RadioBox)

        self.prefs=None
        self.loginProcess=[]
        import collections
        self.networkLog = collections.deque()
        self.networkLogThread = None
        self.networkLogStopEvent = threading.Event()
        self.hiddenWindow = None
        self.progressDialog = None

        if sys.platform.startswith("win"):
            _icon = wx.Icon('MASSIVE.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(_icon)

        if sys.platform.startswith("linux"):
            import MASSIVE_icon
            self.SetIcon(MASSIVE_icon.getMASSIVElogoTransparent128x128Icon())

        self.loadConfig()

        self.menu_bar  = wx.MenuBar()

        self.file_menu = wx.Menu()
        self.menu_bar.Append(self.file_menu, "&File")
        transferFiles=wx.MenuItem(self.file_menu,wx.ID_ANY,"&Transfer Files")
        self.file_menu.AppendItem(transferFiles)
        self.Bind(wx.EVT_MENU, self.transferFilesEvent, id=transferFiles.GetId())
        shareDesktop=wx.MenuItem(self.file_menu,wx.ID_ANY,"&Share my desktop")
        self.file_menu.AppendItem(shareDesktop)
        self.Bind(wx.EVT_MENU, self.saveSessionEvent, id=shareDesktop.GetId())
        loadSession=wx.MenuItem(self.file_menu,wx.ID_ANY,"&Connect to a collaborator")
        self.file_menu.AppendItem(loadSession)
        self.Bind(wx.EVT_MENU, self.loadSessionEvent, id=loadSession.GetId())
        loadDefaultSessions=wx.MenuItem(self.file_menu,wx.ID_ANY,"&Load defaults")
        self.file_menu.AppendItem(loadDefaultSessions)
        self.loadDefaultSessionsId=loadDefaultSessions.GetId()
        self.Bind(wx.EVT_MENU, self.loadDefaultSessionsEvent, id=loadDefaultSessions.GetId())
        manageSites=wx.MenuItem(self.file_menu,wx.ID_ANY,"&Manage sites")
        self.file_menu.AppendItem(manageSites)
        self.Bind(wx.EVT_MENU,self.manageSitesEventHandler,id=manageSites.GetId())
        if sys.platform.startswith("win") or sys.platform.startswith("linux"):
            self.file_menu.Append(wx.ID_EXIT, "E&xit", "Close window and exit program.")
            self.Bind(wx.EVT_MENU, self.onExit, id=wx.ID_EXIT)
           
            

        #if sys.platform.startswith("darwin"):
            ## Only do this for Mac OS X, because other platforms have
            ## a right-click pop-up menu for wx.TextCtrl with Copy,
            ## Select All etc. Plus, the menu doesn't look that good on
            ## the MASSIVE Launcher main dialog, and doesn't work for
            ## non Mac platforms, because FindFocus() will always
            ## find the window/dialog which contains the menu.
            #self.edit_menu = wx.Menu()
            #self.edit_menu.Append(wx.ID_CUT, "Cut", "Cut the selected text")
            #self.Bind(wx.EVT_MENU, self.onCut, id=wx.ID_CUT)
            #self.edit_menu.Append(wx.ID_COPY, "Copy", "Copy the selected text")
            #self.Bind(wx.EVT_MENU, self.onCopy, id=wx.ID_COPY)
            #self.edit_menu.Append(wx.ID_PASTE, "Paste", "Paste text from the clipboard")
            #self.Bind(wx.EVT_MENU, self.onPaste, id=wx.ID_PASTE)
            #self.edit_menu.Append(wx.ID_SELECTALL, "Select All")
            #self.Bind(wx.EVT_MENU, self.onSelectAll, id=wx.ID_SELECTALL)
            #self.menu_bar.Append(self.edit_menu, "&Edit")
        self.edit_menu = wx.Menu()
        self.edit_menu.Append(wx.ID_CUT, "Cu&t", "Cut the selected text")
        self.Bind(wx.EVT_MENU, self.onCut, id=wx.ID_CUT)
        self.edit_menu.Append(wx.ID_COPY, "&Copy", "Copy the selected text")
        self.Bind(wx.EVT_MENU, self.onCopy, id=wx.ID_COPY)
        self.edit_menu.Append(wx.ID_PASTE, "&Paste", "Paste text from the clipboard")
        self.Bind(wx.EVT_MENU, self.onPaste, id=wx.ID_PASTE)
        self.edit_menu.Append(wx.ID_SELECTALL, "Select &All")
        self.Bind(wx.EVT_MENU, self.onSelectAll, id=wx.ID_SELECTALL)
        self.edit_menu.AppendSeparator()
        id_preferences=wx.NewId()
        if sys.platform.startswith("win") or sys.platform.startswith("linux"):
            self.edit_menu.Append(id_preferences, "P&references\tCtrl-P")
        else:
            self.edit_menu.Append(id_preferences, "&Preferences")
        self.Bind(wx.EVT_MENU, self.onOptions, id=id_preferences)
        self.menu_bar.Append(self.edit_menu, "&Edit")

        self.identity_menu = IdentityMenu()
        options=self.getPrefsSection('Global Preferences')
        if options.has_key('auth_mode'):
            auth_mode = int(options['auth_mode'])
        else:
            auth_mode = 0
        self.identity_menu.initialize(self,auth_mode=auth_mode)
        self.menu_bar.Append(self.identity_menu, "&Identity")

        self.help_menu = wx.Menu()
        helpContentsMenuItemID = wx.NewId()
        self.help_menu.Append(helpContentsMenuItemID, "&%s Help"%self.programName)
        self.Bind(wx.EVT_MENU, self.onHelpContents, id=helpContentsMenuItemID)
        self.help_menu.AppendSeparator()
        emailHelpAtMassiveMenuItemID = wx.NewId()
        self.help_menu.Append(emailHelpAtMassiveMenuItemID, "Email &help@massive.org.au")
        self.Bind(wx.EVT_MENU, self.onEmailHelpAtMassive, id=emailHelpAtMassiveMenuItemID)
        submitDebugLogMenuItemID = wx.NewId()
        self.help_menu.Append(submitDebugLogMenuItemID, "&Submit debug log")
        self.Bind(wx.EVT_MENU, self.onSubmitDebugLog, id=submitDebugLogMenuItemID)
        # On Mac, the About menu item will automatically be moved from 
        # the Help menu to the "MASSIVE Launcher" menu, so we don't
        # need a separator.
        if not sys.platform.startswith("darwin"):
            self.help_menu.AppendSeparator()
        self.help_menu.Append(wx.ID_ABOUT,   "&About %s"%self.programName)
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
        self.menu_bar.Append(self.help_menu, "&Help")

        self.SetTitle(self.programName)


        self.loginDialogPanel = wx.Panel(self, wx.ID_ANY)
        self.loginDialogPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.GetSizer().Add(self.loginDialogPanel)

        self.loginFieldsPanel = wx.Panel(self.loginDialogPanel, wx.ID_ANY)
        self.loginFieldsPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        self.loginDialogPanel.GetSizer().Add(self.loginFieldsPanel, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

        widgetWidth1 = 180
        widgetWidth2 = 180
        if not sys.platform.startswith("win"):
            widgetWidth2 = widgetWidth2 + 25
        # widgetWidth3 = 75
        widgetWidth3 = 100 # on Fedora 23 (XFCE4) the theme of the SpinCtrl will set "+" and "-" button side-by-side - this requires more space

        
        self.noneVisible={}
        self.noneVisible['usernamePanel']=False
        self.noneVisible['projectPanel']=False
        self.noneVisible['execHostPanel']=False
        self.noneVisible['resourcePanel']=False
        self.noneVisible['resolutionPanel']=False
        self.noneVisible['cipherPanel']=False
        self.noneVisible['debugCheckBoxPanel']=False
        self.noneVisible['advancedCheckBoxPanel']=False
        self.noneVisible['optionsDialog']=False


        self.sites={}
        self.siteConfigPanel = wx.Panel(self.loginFieldsPanel, wx.ID_ANY)
        self.siteConfigPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.configLabel = wx.StaticText(self.siteConfigPanel, wx.ID_ANY, 'Site',name='label_config')
        self.siteConfigPanel.GetSizer().Add(self.configLabel, proportion=0, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER, border=5)
        self.siteConfigComboBox = wx.ComboBox(self.siteConfigPanel, wx.ID_ANY, choices=self.sites.keys(), style=wx.CB_READONLY,name='jobParams_configName')
        self.siteConfigComboBox.Bind(wx.EVT_COMBOBOX, self.onSiteConfigChanged)
        self.siteConfigPanel.GetSizer().Add(self.siteConfigComboBox, proportion=1,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.siteConfigPanel,proportion=0,flag=wx.EXPAND)

        self.loginHostPanel=wx.Panel(self.loginFieldsPanel,name='loginHostPanel')
        self.loginHostPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.loginHostLabel = wx.StaticText(self.loginHostPanel, wx.ID_ANY, 'Server name or IP',name='label_loginHost')
        self.loginHostPanel.GetSizer().Add(self.loginHostLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginHostTextField = wx.TextCtrl(self.loginHostPanel, wx.ID_ANY, size=(widgetWidth2, -1),name='jobParams_loginHost')
        self.loginHostPanel.GetSizer().Add(self.loginHostTextField, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.loginHostPanel,proportion=0,flag=wx.EXPAND)


        self.usernamePanel=wx.Panel(self.loginFieldsPanel,name='usernamePanel')
        self.usernamePanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.usernameLabel = wx.StaticText(self.usernamePanel, wx.ID_ANY, 'Username',name='label_username')
        self.usernamePanel.GetSizer().Add(self.usernameLabel, proportion=1,flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border=5)
        self.usernameTextField = wx.TextCtrl(self.usernamePanel, wx.ID_ANY, size=(widgetWidth2, -1),name='jobParams_username')
        self.usernamePanel.GetSizer().Add(self.usernameTextField, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.usernamePanel,proportion=0,flag=wx.EXPAND)

        self.projectPanel = wx.Panel(self.loginFieldsPanel,wx.ID_ANY,name="projectPanel")
        self.projectPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.projectLabel = wx.StaticText(self.projectPanel, wx.ID_ANY, 'Project',name='label_project')
        self.projectPanel.GetSizer().Add(self.projectLabel, proportion=1, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)

        self.projectField = wx.TextCtrl(self.projectPanel, wx.ID_ANY, size=(widgetWidth2, -1), name='jobParams_project')
        #self.projectComboBox.Bind(wx.EVT_TEXT, self.onProjectTextChanged)
        self.projectPanel.GetSizer().Add(self.projectField, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.projectPanel, proportion=0,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT)

        self.resourcePanel = wx.Panel(self.loginFieldsPanel, wx.ID_ANY,name="resourcePanel")
        #self.resourcePanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.resourcePanel.SetSizer(wx.FlexGridSizer(rows=4,cols=4))

        self.hoursLabel = wx.StaticText(self.resourcePanel, wx.ID_ANY, 'Hours requested',name='label_hours')
        self.resourcePanel.GetSizer().Add(self.hoursLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        # Maximum of 336 hours is 2 weeks:
        #self.massiveHoursField = wx.SpinCtrl(self.massiveLoginFieldsPanel, wx.ID_ANY, value=self.massiveHoursRequested, min=1,max=336)
        self.hoursField = wx.SpinCtrl(self.resourcePanel, wx.ID_ANY, size=(widgetWidth3,-1), min=1,max=336,name='jobParams_hours')
        self.resourcePanel.GetSizer().Add(self.hoursField, proportion=0,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)

        self.memLabel = wx.StaticText(self.resourcePanel, wx.ID_ANY, 'Memory (GB)',name='label_mem')
        self.resourcePanel.GetSizer().Add(self.memLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        # Maximum of 336 mem is 2 weeks:
        #self.massiveHoursField = wx.SpinCtrl(self.massiveLoginFieldsPanel, wx.ID_ANY, value=self.massiveHoursRequested, min=1,max=336)
        self.memField = wx.SpinCtrl(self.resourcePanel, wx.ID_ANY, size=(widgetWidth3,-1), min=1,max=1024,name='jobParams_mem')
        self.resourcePanel.GetSizer().Add(self.memField, proportion=0,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        
        self.nodesLabel = wx.StaticText(self.resourcePanel, wx.ID_ANY, 'Nodes',name='label_nodes')
        self.resourcePanel.GetSizer().Add(self.nodesLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        self.nodesField = wx.SpinCtrl(self.resourcePanel, wx.ID_ANY, value="1", size=(widgetWidth3,-1), min=1,max=10,name='jobParams_nodes')
        self.resourcePanel.GetSizer().Add(self.nodesField, proportion=0,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        self.ppnLabel = wx.StaticText(self.resourcePanel, wx.ID_ANY, 'PPN',name='label_ppn')
        self.resourcePanel.GetSizer().Add(self.ppnLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL,border=5)
        self.ppnField = wx.SpinCtrl(self.resourcePanel, wx.ID_ANY, value="12", size=(widgetWidth3,-1), min=1,max=12,name='jobParams_ppn')
        self.resourcePanel.GetSizer().Add(self.ppnField, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.resourcePanel, proportion=0,border=0,flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)


        self.resolutionPanel = wx.Panel(self.loginFieldsPanel,name="resolutionPanel")
        self.resolutionPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.resolutionLabel = wx.StaticText(self.resolutionPanel, wx.ID_ANY, 'Resolution',name='label_resolution')
        self.resolutionPanel.GetSizer().Add(self.resolutionLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)


        defaultResolution = "Default resolution"
        vncDisplayResolutions = [
            defaultResolution, "1024x768", "1152x864", "1280x800", "1280x1024", "1360x768", "1366x768", "1440x900", "1600x900", "1680x1050", "1920x1080", "1920x1200", "7680x3200",
            ]
        self.resolutionField = wx.ComboBox(self.resolutionPanel, wx.ID_ANY, value=defaultResolution, choices=vncDisplayResolutions, size=(widgetWidth2, -1), style=wx.CB_DROPDOWN,name='jobParams_resolution')
        self.resolutionPanel.GetSizer().Add(self.resolutionField, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.resolutionPanel,proportion=0,flag=wx.EXPAND)

        
        self.cipherPanel = wx.Panel(self.loginFieldsPanel,name="cipherPanel")
        self.cipherPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        self.sshTunnelCipherLabel = wx.StaticText(self.cipherPanel, wx.ID_ANY, 'SSH tunnel cipher',name='label_cipher')
        self.cipherPanel.GetSizer().Add(self.sshTunnelCipherLabel, proportion=1,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=5)

        if sys.platform.startswith("win"):
            defaultCipher = "arcfour"
            sshTunnelCiphers = ["3des-cbc", "aes128-ctr", "blowfish-cbc", "arcfour"]
        else:
            defaultCipher = "arcfour128"
            sshTunnelCiphers = ["3des-cbc", "aes128-ctr", "blowfish-cbc", "arcfour128"]
        self.sshTunnelCipherComboBox = wx.ComboBox(self.cipherPanel, wx.ID_ANY, value=defaultCipher, choices=sshTunnelCiphers, size=(widgetWidth2, -1), style=wx.CB_DROPDOWN,name='jobParams_cipher')
        self.cipherPanel.GetSizer().Add(self.sshTunnelCipherComboBox, proportion=0,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, border=5)
        self.loginFieldsPanel.GetSizer().Add(self.cipherPanel,proportion=0,flag=wx.EXPAND)
        

        self.checkBoxPanel = wx.Panel(self.loginFieldsPanel,name="checkBoxPanel")
        self.checkBoxPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        
        p = wx.Panel(self.checkBoxPanel,name="debugCheckBoxPanel")
        p.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        l = wx.StaticText(p, wx.ID_ANY, 'Show debug window',name='label_debug')
        c = wx.CheckBox(p, wx.ID_ANY, "",name='debugCheckBox')
        c.Bind(wx.EVT_CHECKBOX, self.onDebugWindowCheckBoxStateChanged)
        p.GetSizer().Add(l,border=5,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)
        p.GetSizer().Add(c,border=5,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.checkBoxPanel.GetSizer().Add(p,flag=wx.ALIGN_LEFT)
    
        t=wx.StaticText(self.checkBoxPanel,label="")
        self.checkBoxPanel.GetSizer().Add(t,proportion=1,flag=wx.EXPAND)
  
        p = wx.Panel(self.checkBoxPanel,name="advancedCheckBoxPanel")
        p.SetSizer(wx.BoxSizer(wx.HORIZONTAL))
        l = wx.StaticText(p, wx.ID_ANY, 'Show Advanced Options',name='label_advanced')
        c = wx.CheckBox(p, wx.ID_ANY, "",name='advancedCheckBox')
        c.Bind(wx.EVT_CHECKBOX, self.onAdvancedVisibilityStateChanged)
        p.GetSizer().Add(l,border=5,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)
        p.GetSizer().Add(c,border=5,flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.checkBoxPanel.GetSizer().Add(p,flag=wx.ALIGN_RIGHT)

        self.loginFieldsPanel.GetSizer().Add(self.checkBoxPanel,flag=wx.ALIGN_BOTTOM|wx.EXPAND,proportion=1)

        #self.tabbedView.AddPage(self.loginFieldsPanel, "Login")

        #self.loginDialogPanelSizer.Add(self.tabbedView, flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

        # Buttons Panel

        self.buttonsPanel = wx.Panel(self.loginDialogPanel, wx.ID_ANY)
        #self.buttonsPanel.SetSizer(wx.FlexGridSizer(rows=1, cols=4, vgap=5, hgap=10))
        self.buttonsPanel.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

        self.manageResButton = wx.Button(self.buttonsPanel,wx.ID_ANY,'Manage Reservations',name='manageResButton')
        self.buttonsPanel.GetSizer().Add(self.manageResButton, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_LEFT,border=10)
        self.manageResButton.Bind(wx.EVT_BUTTON, self.onManageReservations)

        self.exitButton = wx.Button(self.buttonsPanel, wx.ID_ANY, 'Exit')
        self.buttonsPanel.GetSizer().Add(self.exitButton, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border=10)
        self.Bind(wx.EVT_BUTTON, self.onExit,  id=self.exitButton.GetId())

        self.loginButton = wx.Button(self.buttonsPanel, wx.ID_ANY, 'Login')
        self.buttonsPanel.GetSizer().Add(self.loginButton, flag=wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, border=10)
        self.loginButton.Bind(wx.EVT_BUTTON, self.savePrefsEventHandler)
        self.loginButton.Bind(wx.EVT_BUTTON, self.onLogin)
        self.loginButton.SetDefault()
        #self.buttonsPanel.SetMinSize((-1,100))


        #self.preferencesButton.Show(False)

        self.loginDialogPanel.GetSizer().Add(self.buttonsPanel, flag=wx.ALIGN_RIGHT|wx.BOTTOM|wx.LEFT|wx.RIGHT, border=15)

        self.loginDialogStatusBar = LauncherStatusBar(self)


        #self.Fit()
        #self.Layout()
        #self.menu_bar.Show(False)

        #self.Centre()

        self.hiddenWindow=wx.Frame(self,name='hidden_window')
        self.GetSizer().Add(self.hiddenWindow)
        self.hiddenWindow.SetSizer(wx.BoxSizer(wx.VERTICAL))
        t=wx.TextCtrl(self.hiddenWindow,wx.ID_ANY,name='jobParams_aaf_idp')
        self.hiddenWindow.GetSizer().Add(t)
        t=wx.TextCtrl(self.hiddenWindow,wx.ID_ANY,name='jobParams_aaf_username')
        self.hiddenWindow.GetSizer().Add(t)

        # any controls created on this frame will be inaccessible to the user, but if we set them it will cause them to be saved to the config file

        self.logWindow = wx.Frame(self, title="%s Debug Log"%self.programName, name="%s Debug Log"%self.programName,pos=(200,150),size=(700,450))
        self.logWindow.Bind(wx.EVT_CLOSE, self.onCloseDebugWindow)
        self.logWindowPanel = wx.Panel(self.logWindow)
        self.logTextCtrl = wx.TextCtrl(self.logWindowPanel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        logWindowSizer = wx.FlexGridSizer(rows=2, cols=1, vgap=0, hgap=0)
        logWindowSizer.AddGrowableRow(0)
        logWindowSizer.AddGrowableCol(0)
        logWindowSizer.Add(self.logTextCtrl, flag=wx.EXPAND)
        self.submitDebugLogButton = wx.Button(self.logWindowPanel, wx.ID_ANY, 'Submit debug log')
        self.Bind(wx.EVT_BUTTON, self.onSubmitDebugLog, id=self.submitDebugLogButton.GetId())
        logWindowSizer.Add(self.submitDebugLogButton, flag=wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM|wx.RIGHT, border=10)
        self.logWindowPanel.SetSizer(logWindowSizer)
        if sys.platform.startswith("darwin"):
            font = wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        else:
            font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        self.logTextCtrl.SetFont(font)

        if sys.platform.startswith("win"):
            _icon = wx.Icon('MASSIVE.ico', wx.BITMAP_TYPE_ICO)
            self.logWindow.SetIcon(_icon)

        if sys.platform.startswith("linux"):
            import MASSIVE_icon
            self.logWindow.SetIcon(MASSIVE_icon.getMASSIVElogoTransparent128x128Icon())

        logger.sendLogMessagesToDebugWindowTextControl(self.logTextCtrl)

        import getpass
        logger.debug('getpass.getuser(): ' + getpass.getuser())

        logger.debug('sys.platform: ' + sys.platform)

        import platform

        logger.debug('platform.architecture: '  + str(platform.architecture()))
        logger.debug('platform.machine: '       + str(platform.machine()))
        logger.debug('platform.node: '          + str(platform.node()))
        logger.debug('platform.platform: '      + str(platform.platform()))
        logger.debug('platform.processor: '     + str(platform.processor()))
        logger.debug('platform.release: '       + str(platform.release()))
        logger.debug('platform.system: '        + str(platform.system()))
        logger.debug('platform.version: '       + str(platform.version()))
        logger.debug('platform.uname: '         + str(platform.uname()))

        if sys.platform.startswith("win"):
            logger.debug('platform.win32_ver: ' + str(platform.win32_ver()))

        if sys.platform.startswith("darwin"):
            logger.debug('platform.mac_ver: ' + str(platform.mac_ver()))

        if sys.platform.startswith("linux"):
            logger.debug('platform.linux_distribution: ' + str(platform.linux_distribution()))
            logger.debug('platform.libc_ver: ' + str(platform.libc_ver()))

        logger.debug('launcher_version_number.version_number: ' + launcher_version_number.version_number)
        import commit_def
        logger.debug('launcher commit hash: ' + commit_def.LATEST_COMMIT)
        logger.debug('cvlsshutils commit hash: ' + commit_def.LATEST_COMMIT_CVLSSHUTILS)
        self.contacted_massive_website = False

        self.Bind(wx.EVT_CLOSE,self.onExit)
        self.startupinfo = None
        try:
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
            self.startupinfo.wShowWindow = subprocess.SW_HIDE
        except:
            # On non-Windows systems, the previous block will throw:
            # "AttributeError: 'module' object has no attribute 'STARTUPINFO'".
            if sys.platform.startswith("win"):
                logger.debug('exception: ' + str(traceback.format_exc()))

        self.creationflags = 0
        try:
            import win32process
            self.creationflags = win32process.CREATE_NO_WINDOW
        except:
            # On non-Windows systems, the previous block will throw an exception.
            if sys.platform.startswith("win"):
                logger.debug('exception: ' + str(traceback.format_exc()))

        # launcherMainFrame.keyModel must be initialized before the
        # user presses the Login button, because the user might
        # use the Identity Menu to delete their key etc. before
        # pressing the Login button.
        self.keyModel = KeyModel(startupinfo=self.startupinfo,creationflags=self.creationflags,temporaryKey=False)
        self.keyModelCreated=threading.Event()
        self.keyModelCreated.clear()

        if options.has_key('monitor_network_checkbox'):
            if options['monitor_network_checkbox']:
                self.networkLogStopEvent.clear()
                self.networkLogThread = threading.Thread(target=self.monitorNetwork,args=[options['monitor_network_url'],self.networkLogStopEvent,self.networkLog])
                self.networkLogThread.start()
            else:
                self.networkLogStopEvent.set()

        #self.loadPrefs()

    def manageSitesEventHandler(self,event):
        t=threading.Thread(target=self.manageSites)
        t.start()

    def getSitePrefs(self,queue):
        options = self.getPrefsSection('configured_sites')
        siteList=[]
        for s in options.keys():
            if 'siteurl' in s:
                site=options[s]
                number=int(s[7:])
                enabled=options['siteenabled%i'%number]
                if enabled=='True':
                    enabled=True
                elif enabled=='False':
                    enabled=False
                name=options['sitename%i'%number]
                siteList.append({'url':site,'enabled':enabled,'name':name,'number':number})
                siteList.sort(key=lambda x:x['number'])
        queue.put(siteList)

    def getNewSites(self,queue):
        newlist=[]
        try:
            if sys.platform.startswith("linux"):
                f=open(os.path.join(sys.path[0],"masterList.url"),'r')
            else:
                f=open("masterList.url",'r')
            url=f.read().rstrip()
            logger.debug("master list of sites is available at %s"%url)
            newlist=siteConfig.getMasterSites(url)
            queue.put(newlist)
        except requests.exceptions.RequestException as e:
            logger.debug("getNewSites: Exception %s"%e)
            logger.debug("getNewSites: Traceback %s"%traceback.format_exc())
            queue.put(None)
        except Exception as e:
            logger.debug("getNewSites: Exception %s"%e)
            logger.debug("getNewSites: Traceback %s"%traceback.format_exc())
            queue.put(None)
        finally:
            f.close()

    def showSiteListDialog(self,siteList,newlist,q):
        import siteListDialog
        dlg=siteListDialog.siteListDialog(parent=self,siteList=siteList,newSites=newlist,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        r=dlg.ShowModal()
        q.put([r,dlg.getList()])

    def loadNewSitesNonBlocking(self,time=None):
        r=Queue.Queue()
        timeoutObject=object()
        threading.Thread(target=self.getNewSites,args=[r]).start()
        if time!=None:
            timer=threading.Timer(time,r.put,args=[timeoutObject])
            timer.start()
        newlist=r.get()
        if isinstance(newlist,type([])):
            pass
        elif newlist == timeoutObject:
            raise siteConfig.TimeoutException("Timeout loading new sites")
        elif newlist == None:
            raise siteConfig.TimeoutException("Timeout loading new sites")
        elif isinstance(newlist,type("")):
            raise siteConfig.StatusCode(newlist)
        else:
            raise siteConfig.CancelException("Cancelled load new sites")
        return newlist

    def manageSites(self,loadDefaultSessions=True):
        siteList=[]
        tlist=[]

        origq=Queue.Queue()
        threading.Thread(target=self.getSitePrefs,args=[origq]).start()

        wx.CallAfter(wx.BeginBusyCursor)
        retry=True
        try:
            newlist=self.loadNewSitesNonBlocking(time=10)
        except siteConfig.CancelException:
            newlist=[]
            retry=False
        except siteConfig.TimeoutException:
            newlist=[]
            retry=True
        except siteConfig.StatusCode as e:
            newlist=[]
            retry=False
            q=Queue.Queue()
            wx.CallAfter(wx.EndBusyCursor)
            event=threading.Event()
            event.clear()
            wx.CallAfter(self.createAndShowModalDialog,event,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self,title="",message=dialogs.siteListOtherException.message,ButtonLabels=dialogs.siteListOtherException.ButtonLabels,q=q)
            event.wait()
            button=q.get()
            wx.CallAfter(wx.BeginBusyCursor)

        origSiteList=origq.get()

        wx.CallAfter(wx.EndBusyCursor)

        if origSiteList==[] and newlist==[] and retry==True:

            q=Queue.Queue()
            e=threading.Event()
            e.clear()
            wx.CallAfter(self.createAndShowModalDialog,e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self,title="",message=dialogs.siteListRetry.message,ButtonLabels=dialogs.siteListRetry.ButtonLabels,q=q)
            e.wait()
            button=q.get()
            if button==0:
                retry=False
            while retry:
                try:
                    newlist=self.loadNewSitesNonBlocking(time=None)
                    if isinstance(newlist,type([])) and newlist!=[]:
                        retry=False
                    if newlist==None:
                        retry=True
                except Exception as e:
                    logger.debug("getNewSites: Exception %s"%e)
                    logger.debug("getNewSites: Traceback %s"%traceback.format_exc())
                    q=Queue.Queue()
                    e=threading.Event()
                    e.clear()
                    wx.CallAfter(self.createAndShowModalDialog,e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self,title="",message=dialogs.siteListOtherException.message,ButtonLabels=dialogs.siteListOtherException.ButtonLabels,q=q)
                    e.wait()
                    button=q.get()
                    retry=False
                if retry:
                    q=Queue.Queue()
                    e=threading.Event()
                    e.clear()
                    wx.CallAfter(self.createAndShowModalDialog,e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self,title="",message=dialogs.siteListRetry.message,ButtonLabels=dialogs.siteListRetry.ButtonLabels,q=q)
                    e.wait()
                    button=q.get()
                    if button==0:
                        retry=False
                

        q=Queue.Queue()

        import copy
        import re
        for newsite in newlist:
            if newsite.has_key('replaces'):
                replaced=False
                urls=newsite['replaces']
                siteListCopy=copy.copy(origSiteList)
                for site in siteListCopy:
                    for rurl in urls:
                        if re.search(rurl,site['url']):
                            if not newsite.has_key('enabled'):
                                newsite['enabled']=site['enabled']
                            origSiteList.remove(site)

        wx.CallAfter(self.showSiteListDialog,origSiteList,newlist,q)
        r=q.get()
        if (r[0] == wx.ID_OK):
            newSiteList=r[1]
            changed=False
            if len(newSiteList) == len(origSiteList):
                for i in range(0,len(newSiteList)):
                    if newSiteList[i]['url']!=origSiteList[i]['url'] or newSiteList[i]['enabled']!=origSiteList[i]['enabled'] or newSiteList[i]['name']!=origSiteList[i]['name']:
                        changed=True
            else:
                changed=True
            if changed:
                options={}
                i=0
                for s in newSiteList:
                    options['siteurl%i'%i]='%s'%s['url']
                    options['siteenabled%i'%i]='%s'%s['enabled']
                    options['sitename%i'%i]='%s'%s['name']
                    i=i+1

                self.prefs.remove_section('configured_sites')
                self.setPrefsSection('configured_sites',options)
                self.savePrefs(section='configured_sites')

                if loadDefaultSessions:
                    launcherMainFrame.loadDefaultSessions(True)

    def walkChildren(self,window=None,i=0,name=''):
        if window==None:
            window=self
        for item in window.GetChildren():
            if item.GetName() == name:
                return item
            else:
                r = self.walkChildren(item,i+1,name=name)
                if r!=None:
                    return r
        return None


    def loadSessionEvent(self,event):
        import SharedSessions
#        idpwindow=self.FindWindowByName(name='jobParams_aaf_idp')
#        print idpwindow
#        idp=self.FindWindowByName('jobParams_aaf_idp').GetValue()
        idp = self.walkChildren(name='jobParams_aaf_idp').GetValue()
        username = self.walkChildren(name='jobParams_aaf_username').GetValue()
#        username=self.FindWindowByName('jobParams_aaf_username').GetValue()
        s=SharedSessions.SharedSessions(self,idp=idp,username=username)
        t=threading.Thread(target=s.retrieveSession)
        t.start()
#        dlg=wx.FileDialog(self,"Load a session",style=wx.FD_OPEN)
#        status=dlg.ShowModal()
#        if status==wx.ID_CANCEL:
#            logger.debug('loadSession cancelled')
#        f=open(dlg.GetPath(),'r')
#        self.loadSession(f)
#        f.close()

    def loadSession(self,f,path=None):
        import collections
        import json
        if path!=None:
            f=open(path,'r')
        saved=siteConfig.GenericJSONDecoder().decode(f.read())
        if isinstance(saved,list):
            self.sites=collections.OrderedDict()
            keyorder=saved[0]
            for key in keyorder:
                    nk = key
                    i=1
                    while nk in self.sites.keys():
                        i=i+1
                        nk = key+" %s"%i
                    self.sites[nk]=saved[1][key]
        else:
            self.sites=saved
        cb=self.FindWindowByName('jobParams_configName')
        for i in range(0,cb.GetCount()):
            cb.Delete(0)
        for s in self.sites.keys():
            cb.Append(s)
        cb.SetSelection(0)
        if path!=None:
            f.close()
        self.loadSiteDefaults(configName=self.FindWindowByName('jobParams_configName').GetValue())
        self.loadPrefs()
        self.updateVisibility()



    def createAndShowModalDialog(self,event,dlgclass,*args,**kwargs):
        dlg=dlgclass(*args,**kwargs)
        # Do not use the return value from ShowModal. It seems on MacOS wx3.0, this event handler may run before the onClose method of the dialog
        # Resulting in ShowModal returning an incorrect value. If you need the return value, pass a queue to the dialog and get the onClose method to 
        # put a value on the queue (as is done in multiButtonDialog)
        dlg.ShowModal()
        event.set()

    def createMultiButtonDialog(self,q,*args,**kwargs):
        dlg=LauncherOptionsDialog.multiButtonDialog(*args,**kwargs)
        q.put(dlg)

    def showModalFromThread(self,dlg,q):
        r=dlg.ShowModal()
        q.put(r)

    def loadDefaultSessions(self,redraw=True):
        sites=self.getPrefsSection(section='configured_sites')
        retry=True
        while sites.keys() == [] and retry:
            q=Queue.Queue()
            e=threading.Event()
            wx.CallAfter(self.createAndShowModalDialog,event=e,dlgclass=LauncherOptionsDialog.multiButtonDialog,parent=self,message=dialogs.siteListFirstUseInfo.message,ButtonLabels=dialogs.siteListFirstUseInfo.ButtonLabels,title="",q=q)
            e.wait()
            button=q.get()
            if button==0:
                retry=False
            else:
                self.manageSites()
                return
            
        wx.CallAfter(wx.BeginBusyCursor)
        self.sites=siteConfig.getSites(self.prefs,os.path.dirname(launcherPreferencesFilePath))
        wx.CallAfter(wx.EndBusyCursor)
        wx.CallAfter(self.loadDefaultSessionsGUI,redraw)
        applicationName=self.programName
        # Something buggy in wx3.0 on MacOS. Even if the application has focus it won't render some widgets correctly
        # Using finder/osascript to refocus seems to correct this
        if sys.platform.startswith("darwin"):
            subprocess.Popen(['osascript', '-e',
                "tell application \"System Events\"\r" +
                "  set launcherApps to every process whose name contains \"" + applicationName + "\"\r" +
                "  try\r" +
                "    set launcherApp to item 1 of launcherApps\r" +
                "    set frontmost of launcherApp to true\r" +
                "    tell application \"" + applicationName + "\" to activate\r" +
                "  end try\r" +
                "end tell\r"])

    def loadDefaultSessionsGUI(self,redraw):
        cb=self.FindWindowByName('jobParams_configName')
        # attempt to preserve the selection on the combo box if the site remains in the list. If not, set the selection to 0
        try:
            sn=cb.GetValue()
        except:
            sn=''
                    
        
        if (sn==None or sn==""):
            if self.prefs.has_option("Launcher Config","siteConfigDefault"):
                sn = self.prefs.get("Launcher Config","siteConfigDefault")


        for i in range(0,cb.GetCount()):
            cb.Delete(0)
        for s in self.sites.keys():
            cb.Append(s)
        if sn!=None and sn in self.sites.keys():
            cb.SetValue(sn)
        else:
            try:
                if len(self.sites.keys())>0:
                    cb.SetSelection(0)
                else:
                    logger.debug("unable to set the default flavour. Apparently there are no flavours available")  
            except:
                logger.debug("unable to set the default flavour. Apparently there are no flavours available")  
            
        #cb.SetSelection(0)
        if (redraw):
            self.loadSiteDefaults(configName=self.FindWindowByName('jobParams_configName').GetValue())
            self.loadPrefs()
            self.updateVisibility()
        #    self.updateVisibility(self.noneVisible)

    def loadDefaultSessionsEvent(self,event):
        t=threading.Thread(target=self.loadDefaultSessions,args=[True])
        t.start()

    def saveSessionEvent(self,event):
        import SharedSessions
        idp = self.walkChildren(name='jobParams_aaf_idp').GetValue()
        username = self.walkChildren(name='jobParams_aaf_username').GetValue()
        print "idp is %s"%idp
        print "username is %s"%username
        s=SharedSessions.SharedSessions(self,idp=idp,username=username)
        t=threading.Thread(target=s.shareSession,kwargs={'loginProcess':self.loginProcess})
        t.start()

    def transferFilesEvent(self,event):
        self.loginButton.Disable()
        import cvlsshutils.skd_thread
        if not self.sanityCheck():
            print "sanitycheckFailed"
            return
        self.logStartup()
        self.buildKeyModel()
        (jobParams,siteConfig) = self.generateParameters()
        if siteConfig.provision!=None:
            progressDialog=launcher_progress_dialog.LauncherProgressDialog(self, wx.ID_ANY, "Creating VM ...", "", 2, True,self.raiseException)
            import NeCTAR
            if siteConfig.provision == 'NeCTAR':
                self.provider=NeCTAR.Provision(notify_window=progressDialog,jobParams=jobParams,imageid=siteConfig.imageid,instanceFlavour=siteConfig.instanceFlavour,keyModel=self.keyModel,username=siteConfig.username)
            else:
                self.provider=None
            def callback():
                wx.PostEvent(self.notify_window.GetEventHandler(),event)
                self.jobParams.update(self.provider.updateDict)
            def failcallback():
                self.shutdown()
            threading.Thread(target=self.provider.run,args=[callback,failcallback]).start()
        progressDialog=launcher_progress_dialog.LauncherProgressDialog(self, wx.ID_ANY, "Authorising login ...", "", 2, True,self.shutdown_skd_thread)
        self.skd = cvlsshutils.skd_thread.KeyDist(keyModel=self.keyModel,parentWindow=self,progressDialog=progressDialog,jobParams=jobParams,siteConfig=siteConfig,startupinfo=self.startupinfo,creationflags=self.creationflags)
        t=threading.Thread(target=self.authAndLogin,args=[lambda:wx.CallAfter(self.launchSFTP,jobParams,siteConfig)])
        t.start()
        event.Skip()



    def checkVersionNumber(self):
        # Check for the latest version of the launcher:
        try:
            myHtmlParser = MyHtmlParser('MassiveLauncherLatestVersionNumber')
            feed = urllib2.urlopen(LAUNCHER_URL, timeout=2)
            html = feed.read()
            myHtmlParser.feed(html)
            myHtmlParser.close()

            latestVersionNumber = myHtmlParser.latestVersionNumber
            htmlComments = myHtmlParser.htmlComments
            htmlCommentsSplit1 = htmlComments.split("<pre id=\"CHANGES\">")
            htmlCommentsSplit2 = htmlCommentsSplit1[1].split("</pre>")
            latestVersionChanges = htmlCommentsSplit2[0].strip()
            self.contacted_massive_website = True
        except:
            logger.debug(traceback.format_exc())
            self.contacted_massive_website = False
            e=threading.Event()
            e.clear()
            #wx.CallAfter(self.createAndShowModalDialog,e,wx.MessageDialog,self,"Warning: Could not contact the MASSIVE website to check version number.\n\n", "%s"%self.programName, wx.OK | wx.ICON_INFORMATION)
            e.wait()

            latestVersionNumber = launcher_version_number.version_number
            latestVersionChanges = ''

        if latestVersionNumber > launcher_version_number.version_number:
            import new_version_alert_dialog
            e=threading.Event()
            e.clear()
            wx.CallAfter(self.createAndShowModalDialog,e,new_version_alert_dialog.NewVersionAlertDialog,self,wx.ID_ANY, self.programName, latestVersionNumber, latestVersionChanges, LAUNCHER_URL)
            e.wait()
            logger.debug('Old launcher version !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            logger.debug('launcher version: ' + str(launcher_version_number.version_number))


    def buildJobParams(self,window):
        jobParams={}
        for item in window.GetChildren():
            name = item.GetName()
            if ('jobParam' in name):
                (prefix,keyname) = name.split('_',1) 
                if isinstance(item,wx.RadioBox):
                    jobParams[keyname]=item.GetSelection()
                else:
                    jobParams[keyname]=item.GetValue()
            r = self.buildJobParams(item)
            jobParams.update(r)
        if jobParams.has_key('resolution'):
            try:
                a=int(jobParams['resolution'][0])
            except:
                display = wx.Display(0)
                displaySize = display.GetGeometry().GetSize()
                # displaySize = wx.DisplaySize()
                desiredWidth = displaySize[0] * 0.99
                desiredHeight = displaySize[1] * 0.85
                jobParams['resolution'] = str(int(desiredWidth)) + "x" + str(int(desiredHeight))

        return jobParams


    def onSiteConfigChanged(self,event):
        self.Freeze()
        self.loadSiteDefaults(configName=event.GetEventObject().GetValue())
        self.loadPrefs(site=event.GetEventObject().GetValue())
        self.updateVisibility()
        self.Thaw()


    def onAdvancedVisibilityStateChanged(self, event):
        self.updateVisibility()

    def showAll(self,window=None):
        if window==None:
            window=self
        window.Show(True)
        for p in window.GetChildren():
            self.showAll(p)

    def resetLabels(self):
        relabel={}
        relabel['label_loginHost']='Server name or IP'
        relabel['label_username']='Username'
        relabel['label_hours']='Hours'
        relabel['label_mem']='Memory (GB)'
        relabel['label_nodes']='Nodes'
        relabel['label_ppn']='PPN'
        relabel['label_resolution']='resolution'
        relabel['label_cipher']='SSH tunnel cipher'
        relabel['label_config']='Site'
        relabel['label_project']='Project'
        relabel['label_debug']='Show debug window'
        relabel['label_advanced']='Show Advanced Options'
        for key in relabel.keys():
            try:
                window=self.FindWindowByName(key)
                window.SetLabel(relabel[key])
            except:
                pass

    def hideUIElements(self):
        visible={}
        visible['loginHostPanel']=False
        visible['usernamePanel']=False
        visible['projectPanel']=False
        visible['resourcePanel']=False
        visible['resolutionPanel']=False
        visible['cipherPanel']=False
        visible['debugCheckBoxPanel']=False
        visible['advancedCheckBoxPanel']=False
        visible['optionsDialog']=False
        visible['label_ppn']=False
        visible['jobParams_ppn']=False
        visible['label_mem']=False
        visible['jobParams_mem']=False
        visible['label_nodes']=False
        visible['jobParams_nodes']=False
        visible['label_hours']=False
        visible['jobParams_hours']=False
        visible['manageResButton']=False
        for k in visible.keys():
            try: 
                window=self.FindWindowByName(k)
                window.Hide()
            except:
                pass

        

    def updateVisibility(self):
        #self.showAll()
        #self.Fit()
        #self.Layout()
        self.hideUIElements()
        self.resetLabels()
        advanced=self.FindWindowByName('advancedCheckBox').GetValue()
        try:
            sc=None
            sc=self.FindWindowByName('jobParams_configName').GetValue()
            if self.sites.has_key(sc):
                visible = self.sites[sc].visibility
                relabel=self.sites[sc].relabel
                siteRanges=self.sites[sc].siteRanges
                authURL=self.sites[sc].authURL
            else:
                sc=""
                visible={}
                relabel={}
                siteRanges={}
                authURL=None
        except Exception as e:
            logger.debug('updateVisibility: looking for site %s'%sc)
            logger.debug('updateVisibility: no visibility information associated with the siteConfig configName: %s'%sc)
            logger.debug("sc: %s exception:%s"%(sc,e))
            visible={}
        for key in relabel.keys():
            try:
                window=self.FindWindowByName(key)
                window.SetLabel(relabel[key])
            except:
                pass
        for key in siteRanges.keys():
            try:
                logger.debug('setting range for %s %s %s'%(key,siteRanges[key][0],siteRanges[key][1]))
                window=self.FindWindowByName(key)
                window.SetRange(siteRanges[key][0],siteRanges[key][1])
            except Exception as e:
                logger.debug('exception setting range for %s'%key)
                logger.debug(e)
                logger.debug(traceback.format_exc())
                pass
        for key in visible.keys():
            try:
                window=self.FindWindowByName(key) #Panels and controls are all subclasses of windows
                if visible[key]==False:
                    window.Hide()
                if visible[key]==True:
                    window.Show()
                if visible[key]=='Advanced' and advanced==True:
                    window.Show()
                if visible[key]=='Advanced' and advanced==False:
                    window.Hide()
            except:
                pass # a value in the dictionary didn't correspond to a named component of the panel. Fail silently.
        globalOptions = self.getPrefsSection("Global Preferences")
        self.logWindow.Show(self.FindWindowByName('debugCheckBox').GetValue())
        self.hiddenWindow.Hide()

    def monitorNetwork(self,url,stopEvent,log,interval=2,maxlogsize=1000,timeout=5):
        import time
        import requests
        while not stopEvent.isSet():
            try:
                r=requests.get(url,verify=False,timeout=timeout)
                log.append((datetime.datetime.now(),"network OK"))
            except:
                log.append((datetime.datetime.now(),"network timed out"))
            if len(log)>maxlogsize:
                log.pop()
            time.sleep(interval)


    def onDebugWindowCheckBoxStateChanged(self, event):
        self.logWindow.Show(event.GetEventObject().GetValue())

    def onCloseDebugWindow(self, event):
        self.FindWindowByName('debugCheckBox').SetValue(False)
        self.logWindow.Show(False)

    def onHelpContents(self, event):
        from help.HelpController import helpController
        if helpController is not None and helpController.initializationSucceeded:
            helpController.DisplayContents()
        else:
            wx.MessageBox("Unable to open: " + helpController.launcherHelpUrl,
                          "Error", wx.OK|wx.ICON_EXCLAMATION)

    def onEmailHelpAtMassive(self, event):
        import webbrowser
        webbrowser.open("mailto:help@massive.org.au")

    def onSubmitDebugLog(self, event):
        logger.dump_log(launcherMainFrame,submit_log=True,showFailedToOpenRemoteDesktopMessage=False)

    def onAbout(self, event):
        dlg = LauncherMessageDialog(self, dialogs.aboutMessage.message, self.programName, helpEmailAddress="help@massive.org.au" )
        dlg.ShowModal()
        dlg.Destroy()

    def onExit(self, event):
        # Clean-up (including qdel if necessary) is now done in LoginTasks.py
        # No longer using temporary private key file, 
        # so there's no need to delete it as part of clean-up.
        if len(self.loginProcess)>0:
            dlg=LauncherOptionsDialog.multiButtonDialog(parent=self,message=dialogs.confirmQuit.message,ButtonLabels=dialogs.confirmQuit.ButtonLabels,title="")
            if dlg.ShowModal()==1:
                return
        for lp in self.loginProcess:
            logger.debug("LauncherMainFrame.onExit: calling shutdown on a loginprocess")
            lp.shutdown()

        try:
            if hasattr(self, 'loginProcess') and self.loginProcess is not None:
                logger.debug("launcher.py: onExit: Calling self.loginProcess.shutdownReal().")
                self.loginProcess.shutdownReal()
            else:
                logger.debug("launcher.py: onExit: Didn't find a login process to shut down.")

            logger.dump_log(launcherMainFrame)
            if self.skd!=None:
                try:
                    logger.debug("launcher.py: onExit: Calling self.skd.shutdownReal().")
                    self.skd.shutdownReal()
                except:
                    pass
        finally:
            os._exit(0)


    def onOptions(self, event, tabIndex=0):

        options = self.getPrefsSection("Global Preferences")
        dlg = optionsDialog.GlobalOptionsDialog(self,wx.ID_ANY,"Global Options",options,tabIndex)
        rv = dlg.ShowModal()
        if rv == wx.OK:
            options = dlg.getOptions()
            self.setPrefsSection("Global Preferences",options)
            self.savePrefs(section="Global Preferences")
        dlg.Destroy()
        options=self.getPrefsSection('Global Preferences')
        #auth_mode won't be set if, for example, this is the first use and the user displayed options then cancelled
        if options.has_key('auth_mode'): 
            auth_mode = int(options['auth_mode'])
            self.identity_menu.setRadio(auth_mode)
            self.identity_menu.disableItems(auth_mode)
        if options.has_key('monitor_network_checkbox'):
            if options['monitor_network_checkbox']:
                self.networkLogStopEvent.clear()
                self.networkLogThread = threading.Thread(target=self.monitorNetwork,args=[options['monitor_network_url'],self.networkLogStopEvent,self.networkLog])
                self.networkLogThread.start()
            else:
                self.networkLogStopEvent.set()

    def onCut(self, event):
        textCtrl = self.FindFocus()
        if textCtrl is not None:
            textCtrl.Cut()

    def onCopy(self, event):
        textCtrl = self.FindFocus()
        if textCtrl is not None:
            textCtrl.Copy()

    def onPaste(self, event):
        textCtrl = self.FindFocus()
        if textCtrl is not None:
            textCtrl.Paste()

    def onSelectAll(self, event):
        textCtrl = self.FindFocus()
        if textCtrl is not None:
            textCtrl.SelectAll()

    def SetCursor(self, cursor):
        self.massiveLoginDialogPanel.SetCursor(cursor)
        self.massiveLoginFieldsPanel.SetCursor(cursor)
        self.massiveLoginHostLabel.SetCursor(cursor)
        self.massiveProjectLabel.SetCursor(cursor)
        self.massiveHoursLabel.SetCursor(cursor)
        self.massiveVncDisplayResolutionLabel.SetCursor(cursor)
        self.massiveSshTunnelCipherLabel.SetCursor(cursor)
        self.massiveUsernameLabel.SetCursor(cursor)
        self.massiveLoginHostComboBox.SetCursor(cursor)
        self.massiveVncDisplayResolutionComboBox.SetCursor(cursor)
        self.massiveSshTunnelCipherComboBox.SetCursor(cursor)
        self.massiveProjectComboBox.SetCursor(cursor)
        self.massiveHoursField.SetCursor(cursor)
        self.massiveUsernameTextField.SetCursor(cursor)

        self.cvlLoginDialogPanel.SetCursor(cursor)
        self.cvlSimpleLoginFieldsPanel.SetCursor(cursor)
        self.cvlAdvancedLoginFieldsPanel.SetCursor(cursor)
        self.cvlConnectionProfileLabel.SetCursor(cursor)
        self.cvlConnectionProfileComboBox.SetCursor(cursor)
        self.cvlUsernameLabel.SetCursor(cursor)
        self.cvlUsernameTextField.SetCursor(cursor)
        self.cvlVncDisplayResolutionLabel.SetCursor(cursor)
        self.cvlVncDisplayResolutionComboBox.SetCursor(cursor)
        self.cvlSshTunnelCipherLabel.SetCursor(cursor)
        self.cvlSshTunnelCipherComboBox.SetCursor(cursor)

        self.buttonsPanel.SetCursor(cursor)
        self.preferencesButton.SetCursor(cursor)
        self.exitButton.SetCursor(cursor)
        self.loginButton.SetCursor(cursor)

        if self.progressDialog!=None:
            self.progressDialog.SetCursor(cursor)

        super(LauncherMainFrame, self).SetCursor(cursor)

    def queryAuthMode(self):
        var='auth_mode'
        options=self.getPrefsSection('Global Preferences')
        # Create a dialog that will never be shown just so we get an authorative list of options
        import Queue
        dq=Queue.Queue()
        dlg=LauncherOptionsDialog.multiButtonDialog(parent=self,message=dialogs.authModeFirstUseInfo.message,ButtonLabels=dialogs.authModeFirstUseInfo.ButtonLabels,title="")
        dlg.ShowModal()
        dlg = optionsDialog.GlobalOptionsDialog(self,wx.ID_ANY,"Global Options",options,0)
        dlg.tabbedView.SetSelection(2)
        dlg.ShowModal()
        dlg.saveOptions()
        options=dlg.getOptions()
        self.setPrefsSection('Global Preferences',options)
        self.savePrefs(section="Global Preferences")


    def loginComplete(self,lp,oldParams,jobParams):
        shouldSave=False
        for k in jobParams:
            if oldParams.has_key(k): 
                # This is a bit messy, but some of our parameters get converted from ints to strings
                # Specifically nodes is requsted as an int from a SpinCtrl but is updated to a string from the output of qstat.
                try:
                    if not oldParams[k] == jobParams[k] and isinstance(oldParams[k],type(jobParams[k])):
                        winName='jobParams_%s'%k
                        try:
                            self.FindWindowByName(winName).SetValue(jobParams[k])
                            shouldSave=True
                        except Exception as e:
                            logger.debug("launcher: Couldn't update the parameter %s %s %s"%(k,e,e.__class__))
                    elif isinstance(oldParams[k],int) and int(jobParams[k])!= oldParams[k]:
                        try:
                            self.FindWindowByName(winName).SetValue(int(jobParams[k]))
                            shouldSave=True
                        except Exception as e:
                            logger.debug("launcher: Couldn't update the parameter %s %s %s"%(k,e,e.__class__))
                except:
                    logger.debug('loginComlete: unable to update jobParameter %s to value %s'%(k,jobParams[k]))
        try:
            self.loginProcess.remove(lp)
        except:
            logger.debug("launcher: Couldn't remove the loginprocess")
        if shouldSave:
            wx.CallAfter(self.Refresh)
            threading.Thread(target=self.savePrefs).start()
        self.loginButton.Enable()
        options = self.getPrefsSection("Global Preferences")
        if int(options['logstats'])==0:
            import StatsLogger
            statslogger=StatsLogger.StatsLogger(options['uuid'],success=True,jobParams=jobParams)
            threading.Thread(target=statslogger.post,args=["https://cvl.massive.org.au/logstats"]).start()

    def loginCancel(self,lp,oldParams,jobParams):
        self.loginProcess.remove(lp)
        self.loginButton.Enable()
        options = self.getPrefsSection("Global Preferences")
        if int(options['logstats'])==0:
            import StatsLogger
            statslogger=StatsLogger.StatsLogger(options['uuid'],success=False,jobParams=jobParams)
            threading.Thread(target=statslogger.post,args=["https://cvl.massive.org.au/logstats"]).start()


    def onLoginProcessComplete(self, jobParams):
        self.loginProcess = None
        logger.debug("launcher.py: onLogin: Enabling login button.")
        # The refresh below is a workaround for a Windows bug where a
        # dark-coloured rectangle appears in the middle of the main
        # dialog's current panel after a completed or cancelled login session:
        self.massiveLoginDialogPanel.Refresh()
        self.cvlLoginDialogPanel.Refresh()
        self.loginButton.Enable()

    def authAndLogin(self,nextSub,button=None):
        try:
            print "running skd.authorise"
            self.skd.authorise()
            print "skd authorise completed"
            if not self.skd.canceled():
                print "running nextSub"
                self.progressDialog=None
                try:
                    if button!=None:
                        button.Enable()
                except:
                    pass
                try:
                    wx.EndBusyCursor()
                except:
                    pass
                nextSub()
            else:
                try:
                    if button!=None:
                        button.Enable()
                    self.shutdown_skd_thread()
                    try:
                        if button!=None:
                            button.Enable()
                    except:
                        pass
                except:
                    pass
                try:
                    wx.EndBusyCursor()
                except:
                    pass

                logger.debug(self.skd.cancelMessage)
                pass
        except Exception as e:
            print e
            import traceback
            print traceback.format_exc()
            print "skd exception"

            pass
        
    def logStartup(self):
        import platform
        platformstr="\""
        platformstr=platformstr+'platform.machine: '       + str(platform.machine())
        platformstr=platformstr+' platform.node: '          + str(platform.node())
        platformstr=platformstr+' platform.platform: '      + str(platform.platform())
        platformstr=platformstr+' platform.processor: '     + str(platform.processor())
        platformstr=platformstr+' platform.release: '       + str(platform.release())
        platformstr=platformstr+' platform.system: '        + str(platform.system())
        platformstr=platformstr+' platform.version: '       + str(platform.version())
        platformstr=platformstr+"\""
        logging.debug(platformstr)

    def sanityCheck(self):
        configName=self.FindWindowByName('jobParams_configName').GetValue()
        if configName=="" or configName==None:
            dlg=LauncherMessageDialog(self,"Please select a site to log into first","Please select a site")
            dlg.ShowModal()
            return False
        if self.FindWindowByName('usernamePanel').IsShownOnScreen() and (self.FindWindowByName('jobParams_username').GetValue()=="" or self.FindWindowByName('jobParams_username').GetValue()==None):
            dlg = LauncherMessageDialog(self,
                    "Please enter your username.",
                    self.programName)
            dlg.ShowModal()
            self.loginButton.Enable()
            usernamefield = self.FindWindowByName('jobParams_username')
            usernamefield.SetFocus()
            return False
        return True

    def buildKeyModel(self):
        if self.keyModelCreated.is_set():
            logger.debug("keyModel is already created, returning existing model")
            return
        dotSshDir = os.path.join(os.path.expanduser('~'), '.ssh')
        if not os.path.exists(dotSshDir):
            os.makedirs(dotSshDir)
        options=self.getPrefsSection('Global Preferences')
        while not options.has_key('auth_mode'):
            self.queryAuthMode()
            options=self.getPrefsSection('Global Preferences')
        if int(options['auth_mode'])==LauncherMainFrame.TEMP_SSH_KEY:
            logger.debug("launcherMainFrame.onLogin: using a temporary Key pair")
            try:
                if 'SSH_AUTH_SOCK' in os.environ:
                    os.environ['PREVIOUS_SSH_AUTH_SOCK'] = os.environ['SSH_AUTH_SOCK']
                del os.environ['SSH_AUTH_SOCK']
                logger.debug("launcherMainFrame.onLogin: spawning an ssh-agent (not using the existing agent)")
            except:
                logger.debug("launcherMainFrame.onLogin: spawning an ssh-agent (no existing agent found)")
                pass
            logger.debug("creating a temporary keymodel")
            self.keyModel=KeyModel(temporaryKey=True,startupinfo=self.startupinfo)
        else:
            logger.debug("creating a long term keymodel")
            logger.debug("launcherMainFrame.onLogin: using a permanent Key pair")
            self.keyModel=KeyModel(temporaryKey=False,startupinfo=self.startupinfo)
        self.keyModelCreated.set()


    def generateParameters(self):
        jobParams=self.buildJobParams(self)
        jobParams['wallseconds']=int(jobParams['hours'])*60*60
        configName=self.FindWindowByName('jobParams_configName').GetValue()
        siteConfig=self.sites[configName]
        update={}
        update['sshBinary']=self.keyModel.getsshBinary()
        update['launcher_version_number']=launcher_version_number.version_number
        if siteConfig.loginHost!=None:
            update['loginHost']=siteConfig.loginHost
        if siteConfig.username!=None:
            update['username']=siteConfig.username
        jobParams.update(update)
        return (jobParams,siteConfig)

    def raiseException(self):
        raise Exception("user canceled login")

    def shutdown_skd_thread(self):
        try:
            self.skd._stopped.set()
            self.skd._exit.set()
        except:
            pass
        logger.debug("resetting the keymodel")
        self.keyModelCreated.clear()
        self.skd.progressDialog.Hide()
        self.loginButton.Enable()


    def onManageReservations(self,event):
        self.manageResButton.Disable()
        import cvlsshutils.skd_thread
        self.logStartup()
        logger.debug("building a new keymodel")
        self.buildKeyModel()
        (jobParams,siteConfig) = self.generateParameters()
        progressDialog=launcher_progress_dialog.LauncherProgressDialog(self, wx.ID_ANY, "Authorising login ...", "", 2, True,cancelCallback=self.shutdown_skd_thread)
        self.skd = cvlsshutils.skd_thread.KeyDist(keyModel=self.keyModel,parentWindow=self,progressDialog=progressDialog,jobParams=jobParams,siteConfig=siteConfig,startupinfo=self.startupinfo,creationflags=self.creationflags)
        t=threading.Thread(target=self.authAndLogin,args=[lambda:wx.CallAfter(self.showReservationDialog,jobParams,siteConfig),self.manageResButton])
        t.start()
        event.Skip()


    def onLogin(self, event):
        self.loginButton.Disable()
        import cvlsshutils.skd_thread
        if not self.sanityCheck():
            print "sanitycheckFailed"
            return
        self.logStartup()
        self.buildKeyModel()
        (jobParams,siteConfig) = self.generateParameters()
        if siteConfig.provision!=None:
            progressDialog=launcher_progress_dialog.LauncherProgressDialog(self, wx.ID_ANY, "Creating VM ...", "", 2, True,self.raiseException)
            import NeCTAR
            if siteConfig.provision == 'NeCTAR':
                self.provider=NeCTAR.Provision(notify_window=progressDialog,jobParams=jobParams,imageid=siteConfig.imageid,instanceFlavour=siteConfig.instanceFlavour,keyModel=self.keyModel,username=siteConfig.username)
            else:
                self.provider=None
            def callback():
                wx.PostEvent(self.notify_window.GetEventHandler(),event)
                self.jobParams.update(self.provider.updateDict)
            def failcallback():
                self.shutdown()
            threading.Thread(target=self.provider.run,args=[callback,failcallback]).start()
        progressDialog=launcher_progress_dialog.LauncherProgressDialog(self, wx.ID_ANY, "Authorising login ...", "", 2, True,self.shutdown_skd_thread)
        self.skd = cvlsshutils.skd_thread.KeyDist(keyModel=self.keyModel,parentWindow=self,progressDialog=progressDialog,jobParams=jobParams,siteConfig=siteConfig,startupinfo=self.startupinfo,creationflags=self.creationflags)
        print "created skd"
        t=threading.Thread(target=self.authAndLogin,args=[lambda:wx.CallAfter(self.launchVNC,jobParams,siteConfig),self.loginButton])
        t.start()
        event.Skip()

    def showReservationDialog(self,jobParams,siteConfig):
        import reservationDialog
        q=Queue.Queue()
        dlg=reservationDialog.reservationsDialog(rqueue=q,parent=self,siteConfig=siteConfig,jobParams=jobParams,buttons=['New','Delete','Cancel'],startupinfo=self.startupinfo,creationflags=self.creationflags)
        res=dlg.ShowModal()
        self.manageResButton.Enable()

    def launchSFTP(self,jobParams,siteConfig):
        try:
            logger.debug('attempting to launch sftp')
            import subprocess
            if sys.platform.startswith("darwin"):
                opener="open"
                shell=False
            elif sys.platform.startswith("win"):
                opener="start"
                shell=True
            elif sys.platform.startswith("linux"):
                opener="filezilla"
                shell=False
            rv=subprocess.call([opener,'sftp://%s@%s'%(jobParams['username'],siteConfig.loginHost)],shell=shell,startupinfo=self.startupinfo,creationflags=self.creationflags)
            if rv!=0:
                queue=Queue.Queue()
                wx.CallAfter(self.missingHandler(),queue=queue)
                queue.get()
        except Exception as e:
            logger.debug('caught exception %s'%e)
            logger.debug(traceback.format_exc())
            queue=Queue.Queue()
            wx.CallAfter(self.showThankyou(),queue=queue)
            queue.get()

    def missingHandler(self):
        msg="""
Thanks for your interest in the new file transfer feature of Strudel
In order to transfer files to your desktop you need to install an sftp client. 
FileZilla would be a good choice on all platforms (https://filezilla-project.org/)
On Windows this could also be winscp or Cyberduck. Mac's can use Cyberduck
"""
        dlg = LauncherMessageDialog(self, msg, self.programName, helpEmailAddress="help@massive.org.au" )



    def showThankyou(self):
        msg="""
Thanks for your interest in the new file transfer feature of Strudel
At the moment this feature isn't expected to work except maybe on Linux and Mac systems (if you're very lucky and the moon is in the correct phase and the stars all align)
But we'd still appreciate hearing about your experience. We just might not be able to make it work for you right now.
"""
        dlg = LauncherMessageDialog(self, msg, self.programName, helpEmailAddress="help@massive.org.au" )



    def launchVNC(self,jobParams,siteConfig):

        print "attempting to start a vnc server"
        logger.debug("attempting to start a vnc server")

        userCanAbort=True
        maximumProgressBarValue = 10
        self.savePrefs(section="Global Preferences")
        autoExit=False
        globalOptions = self.getPrefsSection("Global Preferences")
        lp=LoginTasks.LoginProcess(self,jobParams,self.keyModel,siteConfig,displayStrings=siteConfig.displayStrings,autoExit=autoExit,globalOptions=globalOptions,startupinfo=self.startupinfo)
        oldParams  = jobParams.copy()
        lp.setCallback(lambda jobParams: self.loginComplete(lp,oldParams,jobParams))
        lp.setCancelCallback(lambda jobParams: self.loginCancel(lp,oldParams,jobParams))
        self.loginProcess.append(lp)
        lp.doLogin()

class LauncherStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent)

        self.SetFieldsCount(2)
        #self.SetStatusText('Welcome to MASSIVE', 0)
        self.SetStatusWidths([-5, -2])

class MyApp(wx.App):
    def OnInit(self):

        appDirs = appdirs.AppDirs("strudel", "Monash University")
        appUserDataDir = appDirs.user_data_dir
        # Add trailing slash:
        appUserDataDir = os.path.join(appUserDataDir,"")
        if not os.path.exists(appUserDataDir):
            os.makedirs(appUserDataDir)

        global launcherPreferencesFilePath 
        launcherPreferencesFilePath = os.path.join(appUserDataDir,"strudel.cfg")

        if sys.platform.startswith("win"):
            os.environ['CYGWIN'] = "nodosfilewarning"

        logger.setGlobalLauncherPreferencesFilePath(launcherPreferencesFilePath)
        sys.modules[__name__].launcherMainFrame = LauncherMainFrame(None, wx.ID_ANY, 'Strudel')
        launcherMainFrame = sys.modules[__name__].launcherMainFrame
        launcherMainFrame.SetStatusBar(launcherMainFrame.loginDialogStatusBar)
        launcherMainFrame.SetMenuBar(launcherMainFrame.menu_bar)
        launcherMainFrame.GetSizer().Fit(launcherMainFrame)
        launcherMainFrame.Layout()
        launcherMainFrame.Center()
        launcherMainFrame.Show(True)
        evt=wx.PyCommandEvent(wx.wxEVT_COMMAND_MENU_SELECTED,id=launcherMainFrame.loadDefaultSessionsId)
        wx.PostEvent(launcherMainFrame.GetEventHandler(),evt)
        t=threading.Thread(target=launcherMainFrame.checkVersionNumber)
        t.start()

        return True

if __name__ == '__main__':
    
    # All multithread Xorg application need call XInitThreads before any work with Xorg or some xcb will abort with
    #    [xcb] Most likely this is a multi-threaded client and XInitThreads has not been called
    # As XInitThreads is not garanteed to be called on all Linux distributions (like Fedora 23), we better do it here.
    import sys
    if sys.platform.startswith('linux'):
        try:
            import ctypes
            x11 = ctypes.cdll.LoadLibrary('libX11.so.6')
            x11.XInitThreads()
        except:
            pass
        
    app = MyApp(False) # Don't automatically redirect sys.stdout and sys.stderr to a Window.
    app.MainLoop()
