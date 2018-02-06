import wx
class Provision(object):
    def __init__(self,notify_window):
        self.notify_window=notify_window

    def run(self,event):
        logger.debug("Running Provisioning")
