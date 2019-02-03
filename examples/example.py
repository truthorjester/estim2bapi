import estim2b
import time

def jolt(e2b, jpower=None, jtime=None):
    if jpower is None: jpower = 2
    if jtime is None: jtime = 3
    print 'power={}; time={}'.format(jpower, jtime)
    e2b.setOutputs(jpower, jpower)
    time.sleep(jtime)
    e2b.kill()

def jolt_simple(e2b, jpower=None, jtime=None):
    ''' Same as above, but simpler (uses kill_after keyword) '''
    if jpower is None: jpower = 2
    if jtime is None: jtime = 3
    print 'power={}; time={}'.format(jpower, jtime)
    e2b.setOutputs(jpower, jpower, kill_after=jtime)

# for Linux, device addr on Windows and Mac will be different.
e2b = estim2b.Estim()
#e2b.getStatus()
e2b.setLow()

# quick status update, tests connection etc
print e2b.status()

# change the mode and send a 2.5 second jolt
e2b.setMode('throb')
e2b.set(10, 10)
time.sleep(3)
e2b.set(0, 0)
jolt(e2b, 3, 3)
print e2b.status()

e2b.setMode('bounce')
e2b.setHigh()
print e2b.status()



