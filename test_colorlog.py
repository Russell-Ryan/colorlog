from colorlog import ColorLog
import sys

def test():

    # get the name of the log (to make changes)
    log=ColorLog(root='test_colorlog')

    # show the standard levels
    print('[info]an informational message')
    print('[warn]an warning message')
    print('[alarm]an alarm')
    print('[debug]a debugging message')
    print('basic printing')

    # add a personal level
    log.add_level('mine',foreground='magenta')
    print('[mine]personal message')

    # change the formatting of an existing level
    log['info']['underline']=True
    print('[info]a changed, informational message')

    # change the color of an existing level
    log['info']['foreground']='white'
    print('[info]another changed, informational message')

    # turn off the ascii logging
    log.logging=False
    print('[warn]hide a message from the logfile, but show to terminal')
    log.logging=True  # ok turn it back on
    
    # turn off the STDOUT
    log.printing=False
    print('suppressed STDout')
    log.printing=True
    print("and... we're back")

    # maybe you don't like the timestamps?  turn them off:
    log.timestamp=False
    print('[info]no timestamps now')


    # you can even close, and reopen the file
    log.close()
    print('nothing gets logged, since the file is closed')
    log.reopen()
    print("and we're back after closing")

    # you can disable certain modes.
    log.disable('debug') # turns off the debugging level
    print("[debug]nothing happened, since this is off")
    # well, there's an issue yet to be dealt with where it prints a blank line.

    # it works with tqdm, sort-of
    import tqdm
    import inspect
    import time
    inspect.builtins.print=tqdm.tqdm.write   # need to do this :(

    for i in tqdm.tqdm(range(10)):
        time.sleep(0.1)
        print('[info]{}'.format(i))


if __name__=='__main__':

    test()
    

