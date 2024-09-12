import numpy as np
import pytest

from groupyr.decomposition import GroupPCA, GroupFPCA, _get_score_func
from groupyr.decomposition import SupervisedGroupPCA, SupervisedGroupFPCA
from sklearn.datasets import load_iris, load_diabetes
from sklearn.decomposition import PCA
from sklearn.feature_selection import f_regression, f_classif
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils._testing import assert_allclose

iris = load_iris()


@pytest.mark.parametrize("exclude_groups", [None, 1, (1, 2)])
@pytest.mark.parametrize("n_components", range(1, iris.data.shape[1]))
def test_group_pca_matches_sklearn_iris_results(n_components, exclude_groups):
    X = iris.data
    pca = PCA(n_components=n_components)

    X_2 = np.hstack([X, X, X])
    groups = [
        np.arange(0, X.shape[1]),
        np.arange(X.shape[1], 2 * X.shape[1]),
        np.arange(2 * X.shape[1], 3 * X.shape[1]),
    ]

    gpca = GroupPCA(
        n_components=n_components, groups=groups, exclude_groups=exclude_groups
    )

    # _ = gpca.fit_transform(X_2)

    X_r = pca.fit_transform(X)
    X_r2 = gpca.fit_transform(X_2)

    hstack_list = [X_r, X_r, X_r]
    if exclude_groups is not None:
        if isinstance(exclude_groups, int):
            hstack_list[exclude_groups] = X
        else:
            for idx in exclude_groups:
                hstack_list[idx] = X

    assert_allclose(X_r2, np.hstack(hstack_list))


def test_group_pca_inverse_matches_input():
    X = iris.data
    X_2 = np.hstack([X, X])
    groups = [np.arange(0, X.shape[1]), np.arange(X.shape[1], 2 * X.shape[1])]

    gpca = GroupPCA(groups=groups, group_names=["one", "two"]).fit(X_2)
    Y = gpca.transform(X_2)
    Y_inv = gpca.inverse_transform(Y)
    assert_allclose(Y_inv, X_2)
    assert gpca.get_feature_names() == (
        [f"one_pc{idx}" for idx in range(Y.shape[1] // 2)]
        + [f"two_pc{idx}" for idx in range(Y.shape[1] // 2)]
    )

    with pytest.raises(TypeError):
        GroupPCA(groups=groups, exclude_groups="error").fit(X_2)


@pytest.mark.parametrize("theta, absolute_threshold", [(1.0, True), (0.8, False)])
def test_supervised_diabetes(theta, absolute_threshold):
    n_components = 3
    diabetes = load_diabetes()

    X = diabetes.data
    y = diabetes.target

    groups = [np.arange(0, X.shape[1]), np.arange(X.shape[1], 2 * X.shape[1])]
    X = np.hstack([X, X])

    sgpca = SupervisedGroupPCA(
        n_components=n_components,
        groups=groups,
        exclude_groups=1,
        theta=theta,
        absolute_threshold=absolute_threshold,
    ).fit(X, y)

    ref_mask = np.ones(20)
    if absolute_threshold:
        zero_idx = [4, 5]
    else:
        zero_idx = [0, 1, 3, 4, 5, 6, 7, 9]
    ref_mask[zero_idx] = 0.0

    assert_allclose(sgpca.screening_mask_, ref_mask)


def test_get_score_func():
    y = np.random.rand(100)
    assert _get_score_func(y) == f_regression

    y = np.random.randint(low=0, high=2, size=100)
    assert _get_score_func(y) == f_classif

    y = np.random.randint(low=0, high=4, size=100)
    assert _get_score_func(y) == f_classif

    with pytest.raises(NotImplementedError):
        y = np.random.rand(100, 2)
        _get_score_func(y)


@pytest.mark.parametrize("binarize", [True, False])
def test_theta_equals_zero_equals_unsupervised(binarize):
    n_components = 3
    diabetes = load_diabetes()

    X = diabetes.data
    y = diabetes.target

    if binarize:
        y = (y > np.median(y)).astype(int)

    groups = [np.arange(0, X.shape[1]), np.arange(X.shape[1], 2 * X.shape[1])]
    X = np.hstack([X, X])

    gpca = GroupPCA(n_components=n_components, groups=groups)
    sgpca = SupervisedGroupPCA(n_components=n_components, groups=groups, theta=0.0)

    X_r = gpca.fit_transform(X, y)
    X_rs = sgpca.fit_transform(X, y)

    assert_allclose(X_r, X_rs)


def test_group_fpca_matches_skfda_results():
    skfda = pytest.importorskip("skfda")
    n_basis = 9
    n_components = 3

    grid_points = np.arange(0.5, 365, 1)
    fd_data = skfda.datasets.fetch_weather()["data"].coordinates[0]
    fd_data = skfda.FDataGrid(np.squeeze(fd_data.data_matrix), grid_points)
    X = fd_data.data_matrix.squeeze()
    X = np.hstack([X, X])
    groups = [np.arange(0, 365), np.arange(365, 730)]
    gfpca = GroupFPCA(
        n_components=n_components,
        n_basis=n_basis,
        basis_domain_range=(0, 365),
        basis="Fourier",
        groups=groups,
    )

    _ = gfpca.fit_transform(X, grid_points=np.hstack([grid_points, grid_points]))

    results = [
        [
            0.9231551,
            0.1364966,
            0.3569451,
            0.0092012,
            -0.0244525,
            -0.02923873,
            -0.003566887,
            -0.009654571,
            -0.0100063,
        ],
        [
            -0.3315211,
            -0.0508643,
            0.89218521,
            0.1669182,
            0.2453900,
            0.03548997,
            0.037938051,
            -0.025777507,
            0.008416904,
        ],
        [
            -0.1379108,
            0.9125089,
            0.00142045,
            0.2657423,
            -0.2146497,
            0.16833314,
            0.031509179,
            -0.006768189,
            0.047306718,
        ],
    ]
    results = np.array(results)

    for grp_idx in range(len(groups)):
        # The sign of the components is arbitrary so we change the sign if necessary
        for i in range(n_components):
            if np.sign(gfpca.components_[grp_idx].coefficients[i][0]) != np.sign(
                results[i][0]
            ):
                results[i, :] *= -1

        np.testing.assert_allclose(
            gfpca.components_[grp_idx].coefficients, results, atol=1e-7
        )


@pytest.mark.parametrize(
    "basis",
    [
        "constant",
        "bspline",
        None,
        "import_bspline",
        "import_constant",
        "import_fourier",
    ],
)
@pytest.mark.parametrize("use_grid_points", [True, False])
@pytest.mark.parametrize("exclude_groups", [None, 1, [1]])
def test_group_fpca_bases(basis, use_grid_points, exclude_groups):
    skfda = pytest.importorskip("skfda")

    if basis == "import_bspline":
        basis = skfda.representation.basis.BSpline
    elif basis == "import_constant":
        basis = skfda.representation.basis.Constant
    elif basis == "import_fourier":
        basis = skfda.representation.basis.Fourier

    n_basis = 9
    n_components = 1

    grid_points = np.arange(0.5, 365, 1)
    fd_data = skfda.datasets.fetch_weather()["data"].coordinates[0]
    fd_data = skfda.FDataGrid(np.squeeze(fd_data.data_matrix), grid_points)
    X = fd_data.data_matrix.squeeze()
    X = np.hstack([X, X])
    groups = [np.arange(0, 365), np.arange(365, 730)]

    if use_grid_points:
        grid_points = np.hstack([grid_points, grid_points])
    else:
        grid_points = None

    gfpca = GroupFPCA(
        n_components=n_components,
        n_basis=n_basis,
        basis_domain_range=(0, 365),
        basis=basis,
        groups=groups,
        exclude_groups=exclude_groups,
    ).fit(X, grid_points=grid_points)

    _ = gfpca.transform(X, grid_points=grid_points)


def test_groupfpca_errors():
    skfda = pytest.importorskip("skfda")

    n_basis = 9
    n_components = 1

    grid_points = np.arange(0.5, 365, 1)
    fd_data = skfda.datasets.fetch_weather()["data"].coordinates[0]
    fd_data = skfda.FDataGrid(np.squeeze(fd_data.data_matrix), grid_points)
    X = fd_data.data_matrix.squeeze()
    X = np.hstack([X, X])
    groups = [np.arange(0, 365), np.arange(365, 730)]

    with pytest.raises(ValueError):
        GroupFPCA(
            n_components=n_components, n_basis=n_basis, basis=object, groups=groups
        ).fit(X)

    with pytest.raises(ValueError):
        GroupFPCA(
            n_components=n_components, n_basis=n_basis, basis="error", groups=groups
        ).fit(X)

    with pytest.raises(TypeError):
        GroupFPCA(
            n_components=n_components,
            n_basis=n_basis,
            groups=groups,
            exclude_groups="error",
        ).fit(X)


@pytest.mark.parametrize(
    "Transformer", [GroupFPCA, GroupPCA, SupervisedGroupFPCA, SupervisedGroupPCA]
)
def test_all_estimators(Transformer):
    return check_estimator(Transformer())
