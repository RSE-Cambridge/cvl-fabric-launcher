class StatsLogger():
    def __init__(self,uuid=None,platform=None,success=True,jobParams=None,*args,**kwargs):
        self.uuid=uuid
        self.platform=platform
        self.success=success
        self.jobParams=jobParams
        if self.platform==None:
            import platform
            platformstr="\""
            platformstr=platformstr+'platform.machine: '      + str(platform.machine())+'\n'
            platformstr=platformstr+'platform.node: '          + str(platform.node())+'\n'
            platformstr=platformstr+'platform.platform: '      + str(platform.platform())+'\n'
            platformstr=platformstr+'platform.processor: '     + str(platform.processor())+'\n'
            platformstr=platformstr+'platform.release: '       + str(platform.release())+'\n'
            platformstr=platformstr+'platform.system: '        + str(platform.system())+'\n'
            platformstr=platformstr+'platform.version: '       + str(platform.version())+'\n'
            platformstr=platformstr+"\""
            self.platform=platformstr


    def post(self,url=""):
        import requests
        data={}
        try:
            data['uuid']=self.uuid
            data['platform']=self.platform
            data['success']=self.success
            data['loginHost']=self.jobParams['jobParam_loginHost']
        except:
            pass
        try:
            requests.post(url,data=data,verify=False)
        except:
            pass
