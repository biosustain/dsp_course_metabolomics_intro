# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: umetaflow-pyopenms
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Pre-processing of LC-MS/MS metabolomics data using pyOpenMS

# %%
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyopenms as oms

# %% [markdown]
# The relevant files are selected:

# %%
metadata = pd.read_csv("data/MTBLS8735/metadata.csv")

input_labels = metadata["phenotype"].tolist()

input_files = []
for i in range(len(metadata)):
    f = re.sub(r"FILES/", "", metadata["derived_spectra_data_file"][i])
    input_files.append("data/MTBLS8735/" + f)

fname_intern_standard = os.path.join("data", "MTBLS8735", "intern_standard_list.txt")


# %% [markdown]
# ## Data visualization
# Before starting the pre-processing workflow, we visualize the **Base Peak
# Chromatogram (BPC)** for each sample. The BPC represents the intensity of the most
# intense ion detected in every MS1 spectrum over the course of the chromatographic run.
# Plotting the BPC provides a quick overview of the data quality and allows us to compare
# the overall signal profiles between samples. Similar chromatographic patterns across
# runs suggest consistent instrument performance, while large differences may indicate
# potential issues that should be investigated before proceeding with further analysis.


# %% tags=["hide-input"]
def extract_bpc(exp):

    bpc_rt = []
    bpc_int = []

    for spec in exp:
        if spec.getMSLevel() != 1:
            continue

        peaks = spec.get_peaks()[1]  # intensities
        bpc_rt.append(spec.getRT())
        bpc_int.append(peaks.max() if len(peaks) else 0)
    return bpc_rt, bpc_int


colors = [
    "coral",
    "steelblue",
    "orchid",
    "coral",
    "orchid",
    "steelblue",
    "coral",
    "orchid",
    "steelblue",
    "coral",
]
for file, color, label in zip(input_files, colors, input_labels):
    exp = oms.MSExperiment()
    oms.MzMLFile().load(file, exp)
    rt, inten = extract_bpc(exp)
    plt.plot(rt, inten, color=color, alpha=0.5, lw=1.5, label=label)

plt.legend()
plt.grid()
plt.title("BPC")
plt.xlabel("Retention Time (s)")
plt.ylabel("Intensity")
plt.show()


# %% [markdown]
# The BPC profiles show that the final portion of the chromatographic run
# contains little to no signal, indicating that no relevant compounds are being detected
# in this region. To reduce unnecessary data and focus the analysis on the informative
# part of the chromatogram, we filter the experiment by retention time and retain only
# spectra acquired between 10 and 240 seconds. The filtered BPCs allow us to verify that
# the useful chromatographic region has been preserved while removing empty sections that
# would otherwise increase processing time and data size.


# %% tags=["hide-input"]
def filter_chr(file):
    filtered = oms.MSExperiment()
    exp = oms.MSExperiment()
    oms.MzMLFile().load(file, exp)

    for spec in exp:
        rt = spec.getRT()
        if 10 <= rt <= 240:
            filtered.addSpectrum(spec)

    return filtered


filtered_exps = []
for file in input_files:
    filtered = filter_chr(file)
    filtered_exps.append(filtered)

for exp, color, label in zip(filtered_exps, colors, input_labels):
    rt, inten = extract_bpc(exp)
    plt.plot(rt, inten, color=color, alpha=0.5, lw=1.5, label=label)

plt.legend()
plt.grid()
plt.title("BPC")
plt.xlabel("Retention Time (s)")
plt.ylabel("Intensity")
plt.show()

# %% [markdown]
# Next, we load a table containing a list of **internal standards (IS)**.
# Internal standards are compounds with known properties that are often included in
# metabolomics experiments as reference signals. In this workflow, we are not using them
# for quantitative correction, but simply visualizing their behavior across samples. This
# helps us inspect their chromatographic profiles and use them as a practical reference
# when selecting or adjusting preprocessing parameters.

# %% tags=["hide-input"]
# %% internal standards
intern_standard = pd.read_csv(
    fname_intern_standard,
    sep="\t",
)
intern_standard


# %% [markdown]
# To inspect the internal standards in more detail, we extract and visualize
# their **Extracted Ion Chromatograms (EICs)**. An EIC represents the intensity of ions
# within a specific m/z range over time, restricted here to a defined retention time
# window.
#
# For each internal standard, we select its expected m/z and retention time boundaries
# from the metadata table, and then compute a signal per MS1 spectrum by summing the
# intensities of all peaks that fall within the selected m/z window. This produces a
# chromatographic trace that reflects the elution profile of that compound in each sample.
#
# Plotting these EICs across runs allows us to visually check peak shape, retention time
# consistency, and signal presence, which helps guide the selection of appropriate
# preprocessing parameters such as chromatographic width or signal-to-noise ratio.


# %% tags=["hide-input"]
def extract_eic(exp, mzmin, mzmax, rtmin, rtmax):
    rt_list = []
    intensity_list = []

    for spec in exp:
        if spec.getMSLevel() != 1:
            continue

        rt = spec.getRT()
        if not (rtmin <= rt <= rtmax):
            continue

        mz, intensity = spec.get_peaks()

        mask = (mz >= mzmin) & (mz <= mzmax)

        if np.any(mask):
            rt_list.append(rt)
            intensity_list.append(intensity[mask].sum())
        else:
            rt_list.append(rt)
            intensity_list.append(0)

    return np.array(rt_list), np.array(intensity_list)


i = 7
mzmin = intern_standard["mzmin"].tolist()[i]
mzmax = intern_standard["mzmax"].tolist()[i]
rtmin = intern_standard["rtmin"].tolist()[i]
rtmax = intern_standard["rtmax"].tolist()[i]

for exp, color, label in zip(filtered_exps, colors, input_labels):
    rt, inten = extract_eic(exp, mzmin, mzmax, rtmin, rtmax)
    plt.plot(rt, inten, color=color, alpha=0.5, lw=1.5, label=label)

plt.legend()
plt.grid()
plt.title(f"EIC for {intern_standard.iloc[i]['name']}")
plt.xlabel("Retention Time (s)")
plt.ylabel("Intensity")
plt.show()

# %% [markdown]
# The different internal standards can be inspected by modifying the
# variable `i`. From the resulting EICs, we observe that internal standards 0, 1, 3, 10,
# 11, and 18 exhibit poor peak shapes or weak signal quality. We can also see that
# well-shaped peaks have a peak width of around 3-5 seconds.

# %% [markdown]
# ## Pre-processing - peak detection
#
# We now perform **peak detection**, which is a three-step workflow that transforms raw
# MS1 data into a structured feature table.
#
# First, **Mass Trace Detection** groups signals that share a similar m/z across
# consecutive scans, reconstructing continuous ion traces over retention time. Here, the
# parameter `mass_error_ppm = 10.0` defines the allowed mass tolerance when grouping
# signals into the same trace. A relatively tight tolerance helps ensure that only signals
# with highly consistent m/z values are merged, improving trace specificity.
#
# Second, **Elution Peak Detection** identifies true chromatographic peaks within each
# mass trace by evaluating their shape in the time domain. Several parameters control this
# step: `chrom_peak_snr = 3.0` sets a minimum signal-to-noise threshold to reduce weak or
# noisy peaks, while `chrom_fwhm = 3.0` defines the expected peak width (full width at
# half maximum) used to guide peak detection. This value is chosen based on the observed
# peak widths of well-behaved internal standards, which typically show widths of
# approximately 3–5 seconds. The bounds `min_fwhm = 0.5` and `max_fwhm = 5.0` further
# restrict acceptable peak widths based on this prior chromatographic behavior.
# Additionally, `masstrace_snr_filtering = true` enables filtering of low-quality mass
# traces before peak picking, improving robustness.
#
# Finally, **Feature Finding (Metabo)** combines co-eluting mass traces into features that
# likely correspond to the same metabolite. The parameter `charge_upper_bound = 1`
# restricts detection to singly charged ions, which is typical for many metabolomics
# datasets. `chrom_fwhm = 3.0` again defines the expected chromatographic peak width used
# during grouping, while `local_rt_range = chrom_fwhm * 2` sets the retention time window
# for associating signals across traces. `isotope_filtering_model = none` disables isotope
# pattern-based grouping, keeping the workflow simpler. Setting `remove_single_traces =
# false` ensures that features composed of only one mass trace are retained, and
# `mz_scoring_by_elements = false` disables element-based scoring of isotopic consistency.
# Finally, `report_convex_hulls = true` enables the storage of chromatographic boundaries,
# which can be useful for downstream visualization and inspection.
#

# %% tags=["hide-input"]
rows = []
mass_traces_final_per_sample = []
features_per_sample = []
feature_maps = []

for s_idx, exp in enumerate(filtered_exps):

    mtd = oms.MassTraceDetection()
    params = mtd.getDefaults()

    params.setValue("mass_error_ppm", 10.0)
    mtd.setParameters(params)
    mass_traces = []
    mtd.run(exp, mass_traces, 0)

    mass_traces_split = []
    mass_traces_final = []
    epd = oms.ElutionPeakDetection()
    epd_params = epd.getDefaults()
    epd_params.setValue("width_filtering", "fixed")
    epd_params.setValue("chrom_peak_snr", 3.0)
    epd_params.setValue("chrom_fwhm", 3.0)
    epd_params.setValue("min_fwhm", 0.5)
    epd_params.setValue("max_fwhm", 7.0)
    epd_params.setValue("masstrace_snr_filtering", "true")
    epd.setParameters(epd_params)
    epd.detectPeaks(mass_traces, mass_traces_split)

    if epd.getParameters().getValue("width_filtering") == "auto":
        epd.filterByPeakWidth(mass_traces_split, mass_traces_final)
    else:
        mass_traces_final = mass_traces_split

    mass_traces_final_per_sample.append(len(mass_traces_final))

    fm = oms.FeatureMap()
    feat_chrom = []
    ffm = oms.FeatureFindingMetabo()
    ffm_params = ffm.getDefaults()
    ffm_params.setValue("charge_upper_bound", 1)
    ffm_params.setValue("chrom_fwhm", 3.0)
    ffm_params.setValue("local_rt_range", ffm_params.getValue("chrom_fwhm") * 2)
    ffm_params.setValue("isotope_filtering_model", "none")
    ffm_params.setValue(
        "remove_single_traces", "false"
    )  # set false to keep features with only one mass trace
    ffm_params.setValue("mz_scoring_by_elements", "false")
    ffm_params.setValue("report_convex_hulls", "true")
    # ffm_params.setValue("local_mz_range", 0.5)
    ffm.setParameters(ffm_params)
    ffm.run(mass_traces_final, fm, feat_chrom)

    fm.setUniqueIds()
    sample_name = os.path.basename(input_files[s_idx])
    print(sample_name)
    fm.setIdentifier(sample_name)
    fm.setPrimaryMSRunPath([sample_name.encode()])
    fm.setLoadedFilePath(input_files[s_idx])

    feature_maps.append(fm)

    peaklist = fm.get_df()

    features_per_sample.append(len(peaklist))

# %% We can check the number of peaks in our feature map objects. [markdown]
#

# %% tags=["hide-input"]
for fm in feature_maps:
    print(fm.size())

# %% [markdown]
# And the peaklist:

# %%
peaklist

# %% [markdown]
# ## Pre-processing - peak alignment and matching
#
# After feature detection, we perform **retention time alignment and feature grouping** to
# make features comparable across samples.
#
# First, we select a **reference feature map** based on the sample with the highest number
# of detected features (`fm.size()`), under the assumption that it provides the most
# complete representation of the chromatographic signal. All other runs will be aligned to
# this reference.
#
# We then apply the **Pose Clustering Map Alignment algorithm**, which corrects retention
# time shifts between samples by identifying corresponding feature patterns and estimating
# RT transformations. Each non-reference feature map is aligned individually, producing a
# transformation (`TransformationDescription`) that is then applied to adjust retention
# times using the `MapAlignmentTransformer`. This step ensures that the same compounds
# elute at comparable retention times across all runs.
#
# Once alignment is completed, we construct a **Consensus Map**, which merges features
# across samples into a unified representation. This is achieved using the
# `FeatureGroupingAlgorithmKD`, which links features based on similarity in m/z and
# aligned retention time. The parameter `warp:mz_tol = 15.0` defines the tolerated m/z
# deviation during grouping, while `link:mz_tol = 15.0` controls the maximum m/z
# difference allowed when connecting features across runs. `distance_MZ:exponent = 1.0`
# defines a linear weighting of m/z differences in the similarity scoring, and
# `warp:max_nr_conflicts = 5` limits ambiguous assignments to improve grouping robustness.
#
# The resulting consensus map contains a consolidated feature table, where each entry
# represents a putative metabolite observed across multiple samples, enabling downstream
# statistical analysis and annotation.
#
#

# %% tags=["hide-input"]
ref_index = [
    i[0]
    for i in sorted(enumerate([fm.size() for fm in feature_maps]), key=lambda x: x[1])
][-1]
aligner = oms.MapAlignmentAlgorithmPoseClustering()
aligner.setReference(feature_maps[ref_index])

for i, fm in enumerate(feature_maps):

    if i == ref_index:
        continue

    trafo = oms.TransformationDescription()

    aligner.align(fm, trafo)

    transformer = oms.MapAlignmentTransformer()
    transformer.transformRetentionTimes(fm, trafo, True)

from pyopenms import ColumnHeader

consensus_map = oms.ConsensusMap()
file_descriptions = consensus_map.getColumnHeaders()

feature_grouper = (
    oms.FeatureGroupingAlgorithmKD()
)  # FeatureGroupingAlgorithmKD in metaboigniter
grouper_params = feature_grouper.getDefaults()
grouper_params.setValue("warp:mz_tol", 15.0)
grouper_params.setValue("link:mz_tol", 15.0)
grouper_params.setValue("distance_MZ:exponent", 1.0)
grouper_params.setValue("warp:max_nr_conflicts", 5)
feature_grouper.setParameters(grouper_params)

for i, feature_map in enumerate(feature_maps):
    file_description = file_descriptions.get(i, ColumnHeader())
    file_description.filename = feature_map.getMetaValue("spectra_data")[0].decode()
    file_description.size = feature_map.size()
    file_descriptions[i] = file_description

# execute feature linking:
feature_grouper.group(feature_maps, consensus_map)
consensus_map.setUniqueIds()
consensus_map.setColumnHeaders(file_descriptions)

print(f"Total number of consensus features: {consensus_map.size()}\n\n")

# %%
peaklist = consensus_map.get_df()
sample_names = [os.path.basename(file) for file in input_files]
peaklist2 = peaklist[sample_names]

zero_counts = (peaklist2 == 0).sum(axis=1)

df_zeros = pd.DataFrame({"feature_id": peaklist2.index, "n_zeros": zero_counts})

freq_table = zero_counts.value_counts().sort_index()

df_freq = freq_table.reset_index()
df_freq.columns = ["Number_of_samples_with_0s", "n_features"]

df_freq

# %%
df = peaklist2.copy()
dict_0s = {}

for i in range(len(df)):
    n_0s = (df.iloc[i] == 0).sum()

    if n_0s not in dict_0s:
        dict_0s[n_0s] = []

    dict_0s[n_0s].append(i)

# %%
groups = list(dict_0s.keys())
samples = df.columns
result = pd.DataFrame(index=groups, columns=samples)

for j in samples:
    sample_is = df[j]
    for g in groups:
        sample_feats = sample_is.iloc[dict_0s[g]]
        n_0s = (sample_feats != 0).sum()
        result.loc[g, j] = n_0s

# %%
result

# %%
peaklist.to_csv("openms_peaklist.csv")
