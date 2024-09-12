import math

class MarkovChainKullbackLeibler:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainKullbackLeibler class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def compute(self, matrix, tolerance=1e-10, max_iterations=1000):
        """
        Compute the stationary distribution of a Markov chain from its transition matrix.
        
        Parameters:
        matrix (list of list of float): Transition matrix of the Markov chain.
        tolerance (float): Tolerance level for convergence.
        max_iterations (int): Maximum number of iterations for convergence.
        
        Returns:
        list of float: The stationary distribution of the Markov chain.
        """
        dist = [1.0 / self.num_states] * self.num_states
        for _ in range(max_iterations):
            next_dist = [0] * self.num_states
            for i in range(self.num_states):
                for j in range(self.num_states):
                    next_dist[i] += dist[j] * matrix[j][i]
            if all(abs(next_dist[i] - dist[i]) < tolerance for i in range(self.num_states)):
                break
            dist = next_dist
        return dist

    def kl_divergence(self, p, q):
        """
        Compute the Kullback-Leibler (KL) divergence between two probability distributions.
        
        Parameters:
        p (list of float): First probability distribution.
        q (list of float): Second probability distribution.
        
        Returns:
        float: KL divergence D_KL(p || q).
        """
        kl_div = 0.0
        for i in range(len(p)):
            if p[i] > 0 and q[i] > 0:
                kl_div += p[i] * math.log(p[i] / q[i])
        return kl_div

    def kullback_leibler_distance(self):
        """
        Compute the Kullback-Leibler distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Kullback-Leibler distance between the stationary distributions.
        """
        # Compute stationary distributions of P and Q
        pi_P = self.stationary_distribution(self.P)
        pi_Q = self.stationary_distribution(self.Q)
        
        # Compute the Kullback-Leibler divergence between the two stationary distributions
        return self.kl_divergence(pi_P, pi_Q)




class MarkovChainWasserstein:
    def __init__(self, P, Q, cost_matrix):
        """
        Initialize the MarkovChainWassersteinDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        cost_matrix (list of list of float): Cost matrix (n x n) representing the "distance" between states.
        """
        self.P = P
        self.Q = Q
        self.cost_matrix = cost_matrix
        self.num_states = len(P)

    def stationary_distribution(self, matrix, tolerance=1e-10, max_iterations=1000):
        """
        Compute the stationary distribution of a Markov chain from its transition matrix.
        
        Parameters:
        matrix (list of list of float): Transition matrix of the Markov chain.
        tolerance (float): Tolerance level for convergence.
        max_iterations (int): Maximum number of iterations for convergence.
        
        Returns:
        list of float: The stationary distribution of the Markov chain.
        """
        dist = [1.0 / self.num_states] * self.num_states
        for _ in range(max_iterations):
            next_dist = [0] * self.num_states
            for i in range(self.num_states):
                for j in range(self.num_states):
                    next_dist[i] += dist[j] * matrix[j][i]
            if all(abs(next_dist[i] - dist[i]) < tolerance for i in range(self.num_states)):
                break
            dist = next_dist
        return dist

    def compute(self):
        """
        Compute the Wasserstein distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Wasserstein distance between the stationary distributions.
        """
        # Compute stationary distributions of P and Q
        pi_P = self.stationary_distribution(self.P)
        pi_Q = self.stationary_distribution(self.Q)
        
        # Compute Wasserstein distance using a greedy algorithm
        distance = self._compute_wasserstein_greedy(pi_P, pi_Q)
        return distance

    def _compute_wasserstein_greedy(self, pi_P, pi_Q):
        """
        A greedy algorithm to compute an approximation of the Wasserstein distance between two distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Approximate Wasserstein distance between the two distributions.
        """
        n = self.num_states
        flow = [[0] * n for _ in range(n)]  # Flow matrix (transport plan)
        pi_P_copy = pi_P[:]
        pi_Q_copy = pi_Q[:]
        total_cost = 0.0

        for i in range(n):
            for j in range(n):
                # Flow is the minimum of remaining mass in pi_P and pi_Q
                flow_amount = min(pi_P_copy[i], pi_Q_copy[j])
                flow[i][j] = flow_amount
                total_cost += flow_amount * self.cost_matrix[i][j]
                
                # Update remaining mass in pi_P and pi_Q
                pi_P_copy[i] -= flow_amount
                pi_Q_copy[j] -= flow_amount
        
        return total_cost



#TVD
class MarkovChainTotalVariation:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainTotalVariationDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def stationary_distribution(self, matrix, tolerance=1e-10, max_iterations=1000):
        """
        Compute the stationary distribution of a Markov chain from its transition matrix.
        
        Parameters:
        matrix (list of list of float): Transition matrix of the Markov chain.
        tolerance (float): Tolerance level for convergence.
        max_iterations (int): Maximum number of iterations for convergence.
        
        Returns:
        list of float: The stationary distribution of the Markov chain.
        """
        dist = [1.0 / self.num_states] * self.num_states  # Initial guess: uniform distribution
        for _ in range(max_iterations):
            next_dist = [0] * self.num_states
            for i in range(self.num_states):
                for j in range(self.num_states):
                    next_dist[i] += dist[j] * matrix[j][i]
            if all(abs(next_dist[i] - dist[i]) < tolerance for i in range(self.num_states)):
                break
            dist = next_dist
        return dist

    def total_variation_distance(self, pi_P, pi_Q):
        """
        Compute the total variation distance between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Total variation distance between the two distributions.
        """
        total_variation = 0.0
        for i in range(len(pi_P)):
            total_variation += abs(pi_P[i] - pi_Q[i])
        return total_variation / 2

    def compute(self):
        """
        Compute the total variation distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Total variation distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = self.stationary_distribution(self.P)
        pi_Q = self.stationary_distribution(self.Q)

        # Compute the total variation distance between the two stationary distributions
        return self.total_variation_distance(pi_P, pi_Q)



class MarkovChainHellinger:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainHellingerDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def hellinger_distance(self, pi_P, pi_Q):
        """
        Compute the Hellinger distance between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Hellinger distance between the two distributions.
        """
        sum_squares = 0.0
        for i in range(len(pi_P)):
            sqrt_diff = math.sqrt(pi_P[i]) - math.sqrt(pi_Q[i])
            sum_squares += sqrt_diff ** 2
        return sum_squares**0.5 / 2**0.5

    def compute(self):
        """
        Compute the Hellinger distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Hellinger distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = self.stationary_distribution(self.P)
        pi_Q = self.stationary_distribution(self.Q)

        # Compute the Hellinger distance between the two stationary distributions
        return self.hellinger_distance(pi_P, pi_Q)


class MarkovChainJensenShannon:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainJensenShannonDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def kl_divergence(self, p, q):
        """
        Compute the Kullback-Leibler (KL) divergence between two probability distributions.
        
        Parameters:
        p (list of float): First probability distribution.
        q (list of float): Second probability distribution.
        
        Returns:
        float: KL divergence D_KL(p || q).
        """
        kl_div = 0.0
        for i in range(len(p)):
            if p[i] > 0 and q[i] > 0:  # KL divergence is only defined when p[i] and q[i] are positive
                kl_div += p[i] * math.log(p[i] / q[i])
        return kl_div

    def jensen_shannon_divergence(self, pi_P, pi_Q):
        """
        Compute the Jensen-Shannon divergence between two stationary distributions.
        
        Parameters:
        pi_P (list of float): Stationary distribution of the first Markov chain.
        pi_Q (list of float): Stationary distribution of the second Markov chain.
        
        Returns:
        float: Jensen-Shannon divergence between the two distributions.
        """
        # Compute M = (P + Q) / 2
        M = [(pi_P[i] + pi_Q[i]) / 2 for i in range(len(pi_P))]

        # Compute the Jensen-Shannon divergence
        js_div = (self.kl_divergence(pi_P, M) + self.kl_divergence(pi_Q, M)) / 2
        return js_div

    def compute(self):
        """
        Compute the Jensen-Shannon distance between the stationary distributions of two Markov chains.
        
        Returns:
        float: Jensen-Shannon distance between the stationary distributions of the two Markov chains.
        """
        # Compute stationary distributions of P and Q
        pi_P = self.stationary_distribution(self.P)
        pi_Q = self.stationary_distribution(self.Q)

        # Compute the Jensen-Shannon divergence
        js_divergence = self.jensen_shannon_divergence(pi_P, pi_Q)

        # Return the square root of the Jensen-Shannon divergence (Jensen-Shannon distance)
        return js_divergence**0.5



class MarkovChainFrobenius:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainFrobeniusDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def compute(self):
        """
        Compute the Frobenius distance between the transition matrices of two Markov chains.
        
        Returns:
        float: Frobenius distance between the two transition matrices.
        """
        sum_of_squares = 0.0
        for i in range(self.num_states):
            for j in range(self.num_states):
                diff = self.P[i][j] - self.Q[i][j]
                sum_of_squares += diff ** 2
        return sum_of_squares**0.5



class MarkovChainSpectral:
    def __init__(self, P, Q):
        """
        Initialize the MarkovChainSpectralDistance class with transition matrices of two Markov chains.
        
        Parameters:
        P (list of list of float): Transition matrix of the first Markov chain (n x n).
        Q (list of list of float): Transition matrix of the second Markov chain (n x n).
        """
        self.P = P
        self.Q = Q
        self.num_states = len(P)

    def compute(self):
        """
        Compute the spectral distance between the transition matrices of two Markov chains.
        
        Returns:
        float: Spectral distance between the two transition matrices.
        """
        # Compute eigenvalues of matrices P and Q
        if self.num_states == 2:
            eigenvalues_P = self.eigenvalues_2x2(self.P)
            eigenvalues_Q = self.eigenvalues_2x2(self.Q)
            
            # Calculate the spectral distance
            distance = 0.0
            for lambda_P, lambda_Q in zip(eigenvalues_P, eigenvalues_Q):
                distance += abs(lambda_P - lambda_Q) ** 2
            return distance**00.5
        else:
            raise NotImplementedError("Spectral distance calculation for matrices larger than 2x2 is not implemented.")


