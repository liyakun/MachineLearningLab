"""
This file contains the optimization algorithms
"""
import numpy as np
import time

class Optimization:

    weights_all = []

    def __init__(self):
        pass

    # sigmoid function
    def sigmoid(self, inX):
        return 1.0/(1+np.exp(-inX))

    # gradient ascent optional optimize algorithm
    def grad_ascent(self, train_matrix, train_class_list, random_index_list_in_training, num_iteration, function):
        #  every time clean the weights_all for all training weights
        self.weights_all = []
        # get start time
        start_time = time.time()
        # get the number of rows and columns of the training matrix
        m, n = np.shape(train_matrix)
        # initialize a temporal weights vector to all 1
        weights_tmp = np.ones((n, 1))
        # iterate within the number of iteration
        for i in range(num_iteration):
            # get the index list of all the data in random_index_list_in_training
            data_index = range(len(random_index_list_in_training))
            for j in range(len(random_index_list_in_training)):
                # alpha changes on each iteration, improve oscillations
                # alpha decreases as the number of iterations increases, but it never reach 0
                alpha = 4/(1.0+j+i) + 0.001
                # randomly selecting each index from data_index, then get value from random_index_list_in_training
                # then we access the instance in train matrix to use in updating the weights, reduce periodic variations
                rand_index = int(np.random.uniform(0, len(data_index)))
                # get the sigmoid value
                h = function.sigmoid(np.sum(train_matrix[random_index_list_in_training[rand_index]]*weights_tmp))
                # compare the sigmoid value with teacher, and store the current error
                error_tmp = (train_class_list[random_index_list_in_training[rand_index]] - h)
                # store all the weights
                self.weights_all.append(np.sum(np.mat(weights_tmp)))
                # update weights in current training example
                weights_tmp += alpha * train_matrix[random_index_list_in_training[rand_index]].transpose() * error_tmp
                # remove the used instances index
                del (data_index[rand_index])
        print "\nTraining finished within %fs!\n" % (time.time() - start_time)
        return weights_tmp

    # sigmoid test function
    def sig_test(self, instance, weights):
        sig_value = self.sigmoid(np.sum(instance*weights))
        if sig_value > 0.5:
            return 1.0
        else:
            return 0.0

    # return a vector of x, which satisfies 'M*x=0'
    def solve_homogeneous(self, equations):
        assert (isinstance(equations, np.ndarray)), "ndarray required"
        # Singular Value Decomposition.
        u, s, vh = np.linalg.svd(equations)
        # the last one is the solution for the sum of multiply with points to zero, as we add all one before
        return vh.T[:, -1]

    # find the alphas to solve the equation
    def find_alphas(self, points):
        _points = np.asarray(points)

        n, m = _points.shape
        equations = np.vstack((np.ones(n), _points.T)) # add one here to prevent we got all zero as the solution
        # <editor-fold desc="Description">
        """
        numpy.vstack(tup): stack array in sequence vertically(row wise)
                Take a sequence of arrays and stack them vertically to make a single array.
                Rebuild arrays divided by vsplit
                For example: a = np.array([1, 2, 3])
                             b = np.array([2, 3, 4])
                            np.vstack((a,b)) => array([[1, 2, 3],
                                                       [2, 3, 4]])
        """
        # </editor-fold>

        return self.solve_homogeneous(equations)

    # find a radon partition
    def radon_partition(self, points):
        # <editor-fold desc="Description">
        """
         points: (n, d)-array like
                 where n is the number of points and d is the dimension of the points
         Return the radon points, the factors for the partition I and the partition J
         and two masking arrays, representing the partitions in reference to the inputarray.
            (radon point),
            (alpha_I, alpha_J),
            (mask_I, mask_J)
        """
        # </editor-fold>
        points = np.asarray(points)
        n, d = points.shape
        assert (n >= d + 2), "Not enough points"

        # get the array of alphas
        alphas = self.find_alphas(points)

        positive_idx = alphas > 0
        positive_alphas = alphas[positive_idx]
        positive_points = points[positive_idx]
        non_positive_idx = ~ positive_idx
        non_positive_alphas = alphas[non_positive_idx]

        # <editor-fold desc="Description">
        """
        The convex hull of I and J must intersect, because they both contain the
        point
                p = sum{(a_i/A)x_i}, i in I = sum{-(a_j/A)*x_j}, j in J
        where
                A = sum{a_i}, i in I, = -sum{a_j}, i in J
        """
        # </editor-fold>
        sum_alphas = np.sum(positive_alphas)
        radon_pt_positive_alphas = positive_alphas / sum_alphas
        radon_pt_non_positive_alphas = non_positive_alphas / (-sum_alphas)
        # dot product of two arrays, we get the radon point in this step, p = sum{(a_i/A)x_i}, i
        radon_pt = np.dot(radon_pt_positive_alphas, positive_points)

        return (radon_pt,
                (radon_pt_positive_alphas, radon_pt_non_positive_alphas),
                (positive_idx, non_positive_idx))

    # find  the radon point
    def radon_point(self, points):
        # <editor-fold desc="Description">
        """
         points : (n, d)-array_like where n is the number of points and d is the dimension of the points
         Return the radon point as a ndarray
        """
        # </editor-fold>
        radon_pt, _, _ = self.randon_partition(points)
        return radon_pt

    # yield n element from the list l, Throws IndexError if len(l) < n
    def pop(self, l, n):
        for i in range(n):
            yield l.pop()

    # let l be the max such that B_(l-1) has at least d+2 points
    def find_l(self, buckets, d):
        l = None
        for i, b in enumerate(buckets):
            if len(b) >= d + 2:
                l = i

        assert (l is not None), "No bucket with d+2 points found"
        return l + 1

    def prune_zipped(self, alphas, hull):
        _alphas = np.asarray(alphas)
        _hull = np.asarray(hull)
        alphas, hull, non_hull = self.prune_recursive(_alphas, _hull, [])
        assert (alphas.shape[0] == hull.shape[0]), "Broken hull"
        non_hull = [(p, [[(1,p)]]) for p in non_hull]
        return zip(alphas, hull), non_hull

    def prune_recursive(self, alphas, hull, non_hull):
        # remove all coefficients that are already (close to) zero
        idx_nonzero = ~ np.isclose(alphas, np.zeros_like(alphas))  # alphas != 0
        alphas = alphas[idx_nonzero]

        # Add pruned points to the non hull (and thus back to bucket B_0)
        non_hull = non_hull + hull[~idx_nonzero].tolist()

        hull = hull[idx_nonzero]
        n, d = hull.shape

        # Anchor: d+1 hull points can't  be reduced any further
        if n <= d + 1:
            return alphas, hull, non_hull

        # Choose d + 2 hull points
        _hull = hull[:d + 2]
        _alphas = alphas[:d + 2]

        # create linearly dependent vectors
        lindep = _hull[1:] - _hull[1]

        # solve theta * lindep = 0
        _betas = self.solve_homogenerous(lindep.T)

        # calculate theta_1 in a way to assure theta_i = 0
        beta1 = np.negative(np.sum(_betas))
        betas = np.hstack((beta1, _betas))

        # calculate the adjusted alphas and determine the minimum
        # calculate the minimum fraction alpha / theta_i for each theta_i > 0
        idx_positive = betas > 0
        idx_nonzero = ~ np.isclose(betas, np.zeros_like(betas)) # betas != 0
        idx = idx_positive & idx_nonzero
        lambdas = _alphas[idx] / betas[idx]
        lambda_min_idx = np.argmin(lambdas)

        # adjust the alpha's of the original point
        # since _alphas is a view to the original data, the alphas array will like
        # be updated automatically
        _alphas[:] = _alphas - (lambdas[lambda_min_idx] * betas)

        # remove (filter) the pruned hull vector
        idx = np.arrange(n) != lambda_min_idx
        hull = hull[idx]
        non_hull.append(hull[lambda_min_idx])
        alphas = alphas[idx]

        return self._prune_recursive(alphas, hull, non_hull)