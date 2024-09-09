import numpy as np

def laplace_mechanism(true_value, sensitivity, epsilon):
    """Applies the Laplace mechanism for GDP."""
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale, 1)
    return true_value + noise[0]


class GDP:
    @staticmethod
    def add_noise(query_result, sensitivity, epsilon):
        return laplace_mechanism(query_result, sensitivity, epsilon)


