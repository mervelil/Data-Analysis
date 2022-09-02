from random import uniform
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils import check_random_state, check_array
sklearn.utils.check_random_state(400)
import math
class BeesAlgo:
    def __init__(self):
        self.n = 50  # number of scout bees
        self.m = 15  # number of sites selected out of n visited sites
        self.e = 3  # elite patches
        self.nep = 12  # elite bees recruited
        self.nsp = 8  # non-elite bees recruited
        self.ngh = 0.1  # neighbourhood size
        self.maxiter = 5000  # n X, y = check_X_y(X, y)

    # step 1
    def rand_init_extended(self, number_of_coordinates, rng1, rng2):
        result = []
        for i in range(number_of_coordinates):
            result.append((uniform(rng1[0], rng1[1]), uniform(rng2[0], rng2[1])))
        return result

    def rand_init(self, rng):
        return self.rand_init_extended(self.n, rng, rng)

    def de_jong(self, arr):
        # arr[0] = x1, arr[1] = x2
        mx = 3905.93 - 100 * (arr[0] ** 2 - arr[1]) ** 2 - (1 - arr[0]) ** 2
        return mx

    # step 2
    def fitness(self, flowers):
        result = []
        for i in range(len(flowers)):
            result.append((flowers[i], self.de_jong(flowers[i])))
        return result

    # step 5
    def recruitment(self, elite_patches, non_elite_patches):
        fitness_of_recruits = []
        for patch in elite_patches:
            fitness_of_recruits.append(self.max_fitness_of_recruits(patch, self.nep))
        for patch in non_elite_patches:
            fitness_of_recruits.append(self.max_fitness_of_recruits(patch, self.nsp))
        return fitness_of_recruits

    def max_fitness_of_recruits(self, patch, number_of_recruits):
        recruits = self.rand_init_extended(number_of_recruits, [patch[0][0] - self.ngh, patch[0][0] + self.ngh],
                                           [patch[0][1] - self.ngh, patch[0][1] + self.ngh])
        recruits.append(patch[0])
        return self.maximum(recruits)

    def maximum(self, flowers):
        sites = self.fitness(flowers)
        sites = sorted(sites, reverse=True, key=lambda x: x[1])
        return sites[0]

   
    def remaining_bees(self):
        
        bees = self.rand_init_extended(self.n-self.m, [-2.048, 2.048], [-2.048, 2.048])
        return self.fitness(bees)
    def fit(self, X=None, y=None):
        self.random_state_ = check_random_state(self.random_state)
    def fit(self,X=None, y=None):
        from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
        self.random_state_ = check_random_state(self.random_state)
        X, y = check_X_y(X=None, y=None)
        
        self.classes_ = unique_labels(y)

        self.X_ = X
        self.y_ = y
        
        return self
    def predict(self, X):

        check_is_fitted(self)

        # Input validation
        X = check_array(X)

        closest = np.argmin(euclidean_distances(X, self.X_), axis=1)
        return self.y_[closest]

    def main(self):
        sites = self.rand_init([-2.048, 2.048])
        result = self.fitness(sites)
        for i in range(self.maxiter):
            # forming new population
            population_fitness = sorted(result, reverse=True, key=lambda x: x[1])
            elite = population_fitness[:self.e]
            non_elite = population_fitness[self.e:self.m]
            best_recruits = self.recruitment(elite, non_elite)
            rb = self.remaining_bees()
            result = best_recruits + rb
        population_fitness = sorted(result, reverse=True, key=lambda x: x[1])
        return population_fitness

b = BeesAlgo()
print(b.main())