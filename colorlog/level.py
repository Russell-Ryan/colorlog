

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

        
        
    def __call__(self,txt):
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

    
    
