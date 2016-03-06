from utils import common as uc
import numpy as np
import cv2 as cv
import pickle
import os

class PersistentIsing(object):
    """ Class encapsulating this code I googled """
    def __init__(self):
        """ Constructor """
        self.SIZE = 1000
        self.T = 1.5
        self.path = 'data/ising.pickle'

    def bc(self, i):
        """ Check periodic boundary conditions  """
        if i+1 > self.SIZE-1:
            return 0
        if i-1 < 0:
            return self.SIZE-1
        else:
            return i

    def energy(self, system, N, M):
        """ Calculate internal energy """
        return -1 * system[N,M] * (system[self.bc(N-1), M] \
                                   + system[self.bc(N+1), M] \
                                   + system[N, self.bc(M-1)] \
                                   + system[N, self.bc(M+1)])

    def get_sytem(self):
        """ Or load """
        if os.path.isfile(self.path):
            # Re-read
            with open(self.path, 'r') as fin:
                system = pickle.load(fin)
        else:
            # Initialization
            system = np.random.random_integers(0,1,(self.SIZE,self.SIZE))
            system[system==0] =- 1

        return system

    def run(self):
        """ The Main monte carlo loop """
        system = self.get_sytem()

        for _ in range(21595):
            M = np.random.randint(0,self.SIZE)
            N = np.random.randint(0,self.SIZE)

            E = -2. * self.energy(system, N, M)

            if E <= 0.:
                system[N,M] *= -1
            elif np.exp(-1./self.T*E) > np.random.rand():
                system[N,M] *= -1

        step = len(uc.get_jpgs('img/ising/'))
        numname = 'img/ising/' + str(1000000 + step) + '.jpg'
        cv.imwrite(numname, 256*(1+system))

        with open(self.path, 'w') as fout:
            pickle.dump(system, fout)

if __name__ == '__main__':
    ising = PersistentIsing()
    ising.run()
