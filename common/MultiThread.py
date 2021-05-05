#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Izaak Neutelings (2017)
# Source: https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
#         https://stackoverflow.com/questions/10415028/how-can-i-recover-the-return-value-of-a-function-passed-to-multiprocessing-proce/28799109
#from threading import Thread as _Thread
from multiprocessing import Process, Pipe

class Thread(Process):
    """Class to get return from multithread"""
    def __init__(self, target, args=(), kwargs={},  group=None, name=None, verbose=None):
      Process.__init__(self,group,target,name,args,kwargs)
      self._return = [ ]
      
    def mytarget(self,result,*args,**kwargs):
      result.append(self._target(*self._args,**self._kwargs))
      print result
    
    def run(self):
      """Override run method to save result."""
      self.mytarget(self._return,*self._args,**self._kwargs)
      print self._return
        
    def join(self):
      """Override join method to return result."""
      Process.join(self)
      return self._return
    

class MultiProcessor:
    """Class to get manage multiple processes and their return."""
    
    def __init__(self):
      self.procs = [ ]
      
    def __iter__(self):
      """To loop over processes, and do process.join()."""
      for process, endout in self.procs:
        yield ReturnProcess(process,endout)
      
    def start(self, target, args=(), kwargs={}, group=None, name=None, verbose=False):
      """Start and save process. Create a pipe to return output."""
      endout, endin = Pipe(False)
      newargs = (endin,target) + args
      process = Process(group,self.target,name,newargs,kwargs)
      process.start()
      self.procs.append((process,endout))
      
    def target(self,*args,**kwargs):
      """Return the output to a pipe."""
      args[0].send(args[1](*args[2:],**kwargs))
      

class ReturnProcess:
    """Class contain a process and its piped return value."""
    def __init__(self,process,endout):
      self.name    = process.name
      self.process = process
      self.endout  = endout
    def join(self,*args):
      """Join process, and return output."""
      self.process.join(*args) # wait for process to finish
      return self.endout.recv()


    

