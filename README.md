# ColorLog




## example usage

```
import colorlog

# create the log
log=colorlog.ColorLog(root='test')

# show the standard levels
print('[info]an informational message')
print('[warn]an warning message')
print('[alarm]an alarm')
print('[debug]a debugging message')
print('basic printing')

# add a personal level
log.addlevel('mine',foreground='magenta')
print('[mine]personal message')

# change the formatting of an existing level
log['info']['underline']=True
print('[info]a changed, informational message')

# change the color of an existing level
log['info']['foreground']='white'
print('[info]another changed, informational message')

# turn off the ascii logging
log.logfile.disable()
print('[warn]hide a message from the logfile')
log.logfile.enable()
    
# turn off the STDOUT
log.stdout.disable()
print('suppress STDout')
log.stdout.enable()
print("and... we're back")

# raise an error and see that the log is updated too!
raise RuntimeError('this is an exception')

```