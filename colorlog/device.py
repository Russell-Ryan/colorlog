class Device(object):
    def __init__(self,device,enabled=True):
        self._device=device
        self.enabled=enabled    

    @property
    def device(self):
        return self._device
    
    def write(self,text):
        if self.enabled:
            self._device.write(text)

    def enable(self):
        self.enabled=True

    def disable(self):
        self.enabled=False
