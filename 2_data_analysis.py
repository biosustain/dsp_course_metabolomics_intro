# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: acore-dev
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Metabolomics DSP Course - Data Analysis

# %% [markdown]
# In this demonstrative exercise, we will perform the downstream analysis of the Metabolights dataset MTBLS8735. This dataset contains three control samples derived from healthy samples, three samples from patients with Cardiovascular disease and four pooled Quality Control (QC) samples. 
#
# The rough workflow of this analysis is:
# - Data filtering
# - Imputation
# - Correcting instrumental drift
# - Normalisation and Visualisation
# - Statistical analysis (ANCOVA)
#
# For most of the analyses, we will be using the python package ACORE, which is a package developed by the Data Science Platform of NNF BRIGHT for analysing multi-omics molecular data - including metabolomics data. The documentation of this package can be found here: [`acore documentation`](https://analytics-core.readthedocs.io/latest/).
# Go there to read about the functions in more detail, or to find out what else you can analyse with acore.
#
# Although we are using acore for almost everything, all of these analyses can be carried out with other programs or in your own code, created in R, Python or other places, as well. This notebook serves primarily as a demonstration of the necessary steps of a typical downstream metabolomics data analysis.

# %% [markdown]
# ##### Imports

# %%
# %pip install acore

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import vuecore.plots.basic.scatter


# %% [markdown]
# ##### Helper functions
# First, we are defining some helper functions. Feel free to ignore these while we go through the exercise, they are for example plotting functions. Do, however, run the cells.

# %%
def plot_pca(
    df: pd.DataFrame,
    groups: dict[str, list],  # e.g. {"Control": [0,1,2], "Treatment": [3,4,5]}
    scale: bool = True,
    n_components: int = 2,
    figsize: tuple = (7, 5),
    title: str = "PCA Score Plot",
    palette: list = None,
    ellipse: bool = True,  # 95% confidence ellipse per group
    label_points: bool = False,  # annotate each point with its index
):
    """
    PCA score plot for metabolomics data.

    Parameters
    ----------
    df          : samples × features DataFrame (rows = samples)
    groups      : dict mapping group name -> list of row indices (int or label)
    scale       : z-score scale features before PCA (recommended)
    n_components: number of PCs to compute (≥2)
    ellipse     : draw a 95% confidence ellipse per group
    label_points: annotate each dot with its row index/label
    """

    # build ordered index and group label array
    all_idx = [i for idxs in groups.values() for i in idxs]
    group_labels = {i: grp for grp, idxs in groups.items() for i in idxs}

    X = df.loc[all_idx].copy()
    labels = [group_labels[i] for i in X.index]

    # scale & fit PCA
    if scale:
        X_vals = StandardScaler().fit_transform(X.values)
    else:
        X_vals = X.values

    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X_vals)
    var_exp = pca.explained_variance_ratio_ * 100

    # colours
    group_names = list(groups.keys())
    if palette is None:
        palette = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    color_map = {g: palette[i % len(palette)] for i, g in enumerate(group_names)}

    # plot
    fig, ax = plt.subplots(figsize=figsize)

    for grp in group_names:
        mask = [l == grp for l in labels]
        pts = scores[mask]
        color = color_map[grp]

        ax.scatter(pts[:, 0], pts[:, 1], label=grp, color=color, s=80, zorder=3)

        if label_points:
            idx_list = groups[grp]
            for pt, idx in zip(pts, idx_list):
                ax.annotate(
                    str(idx), pt, textcoords="offset points", xytext=(5, 4), fontsize=8
                )

        if ellipse and len(pts) > 2:
            _confidence_ellipse(pts[:, 0], pts[:, 1], ax, color=color)

    ax.axhline(0, color="grey", lw=0.5, ls="--")
    ax.axvline(0, color="grey", lw=0.5, ls="--")
    ax.set_xlabel(f"PC1 ({var_exp[0]:.1f}%)", fontsize=12)
    ax.set_ylabel(f"PC2 ({var_exp[1]:.1f}%)", fontsize=12)
    ax.set_title(title, fontsize=13)
    ax.legend(framealpha=0.3)
    plt.tight_layout()
    plt.show()

    return pca, scores, var_exp


def _confidence_ellipse(x, y, ax, n_std=1.96, color="tab:blue", alpha=0.15, **kwargs):
    """Draw a covariance-based 95% confidence ellipse."""

    cov = np.cov(x, y)
    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    rx = np.sqrt(1 + pearson)
    ry = np.sqrt(1 - pearson)

    ellipse = Ellipse(
        (0, 0),
        width=rx * 2,
        height=ry * 2,
        facecolor=color,
        alpha=alpha,
        edgecolor=color,
        linewidth=1.5,
        linestyle="--",
        **kwargs,
    )
    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_x, mean_y = np.mean(x), np.mean(y)

    t = (
        transforms.Affine2D()
        .rotate_deg(45)
        .scale(scale_x, scale_y)
        .translate(mean_x, mean_y)
    )

    ellipse.set_transform(t + ax.transData)
    ax.add_patch(ellipse)


def plot_feature_missingness(data):
    missing_features = data.isnull().mean() * 100
    missing_features_nonzero = missing_features[missing_features > 0]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    ax = axes[0]
    ax.hist(
        missing_features_nonzero.values,
        bins=30,
        color="mediumvioletred",
        edgecolor="white",
        linewidth=0.5,
    )
    ax.set_xlabel("Missing (%)")
    ax.set_ylabel("Number of features")
    ax.set_title(
        f"Distribution of missingness\n({len(missing_features_nonzero)} features with any missing)"
    )
    ax.axvline(
        x=20, color="black", linestyle="--", linewidth=0.8, label="20% threshold"
    )
    ax.legend()

    # Dot plot, sorted by missingness
    ax = axes[1]
    sorted_missing = missing_features.sort_values(ascending=True).reset_index(drop=True)
    ax.scatter(
        sorted_missing.index,
        sorted_missing.values,
        s=4,
        color="mediumvioletred",
        alpha=0.6,
        linewidths=0,
    )
    ax.set_xlabel("Features (sorted by missingness)")
    ax.set_ylabel("Missing (%)")
    ax.set_title("Sorted missingness per feature")
    ax.axhline(
        y=20, color="black", linestyle="--", linewidth=0.8, label="20% threshold"
    )
    ax.legend()

    plt.tight_layout()
    plt.show()


def missingness_summary(df_before, df_after):
    total = df_before.size
    n_before = df_before.isnull().sum().sum()
    n_after = df_after.isnull().sum().sum()

    print(f"Total values      : {total:,}")
    print(f"Missing before    : {n_before:,}  ({100*n_before/total:.1f}%)")
    print(f"Missing after     : {n_after:,}  ({100*n_after/total:.1f}%)")
    print(
        f"Features affected : {(df_before.isnull().any()).sum()} / {df_before.shape[1]}"
    )
    print(
        f"Samples affected  : {(df_before.isnull().any(axis=1)).sum()} / {df_before.shape[0]}"
    )


def plot_intensity_distribution(data):
    values = data.values.flatten().astype(float)

    n_total = data.size
    n_missing = int(np.isnan(values).sum())
    pct_missing = n_missing / n_total * 100

    log_values = np.log10(values[(~np.isnan(values)) & (values > 0)])

    fig, (ax_nan, ax_hist) = plt.subplots(
        1, 2, figsize=(11, 5), gridspec_kw={"width_ratios": [1, 8]}, sharey=True
    )

    ax_nan.bar(0, n_missing, width=0.2, color="mediumvioletred", alpha=0.8)
    ax_nan.set_xlim(-0.5, 0.5)
    ax_nan.set_xticks([0])
    ax_nan.set_xticklabels([f"NaN\n({pct_missing:.1f}%)"], fontsize=9)
    ax_nan.set_ylabel("Count")

    ax_hist.hist(
        log_values, bins=100, color="cornflowerblue", edgecolor="none", alpha=0.8
    )
    ax_hist.set_xlabel("Intensity (log₁₀)")
    ax_hist.set_title("Intensity distribution (all features, all samples)")
    ax_hist.yaxis.set_visible(False)

    plt.tight_layout()
    plt.show()


def plot_loess_example_curve(
    df: pd.DataFrame,
    feature_idx: int,
    samples: list,
    qcs: list,
    sample_order: pd.DataFrame,
    show_corrected: bool = True,
    alpha: float = None,  # fixed smoothing span; if None, selected by LOOCV
):
    """
    Plot the raw intensities, LOESS drift curve, and optionally the corrected
    intensities for a single feature according to the loess drift correction function.
    Useful for inspecting drift behaviour before running full drift correction.

    The drift curve is estimated with the same method used by
    ldc.run_drift_correction: LOESS is fit to the QC points and then
    interpolated across all injection positions via a cubic spline
    (qc_rlsc_loess).

    Parameters
    ----------
    df : pd.DataFrame
        Feature matrix with samples as rows and features as columns.
        Metadata columns should have been removed already.
    feature_idx : int
        Column index of the feature to plot.
    samples : list of str
        Row index labels of the biological samples.
    qcs : list of str
        Row index labels of the pooled QC samples.
    sample_order : pd.DataFrame
        Injection-order table with columns `File Name` and `Sample ID`
        (integer run order).
    show_corrected : bool, optional
        If True (default), overlays drift-corrected sample intensities as
        diamond markers.
    alpha : float, optional
        LOESS smoothing span (0 < α ≤ 1). If None (default), the optimal span
        is selected automatically by leave-one-out cross-validation over
        α ∈ [0.40, 1.00]. The selected value is shown in the legend.
    """

    all_rows = samples + qcs
    feature_col = df.iloc[:, feature_idx]

    order_dict = sample_order.set_index("File Name")["Sample ID"].to_dict()
    x_all = np.array([order_dict.get(r, np.nan) for r in all_rows])
    y_all = feature_col.loc[all_rows].astype(float).values

    n_s = len(samples)
    x_sample, y_sample = x_all[:n_s], y_all[:n_s]
    x_qc_arr, y_qc_arr = x_all[n_s:], y_all[n_s:]

    valid_sample = ~np.isnan(x_sample) & ~np.isnan(y_sample)
    valid_qc = ~np.isnan(x_qc_arr) & ~np.isnan(y_qc_arr)
    x_s_v, y_s_v = x_sample[valid_sample], y_sample[valid_sample]
    x_qc_v, y_qc_v = x_qc_arr[valid_qc], y_qc_arr[valid_qc]

    feature_name = df.columns[feature_idx]

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.scatter(x_s_v, y_s_v, label="Samples", color="steelblue", alpha=0.7, zorder=3)
    ax.scatter(
        x_qc_v, y_qc_v, label="QC", color="firebrick", edgecolor="k", s=60, zorder=4
    )

    if len(x_qc_v) >= 4:
        if alpha is not None:
            # Pass a single-element candidate list to skip LOOCV and use the given alpha
            # directly
            drift_curve, best_alpha = dc.qc_rlsc_loess(
                x_qc_v, y_qc_v, x_all, always_use_default=True, default=alpha
            )
        else:
            drift_curve, best_alpha = dc.qc_rlsc_loess(x_qc_v, y_qc_v, x_all)

        valid_curve = ~np.isnan(x_all) & ~np.isnan(drift_curve)
        sort_idx = np.argsort(x_all[valid_curve])
        ax.plot(
            x_all[valid_curve][sort_idx],
            drift_curve[valid_curve][sort_idx],
            label=f"LOESS drift curve (α={best_alpha:.2f})",
            color="black",
            lw=2,
            zorder=5,
        )

        if show_corrected:
            median_qc = np.median(y_qc_v)
            drift_at_samples = drift_curve[:n_s][valid_sample]
            corrected = (y_s_v / drift_at_samples) * median_qc
            ax.scatter(
                x_s_v,
                corrected,
                label="Corrected samples",
                color="lightsteelblue",
                marker="D",
                s=40,
                alpha=0.9,
                zorder=3,
            )
    else:
        print(f"Not enough valid QC points for LOESS ({len(x_qc_v)} found, need ≥4).")

    ax.set_xlabel("Injection Order")
    ax.set_ylabel("Intensity")
    ax.set_title(f"Drift correction example ({feature_name})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def pca_for_cpca_drift(
    df: pd.DataFrame,
    samples,  # list of row index labels, OR dict {group_name: [row index labels]}
    qcs: list,
    log_transform: bool = True,
    title: str = "PCA",
):
    """
    PCA of samples and QC samples.

    Parameters
    ----------
    df      : feature matrix with samples as rows and features as columns.
              Metadata columns should have been removed already.
    samples : list of row index labels of the biological samples (all one group),
              or dict {group_name: [row index labels]} for multiple groups
    qcs     : list of row index labels of the pooled QC samples
    log_transform : apply log1p before scaling
    title   : plot title
    """
    # Normalise samples to a dict
    if isinstance(samples, list):
        sample_groups = {"Samples": samples}
    else:
        sample_groups = samples

    # Build ordered row + label arrays
    all_rows, labels = [], []
    for group, rows in sample_groups.items():
        for r in rows:
            if r in df.index:
                all_rows.append(r)
                labels.append(group)
    for r in qcs:
        if r in df.index:
            all_rows.append(r)
            labels.append("QC")

    # Coerce to numeric, drop features (columns) with any NaN
    X = df.loc[all_rows].apply(pd.to_numeric, errors="coerce").dropna(axis=1)

    if log_transform:
        X = np.log1p(X.clip(lower=0))

    X_scaled = StandardScaler().fit_transform(X.values.astype(float))

    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)
    pc1_var = pca.explained_variance_ratio_[0] * 100
    pc2_var = pca.explained_variance_ratio_[1] * 100

    palette = plt.cm.tab10.colors
    color_map = {g: palette[i % len(palette)] for i, g in enumerate(sample_groups)}
    color_map["QC"] = "black"

    fig, ax = plt.subplots(figsize=(8, 6))
    for group in list(sample_groups) + ["QC"]:
        mask = [_label == group for _label in labels]
        pts = coords[mask]
        is_qc = group == "QC"
        ax.scatter(
            pts[:, 0],
            pts[:, 1],
            label=group,
            color=color_map[group],
            marker="D" if is_qc else "o",
            s=70 if is_qc else 50,
            edgecolors="k" if is_qc else "none",
            alpha=0.9 if is_qc else 0.75,
            zorder=5 if is_qc else 3,
        )

    ax.set_xlabel(f"PC1 ({pc1_var:.1f}%)")
    ax.set_ylabel(f"PC2 ({pc2_var:.1f}%)")
    ax.set_title(title)
    ax.axhline(0, color="grey", lw=0.5, ls="--")
    ax.axvline(0, color="grey", lw=0.5, ls="--")
    ax.legend(framealpha=0.8)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()


# %% [markdown]
# ### Data setup

# %% [markdown]
# First, let's load and have a look at our data. You can find it in the data folder of this codespace.

# %%
metaboigniter_data = pd.read_csv(
    "../data/MTBLS8735/MTBLS8735_preprocessed.csv", index_col=0
)
metaboigniter_data

# %%
metaboigniter_data.columns

# %% [markdown]
# You can see that we have our features in the rows, and that there are 9068 of them. We have some metadata like mass-to-charge ratios and retention times, and then we have our intensities.
#
# In order to properly analyse our data, we have to transpose it first. We also have to remove the metadata columns.

# %%
data = metaboigniter_data.T
data = data.drop(
    [
        "mzmed",
        "mzmin",
        "mzmax",
        "rtmed",
        "rtmin",
        "rtmax",
        "npeaks",
        "CTR",
        "CVD",
        "QC",
        "ms_level",
    ]
)
data

# %% [markdown]
# Now our data consists of only features in the columns, and samples in the rows.
#
# We are also going to define some variables that help us later on in the code.

# %%
samples = [
    "MS_F_POS.mzML",
    "MS_E_POS.mzML",
    "MS_C_POS.mzML",
    "MS_A_POS.mzML",
    "MS_B_POS.mzML",
    "MS_D_POS.mzML",
]
samples_cvd = ["MS_F_POS.mzML", "MS_A_POS.mzML", "MS_D_POS.mzML"]
samples_ctr = ["MS_E_POS.mzML", "MS_C_POS.mzML", "MS_B_POS.mzML"]
qcs = [
    "MS_QC_POOL_1_POS.mzML",
    "MS_QC_POOL_2_POS.mzML",
    "MS_QC_POOL_3_POS.mzML",
    "MS_QC_POOL_4_POS.mzML",
]


groups_samples = {
    "CTR": samples_ctr,
    "CVD": samples_cvd,
}
groups_all = {
    "CTR": samples_ctr,
    "CVD": samples_cvd,
    "QC": qcs,
}

# %% [markdown]
# ## Data filtering
#
# As a first step, we need to filter our data. There are many features in the data which are artifacts, background noise or unreliable. Additionally, there is a lot of missingness. While missing values can be imputed, it's better to remove features with high levels of missingness first and only impute features that have signal in most samples.
#
# We will use three methods of filtering:
# - 80%-rule
# - Coefficient of Variation (CV)-based filtering
# - Dispersion ratio (D-ratio) filtering
#
#
# For most of these, we will use the `filter_metabolomics` module from acore.

# %%
from acore import filter_metabolomics as fm

# %% [markdown]
# Let's first check how much missingness there is in the data.

# %%
plot_feature_missingness(data)
plot_intensity_distribution(data)

# %% [markdown]
# There are quite a lot of missing values, so it is important that we filter first.

# %% [markdown]
# #### 80%-rule for filtering

# %% [markdown]
# The 80%-rule filters out features with too much missingness from our data. More
# specifically, if for a feature, more than 20% of the data is missing across all sample
# columns, it will be removed, so features must have at least 80% of data present in order
# to be retained.
#
# Although it is called the 80%-rule, other thresholds can be used to make the filtering
# more lenient or more stringent.
#
# In acore, this method is implemented in the function filter_by_missingness. Let's first
# have a look at our function.

# %%
help(fm.filter_by_missingness)

# %%
data_filtered_1 = fm.filter_by_missingness(
    data=data,
    method="classic",
    percent=80,  # 80% present, 20% missing is allowed at most
    samples=samples,
)

# %%
print(
    f"Num. of features before filtering: {data.shape[1]}\n"
    f"Num. of features after filtering: {data_filtered_1.shape[1]}"
)
print(f"Difference: {data.shape[1]-data_filtered_1.shape[1]} features removed.")

# %% [markdown]
# Now we have removed 836 features.

# %% [markdown]
# #### CV-based filtering
# In this method, we are taking into account the quality control (QC) samples.
#
# The CV of the biological samples and the CV of the QC samples are calculated per
# feature, and if for a given feature the CV of the QC samples is larger than that of the
# biological samples, it is removed.
# Also, if there are not enough QC samples to calculate the CV, or the mean is near zero, the features will be removed.
#
# In acore, this method is implemented in the function filter_cv.

# %%
data_filtered_2 = fm.filter_cv(data=data_filtered_1, samples=samples, qcs=qcs)

# %%
print(
    f"Num. of features before filtering: {data_filtered_1.shape[1]}\n"
    f"Num. of features after filtering: {data_filtered_2.shape[1]}"
)
print(
    f"Difference: {data_filtered_1.shape[1]-data_filtered_2.shape[1]} features removed."
)


# %% [markdown]
# #### D-ratio filtering
# Finally, we will do dispersion ratio filtering.
#
# This method scores each feature by the ratio of its analytical noise (QC) to its total variation, meaning the standard deviation across pooled QC injections divided by the standard deviation across biological samples. 
#
# A low D-ratio means biological variation dominates the technical noise, and a high one means the feature is mostly measurement noise with little biological signal, so features above a threshold (typically 0.5 or lower) get removed.
#
# Here, we will use the median absolute deviation (MAD, scaled by 1.4826). Because medians ignore extreme values, this version resists outliers and skew, making it the better choice for non-Gaussian data like raw untargeted peak areas — whereas the standard-deviation version is preferable when the data are roughly Gaussian (or have been log-transformed first).
#
# This method is not implemented in acore yet, so we will define it ourselves.

# %%
def filter_dratio(
    data: pd.DataFrame,
    samples: list,
    qcs: list,
    threshold: float = 0.5,
):
    if len(qcs) < 2:
        raise ValueError(
            f"You need more than 1 QC sample to apply this filtering method. Got {len(qcs)}."
        )
    if len(samples) < 2:
        raise ValueError(
            f"You need more than 1 biological sample to apply this filtering method. "
            f"Got {len(samples)}."
        )

    def mad(df):  # median absolute deviation
        # 1.4826 * median(|x - median(x)|), an unbiased SD estimate for Gaussian data.
        med = df.median()
        return 1.4826 * (df - med).abs().median()

    df = data.copy()

    disp_qcs = mad(df.loc[qcs])
    disp_samples = mad(df.loc[samples])
    dratio = disp_qcs / disp_samples

    undefined = dratio.isna() | dratio.isin([np.inf, -np.inf])
    if undefined.any():
        print(
            f"D-ratio is undefined for {undefined.sum()} feature(s) (zero or near-zero biological "
            f"dispersion): {list(df.columns[undefined])}. These features will be dropped.",
        )

    keep = (dratio <= threshold) & ~undefined

    return df.loc[:, keep]


# %%
data_filtered_3 = filter_dratio(data=data, samples=samples, qcs=qcs, threshold=0.4)

# %%
print(
    f"Num. of features before filtering: {data_filtered_2.shape[1]}\n"
    f"Num. of features after filtering: {data_filtered_3.shape[1]}"
)
print(
    f"Difference: {data_filtered_2.shape[1]-data_filtered_3.shape[1]} features removed."
)

# %%
print(f"Now we have a total of {data_filtered_3.shape[1]} features left.")

# %% [markdown]
# ## Imputation
#
# While we have filtered out a lot of missingness, we still have missing values in our data. Those are filled in with imputation. Imputation methods for metabolomics are also implemented in acore. Here we will use the half minimum to impute our values with. 

# %%
from acore.imputation_analysis import (
    imputation_half_minimum,
    imputation_zeros,
)

# %% [markdown]
# But first, let's re-assess how much we need to fill in.

# %%
print(f"Total count of missing cells: {data_filtered_3.isnull().sum().sum()}")
print(
    f"Overall percentage of missingness: {data_filtered_3.isnull().mean().mean() * 100}\n"
)

plot_feature_missingness(data_filtered_3)
plot_intensity_distribution(data_filtered_3)

# %% [markdown]
# #### Impute with half minimum
#
# In this imputation method, we are calculating the minimum of each feature, taking the half of that and using that value to fill in missing values for that feature. This method is implemented in the acore function imputation_half_minimum().
#
# Note: Another commonly used method in metabolomics data imputation is imputing with zeros. This method can also be applied through acore, with the function imputation_zeros().

# %%
data_imputed = imputation_half_minimum(data=data_filtered_3)

# %%
data_imputed

# %%
print(f"Total count of missing cells: {data_imputed.isnull().sum().sum()}")
print(
    f"Overall percentage of missingness: {data_imputed.isnull().mean().mean() * 100}\n"
)

print("SUMMARY of imputation changes:")
missingness_summary(data, data_imputed)
plot_intensity_distribution(data_imputed)

# %% [markdown]
# Now we have filled in all missing values. We can now plot the data in a PCA plot to see whether the samples can be separated well with principal components. We can use the functions we defined earlier at the beginning of the notebook for that.
#
# We can plot the PCA first with all samples and QCs, and then with just the samples, to see how the groups separate.

# %%
pca_model, scores, var_explained = plot_pca(
    data_imputed, groups_all, label_points=True, title="PCA on imputed data"
)
pca_model, scores, var_explained = plot_pca(
    data_imputed, groups_samples, label_points=True, title="PCA on imputed data"
)

# %% [markdown]
# The first plot shows that the QC samples separate quite well from the biological samples.
#
# The second plot shows that the two groups are also separated quite well, although one of the control samples, sample C, clusters slightly away from the rest.

# %% [markdown]
# ## Drift correction

# %% [markdown]
# Now that we have a data frame that has been filtered and is fully filled in, we will look at the within-batch effects. In metabolomics, instrumental drift is common, so the signal degrades over time. 
#
# This is what we have the QC samples for, which is why they are so important to have included in the study. 
#
# We will test two different methods for correcting the instrumental drift in this notebook, inspect the results, and then choose one to continue with.

# %%
from acore import drift_correction as dc

# %% [markdown]
# #### Loess smoothing drift correction
#
# Pooled QC samples are injected at regular intervals over time throughout the experiment. The QC intensities for each features should theoretically be consistent in each measurement. Therefore, any variation in these samples reflect artificial variation, so instrumental drift, instead of biological variation.
#
# LOESS (LOcally Estimated Scatterplot Smoothing) is a non-parametric regression that fits a smooth curve through data without assuming a fixed equation. We use it here to fit a curve over the QC points, and then we rescale the biological sample intensities by the drift estimate. This will be explained better by the visualisations in the real example below.
#
# LOESS smoothing based drift correction is implemented in the loess_drift_correction acore module.

# %% [markdown]
# In order to use this method, we need to know the order in which the samples, including QCs, were run. We have this information in our metadata.

# %%
sample_order = pd.read_csv("../data/MTBLS8735/sample_metadata_metaboigniter.csv")
sample_order

# %%
data_corrected_loess, correction_info = dc.run_loess_drift_correction(
    data=data_imputed, qc_rows=qcs, sample_rows=samples, sample_order=sample_order
)
data_corrected_loess

# %% [markdown]
# Our dataframe has the same structure as before. 
#
# We can also look at the object correction_info, if we want to trace the exact correction that was applied to every feature. 

# %%
correction_info["FT0001"]

# %% [markdown]
# To understand better what is happening, we can plot a single feature with all its measurements over time, and the loess curve that is calculated over it. We can try out a few different features to see what would happen, and also try different smoothing parameters to see how the curve changes.

# %%
plot_loess_example_curve(
    df=data_imputed,
    feature_idx=2,
    samples=samples,
    qcs=qcs,
    sample_order=sample_order,
)

# %% [markdown]
# #### CPCA
#
# Standard PCA finds orthogonal directions (principal components) that capture maximum variance in a single dataset. Common PCA extends this to multiple groups: instead of computing separate components per batch, it tries to find a set of components that are common across groups. 
#
# In this case, it finds the principal components that are common across all samples, because the assumption is that those are the ones that are due to artificial variation, whereas the variance in biological samples will not be shared across all.
#
# First, we can plot a PCA for this purpose.

# %%
pca_for_cpca_drift(
    data_imputed,
    samples=samples,  # list of col names, OR dict {group_name: [col names]}
    qcs=qcs,
    log_transform=True,
    title="PCA",
)

# %% [markdown]
# The QC samples are already quite close together, but there is some variation.
#
# We can use the acore function cpca_drift_correction for this.
#

# %%
data_corrected_cpca = dc.run_cpca_drift_correction(
    data_imputed, sample_rows=samples, qc_rows=qcs, n_comps=1
)

# %%
pca_for_cpca_drift(
    data_corrected_cpca,
    samples=samples,  # list of col names, OR dict {group_name: [col names]}
    qcs=qcs,
    log_transform=True,
    title="PCA",
)

# %%
df_corrected_2comps = dc.run_cpca_drift_correction(
    data_imputed, samples, qcs, n_comps=2
)
df_corrected_3comps = dc.run_cpca_drift_correction(
    data_imputed, samples, qcs, n_comps=3
)
df_corrected_4comps = dc.run_cpca_drift_correction(
    data_imputed, samples, qcs, n_comps=4
)

# %%
pca_for_cpca_drift(
    df_corrected_2comps,
    samples,
    qcs,
    log_transform=True,
    title="PCA with 2 components",
)

pca_for_cpca_drift(
    df_corrected_3comps,
    samples,
    qcs,
    log_transform=True,
    title="PCA with 3 components",
)

pca_for_cpca_drift(
    df_corrected_4comps,
    samples,
    qcs,
    log_transform=True,
    title="PCA with 4 components",
)

# %%
pca_model, scores, var_explained = plot_pca(
    data_corrected_loess,
    groups_all,
    label_points=True,
    title="PCA on LOESS-corrected data",
)
pca_model, scores, var_explained = plot_pca(
    data_corrected_loess,
    groups_samples,
    label_points=True,
    title="PCA on LOESS-corrected data",
)
pca_model, scores, var_explained = plot_pca(
    data_corrected_cpca,
    groups_all,
    label_points=True,
    title="PCA on CPCA-corrected data",
)
pca_model, scores, var_explained = plot_pca(
    data_corrected_cpca,
    groups_samples,
    label_points=True,
    title="PCA on CPCA-corrected data",
)

# %% [markdown]
# Continuing with ???

# %% [markdown]
# ## Normalization
#
# We will also normalise the data with Z-score normalisation. In this case, this will be mainly for visualisation purposes, again to see whether the data is separating well.
#
# We will use an acore function for this again.

# %%
from acore import normalization

# %%
data_normalized = normalization.normalize_data(data_corrected_cpca, "zscore")
data_normalized

# %%
plot_intensity_distribution(data_normalized)

# %%
pca_model, scores, var_explained = plot_pca(
    data_normalized, groups_all, label_points=True, title="PCA on normalized data"
)
pca_model, scores, var_explained = plot_pca(
    data_normalized, groups_samples, label_points=True, title="PCA on normalized data"
)

# %% [markdown]
# We can see... ? depends on which data we choose.

# %% [markdown]
# ## Statistical analysis

# %% [markdown]
# #### ANCOVA
#
# We will now do a statistical analysis. We want to find out which ones of our metabolites are significantly more abundant in the cardiovascular disease group vs the control, or the other way around.
#
# For this, we will do an ANCOVA (analysis of covariance), which compares group means on an outcome while statistically controlling for one or more continuous variables (covariates) that also influence the outcome. In this case, the covariate is age, because we have this in our metadata and know that it could potentially affect the sample outcomes.
#
# We are using another acore function for this.

# %%
import acore.differential_regulation as ad

# %% [markdown]
# We need to do some preparation before we can run the function.

# %%
# Create the variable with the data
# data_ancova = data_corrected_cpca.copy()
data_ancova = np.log2(data_imputed)

# Prepare the data to fit the function input
subject_col = data_ancova.index.name or "index"
data_ancova.rename_axis(subject_col, axis=0, inplace=True)

# Add group information to the data frame as a column
group_map = {
    sample: label for label, samples in groups_all.items() for sample in samples
}
data_ancova.insert(0, "group", data_ancova.index.map(group_map))

# Remove the QC samples
data_ancova = data_ancova[data_ancova["group"] != "QC"]

# Add the column of age information
metadata = sample_order.copy()
metadata.index = metadata["File Name"]
data_ancova.insert(1, "age", metadata["age"])

# %%
data_ancova

# %% [markdown]
# Now we can run ANCOVA.

# %%
ancova = (
    ad.run_ancova(
        data_ancova.astype({"group": str}),  # ! target needs to be of type str
        # subject=subject_col, # not used
        drop_cols=[],
        group="group",  # needs to be a string
        covariates=["age"],
    )
    .set_index("identifier")
    .sort_values(by="padj")
)  # need to be floats?
ancova

# %% [markdown]
# We have filtered the table by the adjusted pvalue. We can look at the top values to see how good our best hits are.
#
# ?? add more info when we have decided

# %% [markdown]
# Now we can inspect the results in a few different ways. First of all, we can look at the group averages, which are shown in the first six columns.

# %%
ancova.iloc[:, :6]

# %% [markdown]
# If we filter to the words below, we can inspect the test results (based on a linear model) for each feature (on each row). The posthoc values are not interesting in this case as we are only comparing between two groups (ctr and cvd). We are mainly interested in the adjusted pvalue (pajd), and in whether the null hypothesis was rejected or not. If rejected=True, it means our feature was significant according to the thresholds we have set.

# %%
regex_filter = "pval|padj|reject|post"
ancova.filter(regex=regex_filter)

# %% [markdown]
# You can also look at the rest of the results.

# %%
ancova.iloc[:, 6:].filter(regex=f"^(?!.*({regex_filter})).*$")

# %% [markdown]
# Now we can plot a volcano plot, which is a scatter plot that combines statistical significance and effect size (magnitude of change) in a single view.

# %%
scatter_plot_adv = vuecore.plots.basic.scatter.create_scatter_plot(
    data=ancova.reset_index(),
    x="log2FC",
    y="-log10 pvalue",
    color="rejected",
    title="Volcano Plot showing CTR vs CVD samples",
    subtitle="Visualizing ANCOVA results",
    labels={
        "log2FC": "Log2 Fold Change",
        "-log10 pvalue": "-log10(p-value)",
        "pvalue": "Raw P value",
        "rejected": "FDR corrected Significant",
        "identifier": "Feature Identifier",
    },
    hover_data=["identifier"],
    # currently does not work:
    # color_discrete_map={False: "#2166AC", True: "#B2182B"},  # Blue  # Red
    color_discrete_sequence=["red", "blue"],
    opacity=1,
    marker_line_width=1,
    marker_line_color="darkgray",
    width=800,
    height=600,
)
scatter_plot_adv

# %%
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Raw p-values
axes[0].hist(
    ancova["pvalue"].dropna(),
    bins=50,
    color="steelblue",
    edgecolor="white",
    linewidth=0.5,
)
axes[0].set_title("Distribution of Raw P-values", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Raw p-value")
axes[0].set_ylabel("Count")
axes[0].axvline(x=0.05, color="red", linestyle="--", linewidth=1.5, label="α = 0.05")
axes[0].legend()

# Adjusted p-values
axes[1].hist(
    ancova["padj"].dropna(),
    bins=50,
    color="darkorange",
    edgecolor="white",
    linewidth=0.5,
)
axes[1].set_title(
    "Distribution of Adjusted P-values (FDR correction BH)",
    fontsize=14,
    fontweight="bold",
)
axes[1].set_xlabel("Adjusted p-value")
axes[1].set_ylabel("Count")
axes[1].axvline(x=0.05, color="red", linestyle="--", linewidth=1.5, label="α = 0.05")
axes[1].legend()


plt.suptitle("P-value Distributions", fontsize=16, fontweight="bold", y=1.02)
plt.tight_layout()
plt.show()

# %% [markdown]
# In the above plot, we are looking at our pvalues and adjusted pvalues in more detail. 
#
# We can also see how many features survived each threshold in the calculations below.

# %%
print("Raw p < 0.05:", (ancova["pvalue"] < 0.05).sum())
print("Raw p < 0.01:", (ancova["pvalue"] < 0.01).sum())
print("padj < 0.05: ", (ancova["padj"] < 0.05).sum())
print("padj < 0.1:  ", (ancova["padj"] < 0.1).sum())

# %% [markdown]
# ## Identify hits
#
# Finally, we can identify our best hits to then be analysed further. Once we have found our top hits, we can match the (for now unknown) features with library spectra and identify which metabolites they are. Then, we can carry out further analyses such as enrichment analysis.

# %%
# Primary hit list for follow-up
hits = ancova[(ancova["pvalue"] < 0.01) & (ancova["log2FC"].abs() > 1)]
print(f"Candidate metabolites: {len(hits)}")
print(f"Upregulated in CVD: {(hits['log2FC'] > 0).sum()}")
print(f"Downregulated in CVD: {(hits['log2FC'] < 0).sum()}")

# %% [markdown]
# We can save and export our hits to a csv file.

# %%
hits.to_csv("MTBLS8735_tophits.csv")
