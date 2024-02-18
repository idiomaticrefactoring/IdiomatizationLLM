import os, sys
import struct
import traceback

import util_rewrite

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code path: ", code_dir)
sys.path.append(code_dir)
import chatgpt_util, random, chat_gpt_ast_util
import openai, tiktoken, ast, util, util_rewrite,baseline_util
import ast
if __name__ == '__main__':
    user_instr = '''
Refactor the following Python code with star in function call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
{{code}}

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with star in function call.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with star in function call.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with star in function call.
******
Non-Idiomatic code:...
Refactored code:...
'''
    examples = [
['''
Refactor the following Python code with star in function call. You give all code pairs where each pair consists of non-idiomatic Python code and the corresponding refactored code. You respond according to the response format.

Python code:
def make_blobs(
    n_samples=100,
    n_features=2,
    centers=None,
    cluster_std=1.0,
    center_box=(-10.0, 10.0),
    shuffle=True,
    random_state=None,
):
    """Generate isotropic Gaussian blobs for clustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    n_samples : int or array-like, optional (default=100)
        If int, it is the total number of points equally divided among
        clusters.
        If array-like, each element of the sequence indicates
        the number of samples per cluster.

    n_features : int, optional (default=2)
        The number of features for each sample.

    centers : int or array of shape [n_centers, n_features], optional
        (default=None)
        The number of centers to generate, or the fixed center locations.
        If n_samples is an int and centers is None, 3 centers are generated.
        If n_samples is array-like, centers must be
        either None or an array of length equal to the length of n_samples.

    cluster_std : float or sequence of floats, optional (default=1.0)
        The standard deviation of the clusters.

    center_box : pair of floats (min, max), optional (default=(-10.0, 10.0))
        The bounding box for each cluster center when centers are
        generated at random.

    shuffle : boolean, optional (default=True)
        Shuffle the samples.

    random_state : int, RandomState instance or None (default)
        Determines random number generation for dataset creation. Pass an int
        for reproducible output across multiple function calls.
        See :term:`Glossary <random_state>`.

    Returns
    -------
    X : tensor of shape [n_samples, n_features]
        The generated samples.

    y : tensor of shape [n_samples]
        The integer labels for cluster membership of each sample.

    Examples
    --------
    >>> from sklearn.datasets import make_blobs
    >>> X, y = make_blobs(n_samples=10, centers=3, n_features=2,
    ...                   random_state=0)
    >>> print(X.shape)
    (10, 2)
    >>> y
    array([0, 0, 1, 0, 2, 2, 2, 1, 1, 0])
    >>> X, y = make_blobs(n_samples=[3, 3, 4], centers=None, n_features=2,
    ...                   random_state=0)
    >>> print(X.shape)
    (10, 2)
    >>> y
    array([0, 1, 2, 0, 2, 2, 2, 1, 1, 0])

    See also
    --------
    make_classification: a more intricate variant
    """
    from ..utils.checks import AssertAllFinite

    generator = check_random_state(random_state)

    if isinstance(n_samples, numbers.Integral):
        # Set n_centers by looking at centers arg
        if centers is None:
            centers = 3

        if isinstance(centers, numbers.Integral):
            n_centers = centers
            centers = generator.uniform(
                center_box[0], center_box[1], size=(n_centers, n_features)
            )

        else:
            centers = check_array(centers)
            n_features = centers.shape[1]
            n_centers = centers.shape[0]

    else:
        # Set n_centers by looking at [n_samples] arg
        n_centers = len(n_samples)
        if centers is None:
            centers = generator.uniform(
                center_box[0], center_box[1], size=(n_centers, n_features)
            )
        try:
            assert len(centers) == n_centers
        except TypeError:
            raise ValueError(
                "Parameter `centers` must be array-like. " f"Got {centers!r} instead"
            )
        except AssertionError:
            raise ValueError(
                "Length of `n_samples` not consistent"
                f" with number of centers. Got n_samples = {n_samples} "
                f"and centers = {centers}"
            )
        else:
            centers = check_array(centers)
            n_features = centers.shape[1]

    # stds: if cluster_std is given as list, it must be consistent
    # with the n_centers
    if hasattr(cluster_std, "__len__") and len(cluster_std) != n_centers:
        if isinstance(centers.op, AssertAllFinite):
            centers = centers.op.inputs[0]
        raise ValueError(
            "Length of `clusters_std` not consistent with "
            f"number of centers. Got centers = {centers} "
            f"and cluster_std = {cluster_std}"
        )

    if isinstance(cluster_std, numbers.Real):
        cluster_std = mt.full(len(centers), cluster_std)

    X = []
    y = []

    if isinstance(n_samples, Iterable):
        n_samples_per_center = n_samples
    else:
        n_samples_per_center = [int(n_samples // n_centers)] * n_centers

        for i in range(n_samples % n_centers):
            n_samples_per_center[i] += 1

    for i, (n, std) in enumerate(zip(n_samples_per_center, cluster_std)):
        if n == 0:
            continue
        X.append(generator.normal(loc=centers[i], scale=std, size=(n, n_features)))
        y += [i] * n

    X = mt.concatenate(X)
    y = mt.array(y)

    if shuffle:
        X, y = util_shuffle(X, y, random_state=generator)

    return X, y

response format:
Answer: You respond with Yes or No for whether the code has non-idiomatic Python code that can be refactored with star in function call.
Information: You respond with all code pairs where each pair consists of non-idiomatic code and the corresponding refactored code. Each pair splits with "******"
Non-Idiomatic Python code: You respond with identified non-idiomatic Python code that can be refactored with star in function call.
Refactored Python code: You respond with the corresponding idiomatic Python code after refactoring the non-idiomatic code with star in function call.
******
Non-Idiomatic code:...
Refactored code:...
''',
'''
Answer: Yes
Information:
Non-Idiomatic code:
center_box[0], center_box[1]

Refactored code:
*center_box[:2]
******
Non-Idiomatic code:
center_box[0], center_box[1]

Refactored code:
*center_box[:2]
''']]
    save_complicated_code_dir_root = util.data_root + "chatgpt/NonIdiomatic/"
    # save_complicated_code_dir_root = util.data_root + "NonIdiomatic/find_code_snippets/"
    save_complicated_code_dir = save_complicated_code_dir_root + "sample_methods/"
    idiom = "call_star"
    file_name = idiom + "_methods"

    samples = util.load_pkl(save_complicated_code_dir_root, file_name)  # methods_sample

    reponse_list = baseline_util.get_response_directly_refactor(user_instr, examples, samples,
                                                                sys_msg="You are a helpful assistant.")
    
    file_name = "baseline_"+idiom
    util.save_pkl(save_complicated_code_dir_root + "baseline/",
                  file_name,
                  reponse_list)
    '''
    file_name = "baseline_"+idiom
    reponse_list = util.load_pkl(save_complicated_code_dir_root+ "baseline/", file_name)  # methods_sample
    print("reponse_list: ",len(reponse_list))
    '''
