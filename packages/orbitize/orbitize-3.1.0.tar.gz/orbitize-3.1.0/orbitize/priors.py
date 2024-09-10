import numpy as np
import abc
from astropy import units as u, constants as cst

from orbitize import basis
from orbitize.kepler import _calc_ecc_anom
import scipy.special
import scipy.stats

"""
This module defines priors with methods to draw samples and compute log(probability)
"""


class Prior(abc.ABC):
    """
    Abstract base class for prior objects.
    All prior objects should inherit from this class.

    Written: Sarah Blunt, 2018
    """

    is_correlated = False

    @abc.abstractmethod
    def draw_samples(self, num_samples):
        pass

    @abc.abstractmethod
    def compute_lnprob(self, element_array):
        pass


class NearestNDInterpPrior(Prior):
    """
    Nearest Neighbor interp. This class is
    a wrapper for scipy.interpolate.NearestNDInterpolator.

    Args:
        interp_fct (scipy.interpolate.NearestNDInterpolator): scipy Interpolator
            object containing the NDInterpolator defined by the user
        total_params (float): number of parameters

    Written: Jorge LLop-Sayson (2021)
    """

    is_correlated = True

    def __init__(self, interp_fct, total_params):
        self.interp_fct = interp_fct
        self.total_params = total_params
        self.param_num = 0
        self.correlated_drawn_samples = None
        self.correlated_input_samples = None
        self.num_priorsFromArr = interp_fct.values.size
        self.ind_draw = None

    def increment_param_num(self):
        """
        Increment the index to evaluate the appropriate parameter.
        """
        self.param_num += 1
        self.param_num = self.param_num % (self.total_params + 1)
        self.param_num = self.param_num % self.total_params

    def transform_samples(self):
        raise NotImplementedError(
            """The transform_samples() method is not implemented for this Prior
            class yet. We're working on it!
            """
        )

    def draw_samples(self, num_samples):
        """
        Draw positive samples from the ND interpolator.
        Negative samples will not be returned.

        Args:
            num_samples (float): the number of samples to generate.

        Returns:
            numpy array of float: samples drawn from the ND interpolator
            distribution. Array has length `num_samples`.
        """
        if self.param_num == 0:
            ind_draw = np.random.randint(self.num_priorsFromArr, size=num_samples)
            self.ind_draw = ind_draw
            return_me = self.interp_fct.points[self.ind_draw, self.param_num]
            self.increment_param_num()
            return return_me
        else:
            return_me = self.interp_fct.points[self.ind_draw, self.param_num]
            self.increment_param_num()
            return return_me

    def compute_lnprob(self, element_array):
        """
        Compute log(probability) of an array of numbers wrt a the defined ND
        interpolator. Negative numbers return a probability of -inf.

        Args:
            element_array (float or np.array of float): array of numbers. We want
                the probability of drawing each of these from the ND interpolator.

        Returns:
            numpy array of float: array of log(probability) values,
            corresponding to the probability of drawing each of the numbers
            in the input `element_array`.
        """
        if self.param_num == 0:
            self.correlated_input_samples = element_array
        else:
            self.correlated_input_samples = np.append(
                self.correlated_input_samples, element_array
            )
        if self.param_num == self.total_params - 1:
            lnlike = self.interp_fct(self.correlated_input_samples)
            self.increment_param_num()
            self.logparam_corr = 1
            return lnlike
        else:
            self.increment_param_num()
            return 0


class KDEPrior(Prior):
    """
    Gaussian kernel density estimation (KDE) prior. This class is
    a wrapper for scipy.stats.gaussian_kde.

    Args:
        gaussian_kde (scipy.stats.gaussian_kde): scipy KDE object containing the
            KDE defined by the user
        total_params (float): number of parameters in the KDE
        bounds (array_like, optional): bounds for the KDE out of which the prob
            returned is -Inf
        bounds (array_like of bool, optional): if True for a parameter the
            parameter is fit to the KDE in log-scale

    Written: Jorge LLop-Sayson, Sarah Blunt (2021)
    """

    is_correlated = True

    def __init__(self, gaussian_kde, total_params, bounds=[], log_scale_arr=[]):
        self.gaussian_kde = gaussian_kde
        self.total_params = total_params
        self.param_num = 0
        self.logparam_corr = 1
        if not bounds:
            self.bounds = [[-np.inf, np.inf] for i in range(total_params)]
        else:
            self.bounds = bounds
        if not log_scale_arr:
            self.log_scale_arr = [False for i in range(total_params)]
        else:
            self.log_scale_arr = log_scale_arr
        self.correlated_drawn_samples = None
        self.correlated_input_samples = None

    def __repr__(self):
        return "Gaussian KDE"

    def increment_param_num(self):
        """
        Increment the index to evaluate the appropriate parameter.
        """
        self.param_num += 1
        self.param_num = self.param_num % (self.total_params + 1)
        self.param_num = self.param_num % self.total_params

    def transform_samples(self):
        raise NotImplementedError(
            """The transform_samples() method is not implemented for this Prior
            class yet. We're working on it!
            """
        )

    def draw_samples(self, num_samples):
        """
        Draw positive samples from the KDE.
        Negative samples will not be returned.

        Args:
            num_samples (float): the number of samples to generate.

        Returns:
            numpy array of float: samples drawn from the KDE
            distribution. Array has length `num_samples`.
        """
        if self.param_num == 0:
            self.correlated_drawn_samples = self.gaussian_kde.resample(num_samples)
            self.increment_param_num()
            return self.correlated_drawn_samples[0]
        else:
            return_me = self.correlated_drawn_samples[self.param_num]
            self.increment_param_num()
            return return_me

    def compute_lnprob(self, element_array):
        """
        Compute log(probability) of an array of numbers wrt a the defined KDE.
        Negative numbers return a probability of -inf.

        Args:
            element_array (float or np.array of float): array of numbers. We want the
                probability of drawing each of these from the KDE.

        Returns:
            numpy array of float: array of log(probability) values,
            corresponding to the probability of drawing each of the numbers
            in the input `element_array`.
        """
        if (
            element_array < self.bounds[self.param_num][0]
            or element_array > self.bounds[self.param_num][1]
        ):
            if self.log_scale_arr[self.param_num]:
                element_array_lin = element_array
                element_array = np.log10(element_array)
                if np.isnan(element_array):
                    element_array = 0  # set to zero bc doesn't matter what it is since we're already returning a small prob
            if self.param_num == 0:
                self.correlated_input_samples = element_array
            else:
                self.correlated_input_samples = np.append(
                    self.correlated_input_samples, element_array
                )
            self.increment_param_num()
            self.logparam_corr = 1
            return -1e10
        if self.log_scale_arr[self.param_num]:
            element_array_lin = element_array
            element_array = np.log10(element_array)
            self.logparam_corr = self.logparam_corr * (element_array_lin)
        if self.param_num == 0:
            self.correlated_input_samples = element_array
        else:
            self.correlated_input_samples = np.append(
                self.correlated_input_samples, element_array
            )
        if self.param_num == self.total_params - 1:
            lnlike = self.gaussian_kde.logpdf(self.correlated_input_samples)
            self.increment_param_num()
            self.logparam_corr = 1
            return lnlike
        else:
            self.increment_param_num()
            return 0


class GaussianPrior(Prior):
    """Gaussian prior.

    .. math::

        log(p(x|\\sigma, \\mu)) \\propto \\frac{(x - \\mu)}{\\sigma}

    Args:
        mu (float): mean of the distribution
        sigma (float): standard deviation of the distribution
        no_negatives (bool): if True, only positive values will be drawn from
        this prior, and the probability of negative values will be 0
        (default:True).

    (written) Sarah Blunt, 2018
    """

    def __init__(self, mu, sigma, no_negatives=True):
        self.mu = mu
        self.sigma = sigma
        self.no_negatives = no_negatives

    def __repr__(self):
        return "Gaussian"

    def transform_samples(self, u):
        """
        Transform uniform 1D samples, u, to samples drawn
        from a Gaussian distribution.

        Args:
            u (array of floats): list of samples with values 0 < u < 1.

        Returns:
            numpy array of floats: 1D u samples transformed to a Gaussian
            distribution.
        """
        # a is the # of standard deviations at which 0 occurs
        a = -self.mu / self.sigma

        if self.no_negatives:
            samples = scipy.stats.truncnorm.isf(
                u, a, np.inf, loc=self.mu, scale=self.sigma
            )
        else:
            z = scipy.special.ndtri(u)
            samples = z * self.sigma + self.mu
        return samples

    def draw_samples(self, num_samples):
        """
        Draw positive samples from a Gaussian distribution.
        Negative samples will not be returned.

        Args:
            num_samples (float): the number of samples to generate

        Returns:
            numpy array of float: samples drawn from the appropriate
            Gaussian distribution. Array has length `num_samples`.
        """
        samples = np.random.uniform(0, 1, num_samples)
        samples = self.transform_samples(samples)

        return samples

    def compute_lnprob(self, element_array):
        """
        Compute log(probability) of an array of numbers wrt a Gaussian distibution.
        Negative numbers return a probability of -inf.

        Args:
            element_array (float or np.array of float): array of numbers. We want the
                probability of drawing each of these from the appopriate Gaussian
                distribution

        Returns:
            numpy array of float: array of log(probability) values,
            corresponding to the probability of drawing each of the numbers
            in the input `element_array`.
        """
        lnprob = -0.5 * ((element_array - self.mu) / self.sigma) ** 2

        if self.no_negatives:
            bad_samples = np.where(element_array < 0)[0]
            lnprob[bad_samples] = -np.inf

        return lnprob


class LogUniformPrior(Prior):
    """
    This is the probability distribution :math:`p(x) \\propto 1/x`

    The __init__ method should take in a "min" and "max" value
    of the distribution, which correspond to the domain of the prior.
    (If this is not implemented, the prior has a singularity at 0 and infinite
    integrated probability).

    Args:
        minval (float): the lower bound of this distribution
        maxval (float): the upper bound of this distribution

    """

    def __init__(self, minval, maxval):
        self.minval = minval
        self.maxval = maxval

        self.logmin = np.log(minval)
        self.logmax = np.log(maxval)

    def __repr__(self):
        return "Log Uniform"

    def transform_samples(self, u):
        """
        Transform uniform 1D samples, u, to samples drawn
        from a Log Uniform distribution.

        Args:
            u (array of floats): list of samples with values 0 < u < 1.

        Returns:
            numpy array of floats: 1D u samples transformed to a Log Uniform
            distribution.
        """
        samples = (self.logmax - self.logmin) * u + self.logmin

        # generate samples following a log uniform distribution
        samples = np.exp(samples)

        return samples

    def draw_samples(self, num_samples):
        """
        Draw samples from this 1/x distribution.

        Args:
            num_samples (float): the number of samples to generate

        Returns:
            np.array:  samples ranging from [``minval``, ``maxval``) as floats.
        """
        # sample from a uniform distribution in log space
        samples = np.random.uniform(0, 1, num_samples)

        # convert from log space to linear space
        samples = self.transform_samples(samples)

        return samples

    def compute_lnprob(self, element_array):
        """
        Compute the prior probability of each element given that its drawn from a Log-Uniofrm  prior

        Args:
            element_array (float or np.array of float): array of paramters to compute the prior probability of

        Returns:
            np.array: array of prior probabilities
        """
        normalizer = self.logmax - self.logmin

        lnprob = -np.log((element_array * normalizer))

        # account for scalar inputs
        if np.shape(lnprob) == ():
            if (element_array > self.maxval) or (element_array < self.minval):
                lnprob = -np.inf
        else:
            lnprob[(element_array > self.maxval) | (element_array < self.minval)] = (
                -np.inf
            )

        return lnprob


class UniformPrior(Prior):
    """
    This is the probability distribution p(x) propto constant.

    Args:
        minval (float): the lower bound of the uniform prior
        maxval (float): the upper bound of the uniform prior

    """

    def __init__(self, minval, maxval):
        self.minval = minval
        self.maxval = maxval

    def __repr__(self):
        return "Uniform"

    def transform_samples(self, u):
        """
        Transform uniform 1D samples, u, to samples drawn
        from a uniform distribution.

        Args:
            u (array of floats): list of samples with values 0 < u < 1.

        Returns:
            numpy array of floats: 1D u samples transformed to a uniform
            distribution.
        """
        # generate samples following a uniform distribution
        samples = (self.maxval - self.minval) * u + self.minval

        return samples

    def draw_samples(self, num_samples):
        """
        Draw samples from this uniform distribution.

        Args:
            num_samples (float): the number of samples to generate

        Returns:
            np.array:  samples ranging from [0, pi) as floats.
        """
        # sample from a uniform distribution in log space
        samples = np.random.uniform(0, 1, num_samples)
        samples = self.transform_samples(samples)

        return samples

    def compute_lnprob(self, element_array):
        """
        Compute the prior probability of each element given that its drawn from this uniform prior

        Args:
            element_array (float or np.array of float): array of paramters to compute the prior probability of

        Returns:
            np.array: array of prior probabilities
        """
        lnprob = np.log(np.ones(np.size(element_array)) / (self.maxval - self.minval))

        # account for scalar inputs
        if np.shape(lnprob) == ():
            if (element_array > self.maxval) or (element_array < self.minval):
                lnprob = -np.inf
        else:
            lnprob[(element_array > self.maxval) | (element_array < self.minval)] = (
                -np.inf
            )

        return lnprob


class SinPrior(Prior):
    """
    This is the probability distribution :math:`p(x) \\propto sin(x)`

    The domain of this prior is [0,pi].
    """

    def __init__(self):
        pass

    def __repr__(self):
        return "Sine"

    def transform_samples(self, u):
        """
        Transform uniform 1D samples, u, to samples drawn
        from a Sine distribution.

        Args:
            u (array of floats): list of samples with values 0 < u < 1.

        Returns:
            numpy array of floats: 1D u samples transformed to a Sine
            distribution.
        """
        # generate samples following a sin distribution
        samples = np.arccos(1 - 2 * u)

        return samples

    def draw_samples(self, num_samples):
        """
        Draw samples from a Sine distribution.

        Args:
            num_samples (float): the number of samples to generate

        Returns:
            np.array:  samples ranging from [0, pi) as floats.
        """

        # draw uniform from -1 to 1
        samples = np.random.uniform(0, 1, num_samples)

        samples = self.transform_samples(samples)

        return samples

    def compute_lnprob(self, element_array):
        """
        Compute the prior probability of each element given that its drawn from a sine prior

        Args:
            element_array (float or np.array of float): array of paramters to compute the prior probability of

        Returns:
            np.array: array of prior probabilities
        """
        normalization = 2.0

        lnprob = np.log(np.sin(element_array) / normalization)

        # account for scalar inputs
        if np.shape(lnprob) == ():
            if (element_array >= np.pi) or (element_array <= 0):
                lnprob = -np.inf
        else:
            lnprob[(element_array >= np.pi) | (element_array <= 0)] = -np.inf

        return lnprob


class LinearPrior(Prior):
    """
    Draw samples from the probability distribution:

    .. math::

        p(x) \\propto mx+b

    where m is negative, b is positive, and the
    range is [0,-b/m].

    Args:
        m (float): slope of line. Must be negative.
        b (float): y intercept of line. Must be positive.

    """

    def __init__(self, m, b):
        self.m = m
        self.b = b

    def __repr__(self):
        return "Linear"

    def transform_samples(self, u):
        """
        Transform uniform 1D samples, u, to samples drawn
        from a Linear distribution.

        Args:
            u (array of floats): list of samples with values 0 < u < 1.

        Returns:
            numpy array of floats: 1D u samples transformed to a Linear
            distribution.
        """
        norm = -0.5 * self.b**2 / self.m

        # generate samples following a linear distribution
        linear_samples = -np.sqrt(2.0 * norm * u / self.m + (self.b / self.m) ** 2) - (
            self.b / self.m
        )

        return linear_samples

    def draw_samples(self, num_samples):
        """
        Draw samples from a descending linear distribution.

        Args:
            num_samples (float): the number of samples to generate

        Returns:
            np.array:  samples ranging from [0, -b/m) as floats.
        """

        # draw uniform from 0 to 1
        samples = np.random.uniform(0, 1, num_samples)

        # generate samples following a linear distribution
        linear_samples = self.transform_samples(samples)

        return linear_samples

    def compute_lnprob(self, element_array):
        x_intercept = -self.b / self.m
        normalizer = -0.5 * self.b**2 / self.m

        lnprob = np.log((self.m * element_array + self.b) / normalizer)

        # account for scalar inputs
        if np.shape(lnprob) == ():
            if (element_array >= x_intercept) or (element_array < 0):
                lnprob = -np.inf
        else:
            lnprob[(element_array >= x_intercept) | (element_array < 0)] = -np.inf

        return lnprob


class ObsPrior(Prior):
    """
    Implements the observation-based priors described in O'Neil+ 2018
    (https://ui.adsabs.harvard.edu/abs/2019AJ....158....4O/abstract)

    Args:
        epochs (np.array of float): array of epochs at which observations are taken [mjd]
        ra_err (np.array of float): RA errors of observations [mas]
        dec_err (np.array of float): decl errors of observations [mas]
        mtot (float): total mass of system [Msol]
        period_lims (2-tuple of float): optional lower and upper prior limits
            for the orbital period [yr]
        tp_lims (2-tuple of float): optional lower and upper prior limits
            for the time of periastron passage [mjd]
        tau_ref_epoch (float): epoch [mjd] tau is defined relative to.

    Note:
        This implementation is designed to be mathematically identical to
        the implementation in O'Neil+ 2018. There are several limitations of our
        implementation, in particular:

            1. `ObsPrior` only works with MCMC (not OFTI)
            2. `ObsPrior` only works with relative astrometry (i.e. you can't use RVs or other data types)
            3. `ObsPrior` only works when the input astrometry is given in RA/decl. format (i.e. not sep/PA)
            4. `ObsPrior` assumes total mass (`mtot`) and parallax (`plx`) are fixed.
            5. `ObsPrior` only works for systems with one secondary object (no multi-planet systems)
            6. You must use `ObsPrior` with the `orbitize.basis.ObsPriors` orbital basis.

        None of these are inherent limitations of the observation-based technique,
        so let us know if you have a science case that would benefit from
        implementing one or more of these things!
    """

    is_correlated = True

    def __init__(
        self,
        epochs,
        ra_err,
        dec_err,
        mtot,
        period_lims=(0, np.inf),
        tp_lims=(-np.inf, np.inf),
        tau_ref_epoch=58849,
    ):
        self.epochs = epochs
        self.tau_ref_epoch = tau_ref_epoch
        self.mtot = mtot
        self.ra_err = ra_err
        self.dec_err = dec_err
        self.period_lims = period_lims
        self.tp_lims = tp_lims

        self.total_params = 3
        self.param_num = 0

        self.correlated_input_samples = None

    def __repr__(self):
        return "ObsPrior"

    def increment_param_num(self):
        self.param_num += 1
        self.param_num = self.param_num % (self.total_params + 1)
        self.param_num = self.param_num % self.total_params

    def draw_uniform_samples(self, num_samples):
        if self.param_num == 0:
            sample_pers = np.random.uniform(
                self.period_lims[0], self.period_lims[1], num_samples
            )
            return sample_pers
        elif self.param_num == 1:
            sample_eccs = np.random.uniform(0, 1, num_samples)
            return sample_eccs
        else:
            sample_tps = np.random.uniform(
                self.tp_lims[0], self.tp_lims[1], num_samples
            )
            return sample_tps

    def draw_samples(self, num_samples):
        """
        Draws `num_samples` samples from uniform distributions in log(per), ecc, and
        tp. This is used for initializing the MCMC walkers.

        Warning:
            The behavior of orbitize.priors.ObsPrior.draw_samples() is different
            from the draw_samples() methods of other Prior objects, which draws
            random samples from the prior itself.
        """

        samples = self.draw_uniform_samples(num_samples)
        self.increment_param_num()
        return samples

    def compute_lnprob(self, element_array):

        if self.param_num == 0:
            self.correlated_input_samples = element_array

        else:
            self.correlated_input_samples = np.append(
                self.correlated_input_samples, element_array
            )

        if self.param_num == (self.total_params - 1):

            period = self.correlated_input_samples[0]
            ecc = self.correlated_input_samples[1]
            tp = self.correlated_input_samples[2]

            if (
                (period < self.period_lims[0])
                or (period > self.period_lims[1])
                or (ecc < 0)
                or (ecc > 1)
                or (tp < self.tp_lims[0])
                or (tp > self.tp_lims[1])
            ):

                self.increment_param_num()
                return -np.inf

            jac_prefactor = -(
                ((cst.G * self.mtot * u.Msun) ** 2 * period / (2 * np.pi**4)) ** (1 / 3)
            ).value

            sma = ((period) ** 2 * self.mtot) ** (1 / 3)

            tau = basis.tp_to_tau(tp, self.tau_ref_epoch, period)

            meananom = basis.tau_to_manom(
                self.epochs, sma, self.mtot, tau, self.tau_ref_epoch
            )
            eccanom = _calc_ecc_anom(meananom, ecc)

            # sum Jacobian over all epochs (O'Neil 2019 eq 33)
            jacobian = np.sum(
                (1 / (self.ra_err * self.dec_err))
                * np.abs(
                    2 * (ecc**2 - 2) * np.sin(eccanom)
                    + ecc * (3 * meananom + np.sin(2 * eccanom))
                    + 3 * meananom * np.cos(eccanom)
                )
                / (6 * np.sqrt(1 - ecc**2))
            )

            jacobian *= np.abs(jac_prefactor)
            lnprob = -2 * np.log(jacobian)

            self.increment_param_num()
            return lnprob

        else:

            self.increment_param_num()
            return 0


def all_lnpriors(params, priors):
    """
    Calculates log(prior probability) of a set of parameters and a list of priors

    Args:
        params (np.array): size of N parameters
        priors (list): list of N prior objects corresponding to each parameter

    Returns:
        float: prior probability of this set of parameters
    """
    logp = 0.0

    for param, prior in zip(params, priors):
        param = np.array([param])

        logp += prior.compute_lnprob(param)  # return a float

    return logp


if __name__ == "__main__":
    # myPrior = LinearPrior(-1.0, 1.0)
    # mySamples = myPrior.draw_samples(1000)
    # print(mySamples)
    # myProbs = myPrior.compute_lnprob(mySamples)
    # print(myProbs)

    # myPrior = GaussianPrior(1.3, 0.2)
    # mySamples = myPrior.draw_samples(1)
    # print(mySamples)

    # myProbs = myPrior.compute_lnprob(mySamples)
    # print(myProbs)

    myPrior = GaussianPrior(-10, 0.5, no_negatives=True)
    u = np.random.uniform(0, 1, int(1e4))
    samps = myPrior.transform_samples(u)
    print(samps.min(), samps.max())

    import matplotlib.pyplot as plt

    plt.hist(samps, bins=50)
    plt.show()
