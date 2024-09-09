import random
 
def getAdditiveShares(secret, N, fieldSize):
    shares = [random.randrange(fieldSize) for i in range(N-1)]
    shares.append((secret - sum(shares)) % fieldSize )
    return shares
 
def reconstructSecret(shares, fieldSize):
    return sum(shares) % fieldSize


class SMPC:
    def __init__(self) -> None:
        self.BASE = 10
        self.PRECISION_INTEGRAL = 8
        self.PRECISION_FRACTIONAL = 8
        self.fieldSize = 293973345475167247070445277780365744413

        self.PRECISION = self.PRECISION_INTEGRAL + self.PRECISION_FRACTIONAL
        assert(self.fieldSize > self.BASE**self.PRECISION)

    def encode(self, rational):
        upscaled = int(rational * self.BASE**self.PRECISION_FRACTIONAL)
        field_element = upscaled % self.fieldSize
        return field_element
    
    def decode(self, field_element):
        upscaled = field_element if field_element <= self.fieldSize/2 else field_element - self.fieldSize
        rational = upscaled / self.BASE**self.PRECISION_FRACTIONAL
        return rational
    
    def get_secret_shares(self, m, N):
        N = N + 1
        shares = getAdditiveShares(self.encode(m), N, self.fieldSize)
        return shares
    
    def addition(self, shares_list):
        aggregate_shares = [sum(x) % self.fieldSize for x in shares_list]
        return self.decode(reconstructSecret(aggregate_shares, self.fieldSize))

    def multiplication(self):
        pass

    def difference(self, shares_a, shares_b):
        difference_shares = [(a - b) % self.fieldSize for a, b in zip(shares_a, shares_b)]
        return self.decode(reconstructSecret(difference_shares, self.fieldSize))
    
    def compare(self, shares_a, shares_b):
        difference_shares = [(a - b) % self.fieldSize for a, b in zip(shares_a, shares_b)]
        reconstructed_difference = self.decode(reconstructSecret(difference_shares, self.fieldSize))
    
        if reconstructed_difference == 0:
            comparison_result = "a is equal to b"
        elif reconstructed_difference > 0:
            comparison_result = "a is greater than b"
        else:
            comparison_result = "a is less than b"

        return comparison_result