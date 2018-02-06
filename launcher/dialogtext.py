
class dialog(object):
    def __init__(self,*args,**kwargs):
        super(dialog,self).__init__(*args,**kwargs)
        self.message=""
        self.ButtonLabels=[]
        self.title=""

class default(object):
    def __init__(self,*args,**kwargs):
        super(default,self).__init__(*args,**kwargs)
        self.siteListRetry=dialog()
        self.siteListRetry.message="It looks like I was unable to contact the server for a list of sites to connect to. If your on a VPN you may want to check your network connectivity"
        self.siteListRetry.ButtonLabels=["Cancel","Retry"]
        self.siteListOtherException=dialog()
        self.siteListOtherException.message="An error occured while trying to retrieve the site list. You can continue, but you will need to configure the list of sites manually."
        self.siteListOtherException.ButtonLabels=["OK"]
        self.siteListFirstUseInfo=dialog()
        self.siteListFirstUseInfo.message="Before you can use this program, you must select from a list of computer systems that you commonly use.\n\nBy checking and unchecking items in this list you can control which options appear in the dropdown menu of which computer to connect to.\n\nYou can access this list again from the File->Manage Sites menu."
        self.siteListFirstUseInfo.ButtonLabels=["Cancel","OK"]
        self.loadingFlavours=dialog()
        self.loadingFlavours.message="Loading flavours"
        self.loadingSiteList=dialog()
        self.loadingSiteList.message="Loading Site List"
        self.loadingSiteList.ButtonLabels=["Cancel"]
        self.shutdownInstance=dialog()
        self.shutdownInstance.message="Would you like to shutdown this VM?"
        self.shutdownInstance.ButtonLabels=["Yes","No"]
        self.existingVM=dialog()
        self.existingVM.message="Would you like use an existing VM or start a new one?"
        self.existingVM.ButtonLabels=["Cancel","Existing","New"]
        self.confirmQuit=dialog()
        self.confirmQuit.message="Are you sure you want to quit?"
        self.confirmQuit.ButtonLabels=["Yes","No"]
        self.authModeFirstUseInfo = dialog()
        self.authModeFirstUseInfo.message="""
This program logs you into other computers. As such it deals with such scary issues as Authentication.

The default behaviour may not be suitable if your laptop or workstation is shared by multiple people.

You can read more by selecting "Identity->Authentication options" from the menu.

I'll now show you what happens when you select "Identity->Authentication options" so you can confirm your choices.
"""
        self.authModeFirstUseInfo.ButtonLabels=["OK"]


        self.queryAuthMode=dialog()
        self.queryAuthMode.message = """
Would you like to use an SSH key pair or your password to authenticate yourself?

If this computer is shared by a number of people then passwords are preferable.

If this computer is not shared, then an SSH key pair will give you advanced features for managing your access.
"""
        import commit_def
        import launcher_version_number
        msg="Strudel is the ScienTific Remote Desktop Launcher\n\n"
        msg=msg+"Strudel was created with funding through the NeCTAR Characterisation Virtual Laboratory by the team at the Monash e-Research Center (Monash University, Australia)\n\n"
        msg=msg+"Strudel is open source (GPL3) software available from https://github.com/CVL-dev/cvl-fabric-launcher\n\n"
        msg=msg+"Version " + launcher_version_number.version_number + "\n" + 'Strudel Commit: ' + commit_def.LATEST_COMMIT + '\n' + 'cvlsshutils Commit: ' + commit_def.LATEST_COMMIT_CVLSSHUTILS + '\n'
        self.aboutMessage=dialog()
        self.aboutMessage.message=msg
        msg="You must start a desktop (i.e. Login) before you can share it with a collaborator"
        self.shareFailedMessage=dialog()
        self.shareFailedMessage.message=msg
        msg="Ask your collaborator to enter the words:\n \"{key}\"\n and login with their account"
        self.shareKeyMessage=dialog()
        self.shareKeyMessage.message=msg


    
