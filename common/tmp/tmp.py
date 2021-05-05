from ROOT import gSystem



gSystem.Load('fake_C.so')

from ROOT import getDYWeight
from ROOT import shutdown

print 'return = ', getDYWeight(1.)

shutdown()
