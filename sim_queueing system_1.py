import heapq
import random
import math
import time
import matplotlib.pyplot as plt

loFlag = 0
sZqEFlag = 0
serForDept = 0
arrDeptCount = 0
busyCount = 0
# Parameters
class Params:
    def __init__(self, lambd, omega, k):        
        self.lambd = lambd 
        self.omega = omega
        self.k = k

# States and statistical counters        
class States:
    def __init__(self):
        
        # States
        self.queue = []        
        
        # Statistics
        self.util = 0.0         
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0


        #new
        self.serverStatus = []
        self.numberOfInTheQueue = 0
        self.numberDelayed = 0
        self.totalDelay = 0.0
        self.auQt = 0.0
        self.auBt =0.0
        self.nextInService = 0.0










    def update(self, sim, event):
        global busyCount
        if event.eventType == 'Arrival':
            for i in range(sim.params.k):
                if self.serverStatus[i] == 0:
                    self.serverStatus[i] = 1
                    self.served += 1
                    break
                elif self.serverStatus[i] == 1:
                    busyCount += 1
            if busyCount == sim.params.k:
                self.numberOfInTheQueue += 1
                self.queue.append(event.eventTime)
                self.auQt += len(self.queue)*(event.eventTime - sim.simclock)
                #busyCount = 0
            #for i in range(sim.params.k):
                #if self.serverStatus[i] == 1:
                    #busyCount += 1
            self.auBt += (busyCount/sim.params.k)*(event.eventTime - sim.simclock)
            busyCount = 0
        elif event.eventType == 'Departure':
            for i in range(sim.params.k):
                if self.serverStatus[i] == 1:
                    if self.queue:
                        self.nextInService = self.queue.pop(0)
                        self.numberOfInTheQueue -= 1
                        self.served += 1
                        self.totalDelay += event.eventTime - self.nextInService
                        global serForDept
                        serForDept = 1
                        self.auQt += len(self.queue)*(event.eventTime - sim.simclock)
                    else:
                        self.serverStatus[i] = 0
                    break
            for i in range(sim.params.k):
                if self.serverStatus[i] == 1:
                    busyCount += 1
            self.auBt += (busyCount/sim.params.k)*(event.eventTime - sim.simclock)
            busyCount = 0

    def printVariables(self):
        #print(self.queue)
        None    
    
    def finish(self, sim):
        #None
        self.avgQdelay = self.totalDelay/self.served
        self.avgQlength = self.auQt/sim.simclock
        #print(self.avgQdelay)
        #print(self.avgQlength)
        self.util = self.auBt/sim.simclock
        
    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, omega = %lf, k = %d' % (sim.params.lambd, sim.params.omega, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))
     
    def getResults(self, sim):
        return (self. avgQlength, self.avgQdelay, self.util)
   
class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        
    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')
    
    def __repr__(self):
        return self.eventType

class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim
        
    def process(self, sim):
        self.first_event_time = -(1/sim.params.lambd) * math.log(random.uniform(0,1),math.e)
        self.sim.scheduleEvent(ArrivalEvent(self.first_event_time, self.sim))
        global arrDeptCount
        arrDeptCount += 1
        #print("beginning e ",arrDeptCount)
        #None
                
class ExitEvent(Event):    
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim
    
    def process(self, sim):
        #if sim.simclock > 10:
            #print("ergrgrhtghfgtjykgyhjfgdfjjggkgfjfgjgkhkjkkkhkyrik")
            #self.sim.scheduleEvent(ExitEvent(eventTime, self.sim))
        None

                                
class ArrivalEvent(Event):
    #new
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'Arrival'
        self.sim = sim
        #new








    def process(self, sim):
        self.iaTime = -(1/sim.params.lambd) * math.log(random.uniform(0,1),math.e)
        #print(self.iaTime)
        self.naTime = self.iaTime + sim.simclock
        #print(self.naTime)
        self.sim.scheduleEvent(ArrivalEvent(self.naTime, self.sim))
        #time.sleep(1)
        #print(sim.states.queue)
        global arrDeptCount
        arrDeptCount += 1
        #print("normal arrival e ",arrDeptCount)
        if sim.states.served > 2500:
            self.sim.scheduleEvent(ExitEvent(self.naTime+0.1, self.sim))

        if not sim.states.queue:
            self.serTime = -(1/sim.params.omega) * math.log(random.uniform(0,1),math.e)
            self.nsTime = self.serTime + sim.simclock
            self.sim.scheduleEvent(DepartureEvent(self.nsTime, self.sim))
            #time.sleep(1)
            arrDeptCount -= 1
            #print("prothom departure e ",arrDeptCount)
        
class DepartureEvent(Event): 
    #new
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'Departure'
        self.sim = sim
        #new




    def process(self, sim):
        global serForDept
        if serForDept == 1:
            self.serTime = -(1/sim.params.omega) * math.log(random.uniform(0,1),math.e)
            self.nsTime = self.serTime + sim.simclock
            serForDept = 0
            self.sim.scheduleEvent(DepartureEvent(self.nsTime, self.sim))
            #time.sleep(1)
            global arrDeptCount
            arrDeptCount -= 1
            #print("notun in service e ",arrDeptCount)


class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0   
        self.seed = seed
        self.params = None
        self.states = None
        
    def initialize(self):
        self.simclock = 0        
        self.scheduleEvent(StartEvent(0, self))
        
    def configure(self, params, states):
        self.params = params
        self.states = states
        for i in range(self.params.k):
            self.states.serverStatus.append(0)
    def now(self):
        return self.simclock
        
    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))        
    
    def run(self):
        random.seed(self.seed)        
        self.initialize()
        
        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)
            
            if event.eventType == 'EXIT':
                break
            
            if self.states != None:
                self.states.update(self, event)
                
            print (event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)
            #new
            #print(self.states.queue)
     
        self.states.finish(self)   
    
    def printResults(self):
        self.states.printResults(self)
        
    def getResults(self):
        return self.states.getResults(self)
        

def experiment1():
    seed = 101    
    sim = Simulator(seed)
    sim.configure(Params(5.0/60, 8.0/60, 1), States())
    sim.run()
    sim.printResults()

def experiment2():
    seed = 110
    omega = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []
    
    for ro in ratios:
        sim = Simulator(seed)
        sim.configure(Params(omega * ro, omega, 1), States())    
        sim.run()
        
        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)
        
    plt.figure(1)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q length')    

    
    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q delay (sec)')    

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Util')    
    
    plt.show()          
    
def experiment3():
    # Similar to experiment2 but for different values of k; 1, 2, 3, 4
    # Generate the same plots
    #None
    seed = 110
    omega = 1000.0 / 60
    sim = Simulator(seed)
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for i in range(1,5,1):
        for ro in ratios:
            sim = Simulator(seed)
            sim.configure(Params(omega * ro, omega, i), States())
            sim.run()

            length, delay, utl = sim.getResults()
            avglength.append(length)
            avgdelay.append(delay)
            util.append(utl)

        plt.figure(1)
        plt.subplot(311)
        plt.plot(ratios, avglength)
        plt.xlabel('Ratio (ro)')
        plt.ylabel('Avg Q length')

        plt.subplot(312)
        plt.plot(ratios, avgdelay)
        plt.xlabel('Ratio (ro)')
        plt.ylabel('Avg Q delay (sec)')

        plt.subplot(313)
        plt.plot(ratios, util)
        plt.xlabel('Ratio (ro)')
        plt.ylabel('Util')

        plt.show()
        avglength = []
        avgdelay = []
        util = []




                            
def main():
    #experiment1()
    experiment2()
    #experiment3()        

          
if __name__ == "__main__":
    main()
                  
