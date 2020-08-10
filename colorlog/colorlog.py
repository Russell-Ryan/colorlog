import sys
import re
import os
from datetime import datetime
import inspect
from timeit import default_timer


    
class Attribute(object):
    def __init__(self,ttype,value):
        self._ttype=ttype
        self._value=value

    def __eq__(self,k):
        return self._value == k

    def __bool__(self):
        if self._ttype == bool:
            return self._value
        else:
            return True
        
    def __str__(self):
        return str(self._value)
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,value):
        if isinstance(value,self._ttype):
            self._value=value

    def lower(self):
        if self._ttype == str:
            return self._value.lower()

    

            
class Level(object):
    def __init__(self,level,delimiter='>',foreground='red',background='none',
                 blink=False,italic=False,underline=False):

        self.level=level

        self._data={'delimiter':Attribute(str,delimiter),
                    'foreground':Attribute(str,foreground),
                    'background':Attribute(str,background),
                    'blink':Attribute(bool,blink),
                    'italic':Attribute(bool,italic),
                    'reversed':Attribute(bool,False),
                    'underline':Attribute(bool,underline)}
        self.setformat()

    def __str__(self):
        tok=['{:>20}: {}'.format(k,v) for k,v in self._data.items()]
        return '\n'.join(tok)
            
        
        
        
    def _foreground(self,bold=True):
        name=self['foreground'].lower()
        bold=';1' if bold else ''
        if name=='black': col='\033[30{}m'.format(bold)
        elif name == 'red': col='\033[31{}m'.format(bold)
        elif name=='green': col='\033[32{}m'.format(bold)
        elif name=='yellow': col='\033[33{}m'.format(bold)
        elif name=='blue': col='\033[34{}m'.format(bold)
        elif name=='magenta': col='\033[35{}m'.format(bold)
        elif name=='cyan': col='\033[36{}m'.format(bold)
        elif name=='white': col='\033[37{}m'.format(bold)
        else: col=''
        return col

    def _background(self,bold=True):
        name=self['background'].lower()
        bold=';1' if bold else ''
        if name=='black': col='\033[40{}m'.format(bold)
        elif name == 'red': col='\033[41{}m'.format(bold)
        elif name=='green': col='\033[42{}m'.format(bold)
        elif name=='yellow': col='\033[43{}m'.format(bold)
        elif name=='blue': col='\033[44{}m'.format(bold)
        elif name=='magenta': col='\033[45{}m'.format(bold)
        elif name=='cyan': col='\033[46{}m'.format(bold)
        elif name=='white': col='\033[47{}m'.format(bold)
        else: col=''
        return col

    def _boolean(self,blinkable=False):
        out=''
        if self['bold']: out+='\033[1m'
        if self['faint']: out+='033[2m'
        if self['italic']: out+='\033[3m'
        if self['underline']: out+='\033[4m'
        if self['blink'] and blinkable: out+='\033[5m'
        if self['reversed']: out+='\033[7m'
        if self['empty']: out+='\033[8m'
        return out

    def setformat(self):
        fg1=self._foreground(bold=True)
        fg2=self._foreground(bold=False)
        b2=self._boolean(blinkable=True)

        fmt='{fg1}{lvl}{delim}\033[00m{fg2} {b2}{txt}\033[00m'
        self.fmt=fmt.format(fg1=fg1,lvl=self.level,delim=self['delimiter'],
                            fg2=fg2,b2=b2,txt='{}')

        
        
    def format(self,txt):
        return self.fmt.format(txt)

    
    def __setitem__(self,k,v):
        if k in self._data:
            self._data[k].value=v
            self.setformat()
        

    def __contains__(self,k):
        return k in self._data
    
    def __getitem__(self,k):
        if k in self:
            return self._data[k]
        else:
            return None

    
    

class ColorLog(object):
    NUM=74
    _instance=None

    
    def __new__(cls,root=None,timestamp=True):
        if cls._instance is None:
            self=cls._instance=super(ColorLog,cls).__new__(cls)
            

            self.logging=True
            self.printing=True

            
            self.t0=default_timer()   # save teh start time

            self.timestamp=timestamp
            # make a filename root
            if root is None:
                q=inspect.stack()[1]
                root=os.path.splitext(q[1])[0]

            # get the name of a file
            self.logfile='{}.log'.format(root)

            # get the path to the log file 
            path=os.path.dirname(self.logfile)
            if path=='':
                path=os.getcwd()
                
            # try opening the file
            try:
                self.file=open(self.logfile,'w')
            except:
                self.file=None


            # put some stuff in the header of the logfile
            if self.file:
                self.write_header(root)
            

            # set stuff for the levels
            self.enabled=[]
            self.levels={}
            self.add_level('debug',foreground='blue',italic=True)
            self.add_level('info',foreground='green')
            self.add_level('warn',foreground='yellow')
            self.add_level('alarm',foreground='red',blink=True)
            self.enable('normal')    # enable the printing
            
            # build a regular expression
            self.regex=re.compile('\[[A-Za-z]+\]')

            self.stdout=sys.stdout
            sys.stdout=self

        return self
            
    def add_level(self,name,**kwargs):
        self.levels[name]=(len(self.levels),Level(name,**kwargs))
        self.enable(name)

    def write_header(self,root):

        format = lambda txt: ' | '+txt+' '*max(self.NUM-len(txt),0)+' |'


        end='\n'
        
        now=datetime.now()
        day=now.strftime("%a")
        date=now.strftime("%b/%d/%Y")
        time=now.strftime("%I:%M:%S %p")
        print(' /-'+self.NUM*'-'+"-\\",file=self.file,end=end)
        print(format(''),file=self.file,end=end)
        print(format(' {} log'.format(root)),file=self.file,end=end)
        print(format(' {}, {} at {}'.format(day,date,time)),file=self.file,end=end)
        print(format(''),file=self.file,end=end)
        print(' \\-'+self.NUM*'-'+"-/\n",file=self.file,end=end)
        

    def write_footer(self):
        format = lambda txt: ' | '+txt+' '*max(self.NUM-len(txt),0)+' |'

        
        end='\n'
        t1=default_timer()
        print('\n /-'+self.NUM*'-'+"-\\",file=self.file,end=end)
        print(format(''),file=self.file,end=end)
        print(format('Finished.'),file=self.file,end=end)
        print(format('run time: {} s'.format(t1-self.t0)),file=self.file,end=end)
        print(format(''),file=self.file,end=end)
        print(' \\-'+self.NUM*'-'+"-/\n",file=self.file,end=end)
        
        
        


        
    def enable(self,*names):
        for name in names:
            if name in self.levels and name not in self.enabled:
                self.enabled.append(name)
            elif name =='normal':                
                self.enabled.append(name)
                self.end =''

    def disable(self,*names):
        for name in names:
            if name in self.enabled:
                self.enabled.remove(name)
                if name=='normal':
                    self.end='\n'
                
    def flush(self):
        pass
    
    def write(self,line):
        match=self.regex.match(line)
        if match:
            name=match.group(0)[1:-1]
            text=line[match.end(0):]        
            #if name in self.enabled:
            if name in self.levels:
                if name in self.enabled:
                    if self.timestamp:
                        now=datetime.now()
                        date=now.strftime("%b/%d/%Y")
                        time=now.strftime("%H:%M:%S")
                        log='[{} {}T{}] {}'.format(name,date,time,text)
                    else:
                        log='[{}] {}'.format(name,text)
                        
                    level,obj = self.levels[name]
                    self._printer(obj.format(text))
                    self._logger(log)
                else:
                    pass  # this level has been disabled, still prints a blank
                          # line.  this is strange to me?
            else:
                self._printer(line)
                self._logger(line)
                
        elif 'normal' in self.enabled:
            self._printer(line)
            self._logger(line)


    def _printer(self,txt):
        if self.printing:
            print(txt,file=self.stdout,end=self.end)
            
    def _logger(self,txt):
        if self.logging:
            print(txt,file=self.file,end=self.end)
            
            
    def reopen(self):
        self.file=open(self.logfile,'a')
        self.stdout=sys.stdout
        sys.stdout=self
        
            
    def close(self):
        if not self.file.closed:
            sys.stdout=self.stdout
            self.file.close()
    
    def __del__(self):        
        if not self.file.closed:
            self.write_footer()
            self.close()

    def __getitem__(self,k):
        return self.levels[k][1]

    
           
