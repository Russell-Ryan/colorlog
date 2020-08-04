import sys
import datetime
import re
import os
import inspect
from timeit import default_timer
from .level import Level
from .device import Device

class ColorLog(dict):
    ''' Constructor for the ColorLog class.
    
    
    Parameters
    ----------
       root : str
          rootname of output log file


    0: debug
    1: info
    2: warn
    3: alarm
    


    '''

    
    NUM=74        # number of characters to print to file    
    def __init__(self,root=None,timestamp=True,stdout=True,stderr=True):  
        
        # get the starting time
        self.t0=default_timer()

        # if the root was not set, then use the caller
        if root is None:
            q=inspect.stack()[1]
            root=os.path.splitext(q[1])[0]
        

        # build a regular expression
        self.regex=re.compile('\[[A-Za-z]+\]')               

        # name the output file
        logfile='{}.log'.format(root)
        path=os.path.dirname(logfile)
        if path=='':
            path=os.getcwd()
        
        # try opening the file
        if os.access(path,os.W_OK):
            self.logfile=Device(open(logfile,'w'),enabled=True)        
        else:
            self.logfile=Device(None,enabled=False)
            
        date,time,day=self.now(pm=True)
        self.logfile.write(' +-'+self.NUM*'-'+'-+ \n')
        self.writeLine('')
        self.writeLine('Log for: {}'.format(root))
        self.writeLine('         {}, {}'.format(day,date))
        self.writeLine('         {}'.format(time))
        self.writeLine('')
        self.logfile.write(' +-'+self.NUM*'-'+'-+ \n\n')
        self.logfile.device.flush()
        
        # record the levels
        self.addlevel('info',foreground='green')
        self.addlevel('warn',foreground='yellow')
        self.addlevel('alarm',foreground='red',blink=True)
        self.addlevel('debug',foreground='blue',italic=True)

        # do we write to STDOUT?
        self.stdout=Device(sys.stdout,enabled=stdout)
        sys.stdout=self
                
        # do we write to STDERR
        self.stderr=Device(sys.stderr,enabled=stderr)
        sys.stderr=self

            
    def addlevel(self,name,**kwargs):
        self[name]=Level(name,**kwargs)
            
    def now(self,pm=False):
        now=datetime.datetime.now()
        day=now.strftime("%a")
        date=now.strftime("%b/%d/%Y")
        if pm:
            time=now.strftime("%I:%M:%S %p")
        else:
            time=now.strftime("%H:%M:%S")
        return date,time,day

    
    def writeLine(self,text):
        n=max(self.NUM-len(text),0)
        self.logfile.write(' | '+text+' '*n+' | \n')


    def default(self,line):
        self.stdout.write(line)
        self.logfile.write(line)
        self.logfile.device.flush()        
        

    def write(self,line):
        
        # look for logging options
        match=self.regex.match(line)
        if match:
            level=match.group(0)[1:-1]
            text=line[match.end(0):]           
            if level in self:
                self.stdout.write(self[level](text))

                date,time,day=self.now(pm=False)
                out='[{}@{}-{}] {}'.format(level,date,time,text)    
                self.logfile.write(out)
                self.logfile.device.flush()
            else:
                self.default(line)
        else:
            self.default(line)

    
    def __str__(self):
        out='Color logging with:\n'
        tmp=['  {}:\n{}'.format(k,str(v)) for k,v in self.items()]
        return out+'\n'.join(tmp)
        

    def flush(self):
        pass

    def __del__(self):
        self.logfile.write('\n\n')
        self.logfile.write(' +-'+self.NUM*'-'+'-+ \n')
        self.writeLine(' ')
        self.writeLine('Finished:')
        self.writeLine('run time: {}'.format(default_timer()-self.t0))
        self.writeLine(' ')
        self.logfile.write(' +-'+self.NUM*'-'+'-+ \n')
        self.logfile.device.close()
        sys.stdout=self.stdout.device
        sys.stderr=self.stderr.device


