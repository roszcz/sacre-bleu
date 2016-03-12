from utils import common as uc
import numpy as np
import cv2 as cv
import pickle
import os

class PersistentIsing(object):
    """ Class encapsulating this code I googled """
    def __init__(self):
        """ Constructor """
        self.size_y = 72 * 3
        self.size_x = 128 * 3
        self.T = 1.1
        self.path = 'data/ising.pickle'

    def energy(self, system, N, M):
        """ Calculate internal energy """
        next_N = N % self.size_y
        next_M = M % self.size_x
        return -1 * system[N,M] * (system[N-1, M] \
                                   + system[next_N, M] \
                                   + system[N, M-1] \
                                   + system[N, next_M])

    def get_sytem(self):
        """ Or load """
        if os.path.isfile(self.path):
            # Re-read
            with open(self.path, 'r') as fin:
                system = pickle.load(fin)
        else:
            # Initialization
            sizeyx = (self.size_y, self.size_x)
            system = np.random.random_integers(0, 1, sizeyx)
            system[system==0] =- 1

        return system

    def run(self):
        """ The Main monte carlo loop """
        system = self.get_sytem()

        for _ in range(1000):
            M = np.random.randint(0, self.size_x)
            N = np.random.randint(0, self.size_y)

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
