'''
Main module.
Implementation of OASIS statistical test(https://www.pnas.org/doi/10.1073/pnas.2304671121)
Tavor Z. Baharav, David Tse, and Julia Salzman

OASIS (Optimized Adaptive Statistic for Inferring Structure) utilizes a linear test-statistic, enabling the computation of closed form P-value bounds, exact asymptotic ones, and interpretable rejection of the null. It is implemented and used in SPLASH: https://github.com/refresh-bio/SPLASH.

The key method in this file is OASIS_pvalue, which returns the p-value of the OASIS test on a given contingency table. The method can be used to compute the p-value using either the asymptotic or finite sample p-value (asymptotic flag), and can return the optimizing row and column embeddings (return_f_c flag).

Please reach out on github with any questions, or directly to tavorb@mit.edu.
'''

import numpy as np # type: ignore
import scipy.stats # type: ignore


# 1: utility functions
def splitCountsColwise(mat, downSampleFrac=.5):
    """Downsamples a matrix columnwise, to ensure that each column is equally well represented in the train / test downsampled matrices.

    Args:
        mat (numpy.ndarray): The input matrix, IxJ.
        downSampleFrac (float, optional): The fraction of counts to retain per column. Default is 0.5.

    Returns:
        out_mat (numpy.ndarray): The downsampled matrix, IxJ.
    """
    
    ####### Helper function to split counts in a vector
    def splitCounts(mat, downSampleFrac=.5):
        """Downsamples a matrix. Very slight modification of https://stackoverflow.com/questions/11818215/subsample-a-matrix-python.
        This downsamples uniformly at random.

        Args:
            mat (numpy.ndarray): The input counts matrix to be downsampled. Must be integer-valued.
            downSampleFrac (float, optional): The fraction of counts to retain. Default is 0.5.

        Returns:
            out_mat (numpy.ndarray): The downsampled matrix.
        """
        keys, counts = zip(*[
            ((i, j), mat[i, j])
            for i in range(mat.shape[0])
            for j in range(mat.shape[1])
            if mat[i, j] > 0
        ])
        # Make the cumulative counts array
        counts = np.array(counts, dtype=np.int64)
        sum_counts = np.cumsum(counts)

        # Decide how many counts to include in the sample
        frac_select = downSampleFrac
        count_select = int(sum_counts[-1] * frac_select)

        # Choose unique counts
        ind_select = sorted(np.random.choice(
            range(sum_counts[-1]), count_select, replace=False))

        # A vector to hold the new counts
        out_counts = np.zeros(counts.shape, dtype=np.int64)

        # Perform basically the merge step of merge-sort, finding where
        # the counts land in the cumulative array
        i = 0
        j = 0
        while i < len(sum_counts) and j < len(ind_select):
            if ind_select[j] < sum_counts[i]:
                j += 1
                out_counts[i] += 1
            else:
                i += 1

        # Rebuild the matrix using the `keys` list from before
        out_mat = np.zeros(mat.shape, dtype=np.int64)
        for i in range(len(out_counts)):
            out_mat[keys[i]] = out_counts[i]

        return out_mat
    
    out_mat = np.zeros_like(mat)
    for j in range(mat.shape[1]):
        if mat[:, j].sum() > 0:
            out_mat[:, j] = splitCounts(np.reshape(
                mat[:, j], (mat.shape[0], -1)), downSampleFrac).flatten()

    return out_mat




# 2: c,f generation (row and column embeddings for contingency table)
def generate_cf_finite_optimized(X, randSeed=0, numRandInits=10):
    """Generates optimized column and row embeddings for the finite sample p-value.
    Tries multiple random initializations and returns the embeddings that maximize the finite sample p-value on the given X.

    Args:
        X (numpy.ndarray): The input count matrix, IxJ.
        randSeed (int, optional): The random seed for reproducibility. Default is 0.
        numRandInits (int, optional): The number of random initializations to try. Default is 10.

    Returns:
        tuple: A tuple containing the column embedding vector (c) and the row embedding vector (f).
            - c (numpy.ndarray): The column embedding vector, J-dimensional.
            - f (numpy.ndarray): The row embedding vector, I-dimensional.
    """
    np.random.seed(randSeed)  # random initialization and extension

    relevantTargs = X.sum(axis=1) > 0
    relevantSamples = X.sum(axis=0) > 0

    nrows, ncols = X.shape

    if relevantTargs.sum() < 2 or relevantSamples.sum() < 2:
        return np.zeros(ncols), np.zeros(nrows)

    X = X[np.ix_(relevantTargs, relevantSamples)]
    
    # starting at c, run alternating maximization
    def altMaximize(X, c):
        # if clustering put all in same cluster, perturb
        if np.all(c == c[0]):
            c[0] = -1*c[0]

        nj = X.sum(axis=0)
        njinvSqrt = 1.0/np.maximum(1, np.sqrt(nj))  # avoid divide by 0 errors
        njinvSqrt[nj == 0] = 0

        Xtild = (X - 1.0/X.sum()*np.outer(X @
                np.ones(X.shape[1]), X.T@np.ones(X.shape[0]))) @ np.diag(njinvSqrt)

        Sold = 0
        i = 0
        while True:
            # find optimal f for fixed c
            f = np.sign(Xtild @ c)
            f1 = (f+1)/2  # to rescale f to be [0,1] valued
            f2 = (1-f)/2
            f = f1
            if np.abs(f2@Xtild@c) > np.abs(f1@Xtild@c):
                f = f2

            # find optimal c for fixed f
            c = Xtild.T @ f
            if np.linalg.norm(c) > 0:
                c /= np.linalg.norm(c)

            # compute objective value, if fixed, stop
            S = f @ Xtild @ c
            if S == Sold:  # will terminate once fOpt is fixed over 2 iterations
                break
            Sold = S
            i += 1
            if i > 50:
                c = np.zeros_like(c)
                f = np.zeros_like(f)
                S = 0
                break
        return c, f, np.abs(S)

    Sbase = 0
    fMax = 0
    cMax = 0
    for _ in range(numRandInits):
        c = np.random.choice([-1, 1], size=X.shape[1])
        c, f, S = altMaximize(X, c)
        if S > Sbase:
            fMax = f
            cMax = c
            Sbase = S

    # extend to targets and samples that didn't occur previously
    fElong = np.random.choice([0, 1], size=nrows)
    fElong[relevantTargs] = fMax
    fOpt = fElong

    cElong = np.zeros(ncols)
    cElong[np.arange(ncols)[relevantSamples]] = cMax  # fancy indexing
    cOpt = cElong

    return (cOpt, fOpt)


def generate_cf_asymp_optimized(X):
    """Generates the optimal column and row embeddings for the asymptotic p-value.

    Args:
        X (numpy.ndarray): The input count matrix, IxJ.

    Returns:
        tuple: A tuple containing the column embedding vector (c) and the row embedding vector (f).
            - c (numpy.ndarray): The length J column embedding vector.
            - f (numpy.ndarray): The length I row embedding vector.
    """
    c = np.ones(X.shape[1])

    zeroIdxs = X.sum(axis=1) == 0
    X = X[~zeroIdxs]

    zeroCols = X.sum(axis=0) == 0
    X = X[:, ~zeroCols]

    # empirical probability dist p over rows of X
    p = X.sum(axis=1)/X.sum()
    Xtild = (X-np.outer(X.sum(axis=1), X.sum(axis=0)) /
             X.sum())@np.diag(1.0/np.sqrt(X.sum(axis=0)))

    A = np.diag(1.0/p)@Xtild @ Xtild.T

    # set f to be principal eigenvector of A
    eigvals, eigvecs = np.linalg.eig(A)
    f = eigvecs[:, np.argmax(eigvals)]

    # retain only real part of f
    f = np.real(f)

    c = Xtild.T@f
    c /= np.linalg.norm(c)

    fOld = f.copy()
    # map the entries of fOld to f, with the zeroIdxs zeroed out
    f = np.zeros(len(zeroIdxs))
    f[~zeroIdxs] = fOld

    cOld = c.copy()
    c = np.zeros(len(zeroCols))
    c[~zeroCols] = cOld

    return (c, f)


# 3. p-value computation

def compute_test_stat(X, c, f, asymptotic=False):
    """Computes the OASIS test statistic.

    Args:
        X (numpy.ndarray): The input count matrix, IxJ.
        c (numpy.ndarray): The column embedding vector, J-dimensional.
        f (numpy.ndarray): The row embedding vector, I-dimensional.
        asymptotic (bool, optional): Whether to return the test statistic for the asymptotic p-value. Default is False (finite sample p-value).

    Returns:
        float: The OASIS test statistic.
    """
    c = np.nan_to_num(c, 0)
    f = np.nan_to_num(f, 0)

    nj = X.sum(axis=0)
    njinvSqrt = 1.0/np.maximum(1, np.sqrt(nj))
    njinvSqrt[nj == 0] = 0

    S = f @ (X-X@np.outer(np.ones(X.shape[1]), nj)/X.sum())@(c*njinvSqrt)
    S = np.abs(S)

    M = X.sum()

    if asymptotic:
        muhat = (f@X).sum()/M

        varF = (f-muhat)**2 @ X.sum(axis=1)/X.sum()
        totalVar = varF * (np.linalg.norm(c)**2 - (c@np.sqrt(nj))**2/M)

        if totalVar <= 0:
            return 0  # numerical error / issue

        normalizedTestStat = S/np.sqrt(totalVar)
    else:
        denom = (np.linalg.norm(c)**2 - (c@np.sqrt(nj))**2/M)
        normalizedTestStat = 2*S / np.sqrt(denom)
    return normalizedTestStat


def compute_pvalue(X, cOpt, fOpt, asymptotic=False):
    """Computes the OASIS p-value for a given contingency table, row embedding, and column embedding.
    Note that in order for the p-value to be valid, the row and column embeddings cannot depend on the input count matrix X.

    Args:
        X (numpy.ndarray): The input count matrix, IxJ.
        cOpt (numpy.ndarray): The column embedding vector, J-dimensional.
        fOpt (numpy.ndarray): The row embedding vector, I-dimensional.
        asymptotic (bool, optional): Whether to compute the asymptotic p-value. Default is False (finite sample p-value).

    Returns:
        float: The OASIS p-value.
    """
    cOpt = np.nan_to_num(cOpt, 0)
    fOpt = np.nan_to_num(fOpt, 0).astype(float)

    if np.all(cOpt == cOpt[0]) or np.all(fOpt == fOpt[0]):
        return 1
    
    # if fOpt.max()-fOpt.min() > 1:
    fOpt /= (fOpt.max()-fOpt.min())
    cOpt /= np.linalg.norm(cOpt)
    
    normalizedTestStat = compute_test_stat(X, cOpt, fOpt, asymptotic)
    if np.isnan(normalizedTestStat):
        return 1
    
    if asymptotic:
        pval = 2*scipy.stats.norm.cdf(-np.abs(normalizedTestStat))
    else:
        pval = 2*np.exp(-normalizedTestStat**2/2)
        
    final_pv = min(np.nan_to_num(pval, 1), 1)
    
    return final_pv



def effectSize_bin(X, c, f):
    """Computes the effect size measure from the OASIS paper. Binarizes samples into positive and negative groups based on the sign of the column embedding.

    Args:
        X (numpy.ndarray): The input count matrix, IxJ.
        c (numpy.ndarray): The column embedding vector, J-dimensional.
        f (numpy.ndarray): The row embedding vector, I-dimensional.

    Returns:
        float: The two-group effect size measure.
    """
    if (c > 0).sum() == 0 or (c < 0).sum() == 0:
        return 0

    e_size = np.abs(f@X@(c > 0) / (X@(c > 0)).sum() - f@X@(c < 0) / (X@(c < 0)).sum())

    return e_size


def OASIS_pvalue(X, numSplits=5, trainFrac=.25, asymptotic=False, return_f_c=False, return_test_stat=False, return_effect_size=False, random_seed=0):
    """
    Computes the p-value using the OASIS method.
        
    Args:
        X (numpy.ndarray): The input count matrix, IxJ.
        numSplits (int, optional): The number of train/test splits for computing optimized f,c on. Default is 5
        trainFrac (float, optional): The fraction of data to be used for training. Default is 0.25.
        asymptotic (bool, optional): Whether to use the asymptotic p-value. Default is False (uses finite sample p-value).
        return_f_c (bool, optional): Whether to return the row and column embeddings. Default is False.
        return_test_stat (bool, optional): Whether to return the test statistic. Default is False.
        return_effect_size (bool, optional): Whether to return the effect size. Default is False.
        random_seed (int, optional): The random seed for reproducibility. Default is 0.

    Returns:
        tuple: A tuple containing the following elements (just the float p-value returned if none of the additional flags are true)::
            - pv (float): The minimum p-value computed across all splits, multiplied by the number of splits (Bonferroni correction). The returned value is capped at 1.
            - f (numpy.ndarray, optional): Length I row embedding vector, f. Returned only if `return_f_c` is True.
            - c (numpy.ndarray, optional): Length J column embedding vector, c. Returned only if `return_f_c` is True.
            - test_stat (float, optional): The OASIS test statistic. Returned only if `return_test_stat` is True.
            - effect_size (float, optional): The effect size measure. Returned only if `return_effect_size` is True.
    """
    I, J = X.shape
    min_pval = 1
    cOpt, fOpt = (np.zeros(J), np.zeros(I))
    test_stat_opt = 0
    effect_size_opt = 0
    f_c_gen_method = generate_cf_asymp_optimized if asymptotic else generate_cf_finite_optimized
    # pval_test_method = testPval_asymp if asymptotic else testPval_finite

    for i in range(numSplits):
        np.random.seed(i+random_seed)
        Xtrain = splitCountsColwise(X, trainFrac)
        Xtest = X-Xtrain
        c, f = f_c_gen_method(Xtrain)
        pval = compute_pvalue(Xtest, c, f, asymptotic)
        
        if pval < min_pval:
            min_pval = pval
            cOpt = c
            fOpt = f
            test_stat_opt = compute_test_stat(Xtest, c, f, asymptotic)
            effect_size_opt = effectSize_bin(Xtest, c, f)

    pval = min(1, numSplits*min_pval)
    return_arr = [pval]
    if return_f_c:
        return_arr.extend([fOpt, cOpt])
    if return_test_stat:
        return_arr.append(test_stat_opt)
    if return_effect_size:
        return_arr.append(effect_size_opt)
        
    if len(return_arr) == 1:
        return return_arr[0]
    return tuple(return_arr)

