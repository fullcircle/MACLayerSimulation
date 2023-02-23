import simpy
import random

class Station:
    def __init__(self, env, id, ap, cwmin=16, cwmax=1024):
        self.env = env
        self.id = id
        self.ap = ap
        self.cwmin = cwmin
        self.cwmax = cwmax
        self.backoff = 0

    def transmit(self):
        print(f"Station {self.id} is trying to transmit")
        if self.ap.busy:
            print(f"AP is busy, station {self.id} has to defer")
            yield self.env.timeout(random.randint(self.cwmin, self.cwmax) * self.backoff)
            self.backoff += 1
            yield self.transmit()
        else:
            self.ap.busy = True
            print(f"Station {self.id} is transmitting")
            yield self.env.timeout(1)
            self.ap.busy = False
            self.backoff = 0
            print(f"Station {self.id} is done transmitting")

class AccessPoint:
    def __init__(self, env):
        self.env = env
        self.busy = False

    def receive(self):
        while True:
            yield self.env.timeout(0.01)
            if self.busy:
                print("AP is receiving")

def simulate(env):
    ap = AccessPoint(env)
    stations = [Station(env, i, ap) for i in range(10)]
    env.process(ap.receive())
    for station in stations:
        yield env.process(station.transmit())

env = simpy.Environment()
env.process(simulate(env))
env.run(until=100)


"""In this code, the Station class represents a wireless station that can transmit and receive data. The AccessPoint class represents the wireless access point that receives data from stations. The simulate function sets up the simulation environment by creating the access point and multiple stations.

The transmit method of the Station class simulates the behavior of the 802.11 protocol by implementing the backoff algorithm. If the access point is busy receiving data from another station, the transmitting station must wait for a random amount of time before attempting to transmit again. The AccessPoint class simply receives data from stations and sets its busy attribute to indicate whether it is currently receiving data.

When the simulation is run, each station attempts to transmit data to the access point. If the access point is busy, the station defers transmission and waits for a random amount of time before attempting to transmit again. Once a station successfully transmits data, it is marked as done and can attempt to transmit again."""