"""

Implementation of the nsF5 steganography method as described in

J. Fridrich, T. Pevny, and J. Kodovsky.
"Statistically undetectable JPEG steganography: Dead ends, challenges, and opportunities"
Multimedia & Security, 2007
http://dde.binghamton.edu/kodovsky/pdf/Fri07-ACM.pdf

Author: Benedikt Lorch, Martin Benes
Affiliation: University of Innsbruck
"""

import numpy as np

from .. import tools


def probability(
    cover_dct_coeffs: np.ndarray,
    alpha: float = 1.,
) -> np.ndarray:
    """Returns nsF5 probability map for consequent simulation.

    :param cover_dct_coeffs: quantized cover DCT coefficients
        of shape [num_vertical_blocks, num_horizontal_blocks, 8, 8]
    :type cover_dct_coeffs: `np.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`__
    :param alpha:
    :type alpha: float
    :return:
    :rtype: `np.ndarray <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>`__

    :Example:

    >>> # TODO
    """

    assert len(cover_dct_coeffs.shape) == 4, "Expected DCT coefficients to have 4 dimensions"
    assert cover_dct_coeffs.shape[2] == cover_dct_coeffs.shape[3] == 8, "Expected blocks of size 8x8"

    # No embedding
    if np.isclose(alpha, 0):
        return np.zeros_like(cover_dct_coeffs)

    # Compute change rate on bound
    beta = tools.inv_entropy(alpha)

    # Number of nonzero AC DCT coefficients
    nzAC = tools.dct.nzAC(cover_dct_coeffs)
    if nzAC == 0:
        raise ValueError('There are no non-zero AC coefficients for embedding')

    # probability map
    p = np.ones(cover_dct_coeffs.shape, dtype='float64') * beta

    # do not change zeros or DC mode
    p[cover_dct_coeffs == 0] = 0
    p[:, :, 0, 0] = 0

    # substract absolute value
    p_p1, p_m1 = p.copy(), p.copy()
    p_p1[cover_dct_coeffs > 0] = 0
    p_m1[cover_dct_coeffs < 0] = 0

    return p_p1, p_m1
