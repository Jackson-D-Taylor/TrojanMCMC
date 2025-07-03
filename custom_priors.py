import numpy as np


class AuxiliaryCircularJump:
    """
    This enforces theta, phi within [0, 2pi] by sending theta to theta % (2pi) and phi to phi % (2pi),
    rather than rejecting proposals that would take theta or phi outside of [0, 2pi].
    """

    def __init__(self, pta, circular_param_names=["phi", "theta"], period=2 * np.pi):
        self.pta = pta
        self.period = period
        self.pulsar_name = pta.pulsars[0]
        self.indices = [
            self.pta.param_names.index(f"{self.pulsar_name}_troj_{p}")
            for p in circular_param_names
        ]

    def __call__(self, x, q, iter, beta):

        for index in self.indices:
            q[index] = q[index] % (self.period)

        return q, 0.0
