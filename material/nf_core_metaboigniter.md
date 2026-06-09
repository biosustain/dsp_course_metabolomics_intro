# Metaboigniter

## Getting the data

```bash
bash  data/MTBLS8735/download.sh
python bin/reindex_mzml.py -i data/MTBLS8735/
```

## Inspect Metaboigniter arguments

```bash
>>> nextflow run nf-core/metaboigniter --help

 N E X T F L O W   ~  version 25.10.4

Launching `https://github.com/nf-core/metaboigniter` [reverent_joliot] DSL2 - revision: 55d8254760 [2.0.1]



------------------------------------------------------
                                        ,--./,-.
        ___     __   __   __   ___     /,-._.--~'
  |\ | |__  __ /  ` /  \ |__) |__         }  {
  | \| |       \__, \__/ |  \ |___     \`-._,-`-,
                                        `._,._,'
  nf-core/metaboigniter v2.0.1-g55d8254
------------------------------------------------------
Typical pipeline command:

  nextflow run nf-core/metaboigniter -profile <docker/singularity/.../institute> --input samplesheet.csv --outdir <OUTDIR>

Generic controls
  --requantification                                                                                   [boolean] If set to true, requantification will be 
                                                                                                                 performed 
  --identification                                                                                     [boolean] If set to true, identification will be 
                                                                                                                 performed. Remember to set identification 
                                                                                                                 specific parameters 
  --polarity                                                                                           [string]  Polarity of the data (accepted: positive, 
                                                                                                                 negative) [default: positive] 
  --parallel_linking                                                                                   [boolean] If set, the linking will be performed in 
                                                                                                                 parallel, see nr_partitions in linking 
  --ms2_collection_model                                                                               [string]  Set wether the MS2 collections have been done 
                                                                                                                 on all the MS1 data. If there is a separate MS2 
                                                                                                                 file, set to separate (accepted: separate, 
                                                                                                                 paired) [default: paired] 

Mapping and Identification
  --mz_tolerance_pyopenms                                                                              [number]  mz tolerance (ppm) for finding C13 
                                                                                                                 [default: 20] 
  --rt_tolerance_pyopenms                                                                              [number]  rt tolerance for finding C13 [default: 
                                                                                                                 5] 
  --ms2_use_feature_ionization                                                                         [boolean] If set, detected adduct will be used in 
                                                                                                                 identification 
  --sirius_sirius_ppm_max                                                                              [number]  Maximum allowed mass deviation in ppm for 
                                                                                                                 decomposing  masses (ppm) [default: 10] 
  --sirius_sirius_ppm_max_ms2                                                                          [number]  Maximum allowed mass deviation in ppm for 
                                                                                                                 decomposing masses in MS2 (ppm).If not 
                                                                                                                 specified, the same value as for the MS1 is 
                                                                                                                 used. [default: 10] 
  --sirius_sirius_no_recalibration                                                                     [boolean] Disable recalibration of input spectra
  --sirius_sirius_profile                                                                              [string]  Name of the configuration profile 
                                                                                                                 (accepted: default, qtof, orbitrap, fticr) 
                                                                                                                 [default: default] 
  --sirius_sirius_candidates                                                                           [integer] The number of formula candidates in the SIRIUS 
                                                                                                                 output [default: 10] 
  --sirius_sirius_candidates_per_ion                                                                   [integer] Minimum number of candidates in the output for 
                                                                                                                 each ionization. Set to force output of results 
                                                                                                                 for each possible ionization, even if not part 
                                                                                                                 of highest ranked results. [default: 1] 
  --sirius_sirius_ions_considered                                                                      [string]  the iontype/adduct of the MS/MS data. Example: 
                                                                                                                 [M+H]+, [M-H]-, [M+Cl]-, [M+Na]+, [M]+. You can 
                                                                                                                 also provide a comma separated list of 
                                                                                                                 adducts. [default: 
                                                                                                                 [M+H]+,[M+K]+,[M+Na]+,[M+H-H2O]+,[M+H-H4O2]+,[M+NH4]+,[M-H]-,[M+Cl]-,[M-H2O-H]-,[M+Br]-] 
  --sirius_sirius_db                                                                                   [string]  Search formulas in the Union of the given 
                                                                                                                 databases db-name1,db-name2,db-name3. If no 
                                                                                                                 database is given all possible molecular 
                                                                                                                 formulas will be respected (no database is 
                                                                                                                 used). Example: possible DBs: 
                                                                                                                 ALL,BIO,PUBCHEM,MESH,HMDB,KNAPSACK,CHEBI,PUBMED,KEGG,HSDB,MACONDA,METACYC,GNPS,ZINCBIO,UNDP,YMDB,PLANTCYC,NORMAN,ADDITIONAL,PUBCHEMANNOTATIONBIO,PUBCHEMANNOTATIONDRUG,PUBCHEMANNOTATIONSAFETYANDTOXIC,PUBCHEMANNOTATIONFOOD,KEGGMINE,ECOCYCMINE,YMDBMINE 
  --sirius_runpassatutto                                                                               [boolean] If set, passatutto will be run
  --sirius_fingerid_db                                                                                 [string]  Search structures in the Union of the given 
                                                                                                                 databases db-name1,db-name2,db-name3. If no 
                                                                                                                 database is given all possible molecular 
                                                                                                                 formulas will be respected (no database is 
                                                                                                                 used). Example: possible DBs: 
                                                                                                                 ALL,BIO,PUBCHEM,MESH,HMDB,KNAPSACK,CHEBI,PUBMED,KEGG,HSDB,MACONDA,METACYC,GNPS,ZINCBIO,UNDP,YMDB,PLANTCYC,NORMAN,ADDITIONAL,PUBCHEMANNOTATIONBIO,PUBCHEMANNOTATIONDRUG,PUBCHEMANNOTATIONSAFETYANDTOXIC,PUBCHEMANNOTATIONFOOD,KEGGMINE,ECOCYCMINE,YMDBMINE 
  --sirius_email                                                                                       [string]  E-mail for your SIRIUS account.
  --sirius_password                                                                                    [string]  Password for your SIRIUS account.
  --sirius_split                                                                                       [boolean] If set, SIRIUS will be run in parallel. See 
                                                                                                                 mgf_splitmgf_pyopenms parameter for 
                                                                                                                 segmentation 
  --split_consensus_parts                                                                              [integer] For running MS2 mapping in parallel set this 
                                                                                                                 higher than 1 [default: 20] 
  --run_ms2query                                                                                       [boolean] If set, MS2Query will be run
  --sirius_runfid                                                                                      [boolean] If set, FingerID will be run. This has to be 
                                                                                                                 run together with run_sirius 
  --run_sirius                                                                                         [boolean] If set SIRIUS will run

Annotation
  --algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms               [integer] Minimal possible charge [default: 1]
  --algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms               [integer] Maximal possible charge [default: 1]
  --algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms          [integer] Maximal range of charges for a single analyte, 
                                                                                                                 i.e. observing q1=[5,6,7] implies span=3. 
                                                                                                                 Setting this to 1 will only find adduct 
                                                                                                                 variants of the same charge [default: 
                                                                                                                 1] 
  --algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms                    [string]  Try different values of charge for each feature 
                                                                                                                 according to the above settings ('heuristic' 
                                                                                                                 [does not test all charges, just the likely 
                                                                                                                 ones] or 'all' ), or leave feature charge 
                                                                                                                 untouched ('feature'). (accepted: feature, 
                                                                                                                 heuristic, all) [default: feature] 
  --algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms       [number]  Maximum allowed RT difference between any two 
                                                                                                                 features if their relation shall be 
                                                                                                                 determined [default: 1] 
  --algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms [number]  Maximum allowed RT difference between between 
                                                                                                                 two co-features, after adduct shifts have been 
                                                                                                                 accounted for (if you do not have any adduct 
                                                                                                                 shifts, this value should be equal to 
                                                                                                                 'retention_max_diff', otherwise it should be 
                                                                                                                 smaller!) [default: 1] 
  --algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms            [number]  Maximum allowed mass tolerance per feature. 
                                                                                                                 Defines a symmetric tolerance window around the 
                                                                                                                 feature. When looking at possible feature 
                                                                                                                 pairs, the allowed feature-wise errors are 
                                                                                                                 combined for consideration of possible adduct 
                                                                                                                 shifts. For ppm tolerances, each window is 
                                                                                                                 based on the respective observed feature mz 
                                                                                                                 (instead of putative experimental mzs causing 
                                                                                                                 the observed one)! [default: 5] 
  --algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms                     [string]  Unit of the 'max_difference' parameter 
                                                                                                                 (accepted: Da, ppm) [default: ppm] 
  --algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms             [integer] Maximal number of neutral adducts(q=0) allowed. 
                                                                                                                 Add them in the 'potential_adducts' 
                                                                                                                 section! [default: 1] 
  --algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms       [boolean] Prune the considered adduct transitions by 
                                                                                                                 transition probabilities. [default: 
                                                                                                                 true] 
  --algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms       [integer] Limits allowed adduct compositions and changes 
                                                                                                                 between compositions in the underlying graph 
                                                                                                                 optimization problem by introducing a 
                                                                                                                 probability-based threshold: the minority bound 
                                                                                                                 sets the maximum count of the least probable 
                                                                                                                 adduct (according to 'potential_adducts' param) 
                                                                                                                 within a charge variant with maximum charge 
                                                                                                                 only containing the most likely adduct 
                                                                                                                 otherwise. E.g., for 'charge_max' 4 and 
                                                                                                                 'max_minority_bound' 2 with most probable 
                                                                                                                 adduct being H+ and least probable adduct being 
                                                                                                                 Na+, this will allow adduct compositions of 
                                                                                                                 '2(H+),2(Na+)' but not of '1(H+),3(Na+)'. 
                                                                                                                 Further, adduct compositions/changes less 
                                                                                                                 likely than '2(H+),2(Na+)' will be discarded as 
                                                                                                                 well. [default: 1] 
  --algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms           [number]  Minimum overlap of the convex hull' RT 
                                                                                                                 intersection measured against the union from 
                                                                                                                 two features (if CHs are given) [default: 
                                                                                                                 0.66] 
  --algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms         [boolean] Enable the intensity filter, which will only 
                                                                                                                 allow edges between two equally charged 
                                                                                                                 features if the intensity of the feature with 
                                                                                                                 less likely adducts is smaller than that of the 
                                                                                                                 other feature. It is not used for features of 
                                                                                                                 different charge. 
  --adducts_pos                                                                                        [string]  possible positive adducts for adduct detection 
                                                                                                                 in the format of adduct:charge:probablity 
                                                                                                                 [default: H:+:0.6 Na:+:0.1 NH4:+:0.1 
                                                                                                                 H-1O-1:+:0.1 H-3O-2:+:0.1] 
  --adducts_neg                                                                                        [string]  possible negative adducts for adduct detection 
                                                                                                                 in the format of adduct:charge:probablity 
                                                                                                                 [default: H-1:-:0.8 H-3O-1:-:0.2] 

Alignment and Linking
  --algorithm_max_num_peaks_considered_mapalignerposeclustering_openms                                 [integer] The maximal number of peaks/features to be 
                                                                                                                 considered per map. To use all, set to 
                                                                                                                 '-1'. [default: 1000] 
  --algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms                        [number]  Maximum of m/z deviation of corresponding 
                                                                                                                 elements in different maps.  This condition 
                                                                                                                 applies to the pairs considered in hashing. 
                                                                                                                 [default: 0.5] 
  --algorithm_superimposer_num_used_points_mapalignerposeclustering_openms                             [integer] Maximum number of elements considered in each 
                                                                                                                 map (selected by intensity).  Use this to 
                                                                                                                 reduce the running time and to disregard weak 
                                                                                                                 signals during alignment.  For using all 
                                                                                                                 points, set this to -1. [default: 2000] 
  --algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms                                 [boolean] false [default]: pairing requires equal charge 
                                                                                                                 state (or at least one unknown charge '0'); 
                                                                                                                 true: Pairing irrespective of charge 
                                                                                                                 state 
  --algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms                    [number]  Never pair features with a larger RT distance 
                                                                                                                 (in seconds). [default: 100.0] 
  --algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms                    [number]  Never pair features with larger m/z distance 
                                                                                                                 (unit defined by 'unit') [default: 0.3] 
  --algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms                              [string]  Unit of the 'max_difference' parameter 
                                                                                                                 (accepted: Da, ppm) [default: Da] 
  --algorithm_mz_unit_featurelinkerunlabeledkd_openms                                                  [string]  Unit of m/z tolerance (accepted: ppm, Da) 
                                                                                                                 [default: ppm] 
  --algorithm_nr_partitions_featurelinkerunlabeledkd_openms                                            [integer] Number of partitions in m/z space [default: 
                                                                                                                 100] 
  --algorithm_warp_enabled_featurelinkerunlabeledkd_openms                                             [boolean] Whether or not to internally warp feature RTs 
                                                                                                                 using LOWESS transformation before linking 
                                                                                                                 (reported RTs in results will always be the 
                                                                                                                 original RTs) [default: true] 
  --algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms                                              [number]  Width of RT tolerance window (sec) 
                                                                                                                 [default: 100.0] 
  --algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms                                              [number]  m/z tolerance (in ppm or Da) [default: 
                                                                                                                 5.0] 
  --algorithm_link_rt_tol_featurelinkerunlabeledkd_openms                                              [number]  Width of RT tolerance window (sec) 
                                                                                                                 [default: 30] 
  --algorithm_link_mz_tol_featurelinkerunlabeledkd_openms                                              [number]  m/z tolerance (in ppm or Da) [default: 
                                                                                                                 10] 
  --algorithm_link_charge_merging_featurelinkerunlabeledkd_openms                                      [string]  whether to disallow charge mismatches 
                                                                                                                 (Identical), allow to link charge zero (i.e., 
                                                                                                                 unknown charge state) with every charge state, 
                                                                                                                 or disregard charges (Any). (accepted: 
                                                                                                                 Identical, With_charge_zero, Any) [default: 
                                                                                                                 With_charge_zero] 
  --algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms                                      [string]  whether to only allow the same adduct for 
                                                                                                                 linking (Identical), also allow linking 
                                                                                                                 features with adduct-free ones, or disregard 
                                                                                                                 adducts (Any). (accepted: Identical, 
                                                                                                                 With_unknown_adducts, Any) [default: Any] 

Re-Quantification
  --extract_mz_window_featurefindermetaboident_openms                                                  [number]  m/z window size for chromatogram extraction 
                                                                                                                 (unit: ppm if 1 or greater, else Da/Th) 
  --extract_n_isotopes_featurefindermetaboident_openms                                                 [integer] Number of isotopes to include in each peptide 
                                                                                                                 assay. 
  --detect_peak_width_featurefindermetaboident_openms                                                  [number]  Expected elution peak width in seconds, for 
                                                                                                                 smoothing (Gauss filter). Also determines the 
                                                                                                                 RT extration window, unless set explicitly via 
                                                                                                                 'extract:rt_window'. 
  --model_type_featurefindermetaboident_openms                                                         [string]  Type of elution model to fit to features 
                                                                                                                 (accepted: symmetric, asymmetric, none) 
                                                                                                                 [default: symmetric] 
  --emgscoring_max_iteration_featurefindermetaboident_openms                                           [integer] Maximum number of iterations for EMG 
                                                                                                                 fitting. 
  --emgscoring_init_mom_featurefindermetaboident_openms                                                [boolean] Alternative initial parameters for fitting 
                                                                                                                 through method of moments. 

Quantification
  --algorithm_signal_to_noise_peakpickerhires_openms                                                   [number]  Minimal signal-to-noise ratio for a peak to be 
                                                                                                                 picked (0.0 disables SNT estimation!) 
  --algorithm_common_noise_threshold_int_featurefindermetabo_openms                                    [number]  Intensity threshold below which peaks are 
                                                                                                                 regarded as noise. [default: 10] 
  --algorithm_common_chrom_peak_snr_featurefindermetabo_openms                                         [number]  Minimum signal-to-noise a mass trace should 
                                                                                                                 have. [default: 3] 
  --algorithm_common_chrom_fwhm_featurefindermetabo_openms                                             [number]  Expected chromatographic peak width (in 
                                                                                                                 seconds). [default: 5] 
  --algorithm_mtd_mass_error_ppm_featurefindermetabo_openms                                            [number]  Allowed mass deviation (in ppm). [default: 
                                                                                                                 20] 
  --algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms                                          [boolean] Enables dynamic re-estimation of m/z variance 
                                                                                                                 during mass trace collection stage. 
                                                                                                                 [default: true] 
  --algorithm_mtd_quant_method_featurefindermetabo_openms                                              [string]  Method of quantification for mass traces. For 
                                                                                                                 LC data 'area' is recommended, 'median' for 
                                                                                                                 direct injection data. 'max_height' simply uses 
                                                                                                                 the most intense peak in the trace. 
                                                                                                                 (accepted: area, median, max_height) [default: 
                                                                                                                 area] 
  --algorithm_epd_enabled_featurefindermetabo_openms                                                   [boolean] Enable splitting of isobaric mass traces by 
                                                                                                                 chromatographic peak detection. Disable for 
                                                                                                                 direct injection. [default: true] 
  --algorithm_epd_width_filtering_featurefindermetabo_openms                                           [string]  Enable filtering of unlikely peak widths. The 
                                                                                                                 fixed setting filters out mass traces outside 
                                                                                                                 the [min_fwhm, max_fwhm] interval (set 
                                                                                                                 parameters accordingly!). The auto setting 
                                                                                                                 filters with the 5 and 95% quantiles of the 
                                                                                                                 peak width distribution. (accepted: off, 
                                                                                                                 fixed, auto) [default: fixed] 
  --algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms                                       [boolean] Require sufficient overlap in RT while 
                                                                                                                 assembling mass traces. Disable for direct 
                                                                                                                 injection data.. [default: true] 
  --algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms                                   [string]  Remove/score candidate assemblies based on 
                                                                                                                 isotope intensities. SVM isotope models for 
                                                                                                                 metabolites were trained with either 2% or 5% 
                                                                                                                 RMS error. For peptides, an averagine cosine 
                                                                                                                 scoring is used. Select the appropriate noise 
                                                                                                                 model according to the quality of measurement 
                                                                                                                 or MS device. (accepted: metabolites (2% 
                                                                                                                 RMS), ...) [default: metabolites (5% RMS)] 
  --algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms                                            [boolean] Use the 13C isotope peak position (~1.003355 
                                                                                                                 Da) as the expected shift in m/z for isotope 
                                                                                                                 mass traces (highly recommended for 
                                                                                                                 lipidomics!). Disable for general metabolites 
                                                                                                                 (as described in Kenar et al. 2014, 
                                                                                                                 MCP.). 

Input/output options
  --input                                                                                              [string]  Path to comma-separated file containing 
                                                                                                                 information about the samples in the 
                                                                                                                 experiment. 
  --outdir                                                                                             [string]  The output directory where the results will be 
                                                                                                                 saved. You have to use absolute paths to 
                                                                                                                 storage on Cloud infrastructure. 
  --email                                                                                              [string]  Email address for completion summary.
  --multiqc_title                                                                                      [string]  MultiQC report title. Printed as page header, 
                                                                                                                 used for filename if not otherwise 
                                                                                                                 specified. 

Generic options
  --multiqc_methods_description                                                                        [string]  Custom MultiQC yaml file containing HTML 
                                                                                                                 including a methods description. 

 !! Hiding 150 params, use --validationShowHiddenParams to show them !!
------------------------------------------------------
If you use nf-core/metaboigniter for your analysis please cite:

* The pipeline
  

* The nf-core framework
  https://doi.org/10.1038/s41587-020-0439-x

* Software dependencies
  https://github.com/nf-core/metaboigniter/blob/master/CITATIONS.md
------------------------------------------------------

```

## Run Metaboigniter

We will run the latest version `2.0.1` using an example dataset.


- uses `nextflow.config` and the following parameters:

```bash
nextflow run nf-core/metaboigniter -profile docker,arm -r 2.0.1
```


more verbosely this run without setting a config file:

```bash
nextflow run nf-core/metaboigniter -profile docker,arm --outdir results_MTBLS8735 \
--input data/MTBLS8735/samplesheet.csv \
--identification -r 2.0.1 -resume \
--max_cpus 4 --max_memory '6.GB' --max_time '6.h' 
```

## Troubleshooting

### Ensure mzML files are correctly indexed

Metaboigniter does not reindex mzML files itself, but relies on using an indexed 
version of the mzML files. If you encounter index access errors us `pyopenms` 
to reindex the mzML files, see the script at 
[`bin/reindex_mzml.py`](../bin/reindex_mzml.py) 
for an example of how to do this.

```bash
pip install pyopenms
# python -m pip install pyopenms
python bin/reindex_mzml.py -h
python bin/reindex_mzml.py --input_dir data/
```

### Corrupt files

When downloading the files, it is possible that error occur. Try to redownload any file that
fails to be processed.

### MS2Query downloads

```bash
# downloaded into your work folder by a process
# e.g. ls -lh work/5f/c28db2c487c595610fa3108e5bd8cb/downloads
-rw-rw-rw- 1 root root 483M Jun  9 11:27 library_GNPS_15_12_2021_ms2ds_embeddings.pickle
-rw-rw-rw- 1 root root 722M Jun  9 11:27 library_GNPS_15_12_2021_s2v_embeddings.pickle
-rw-rw-rw- 1 root root  62M Jun  9 11:27 ms2ds_model_GNPS_15_12_2021.hdf5
-rw-rw-rw- 1 root root 327M Jun  9 11:27 ms2query_library.sqlite
-rw-rw-rw- 1 root root 574K Jun  9 11:27 ms2query_random_forest_model.onnx
-rw-rw-rw- 1 root root 3.9M Jun  9 11:27 spec2vec_model_GNPS_15_12_2021.model
-rw-rw-rw- 1 root root 133M Jun  9 11:28 spec2vec_model_GNPS_15_12_2021.model.syn1neg.npy
-rw-rw-rw- 1 root root 133M Jun  9 11:28 spec2vec_model_GNPS_15_12_2021.model.wv.vectors.npy
```

## Example output of a local run


<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="application/xml+xhtml; charset=UTF-8"/>
<title>stdin</title>
</head>
<body>
<pre>

<span style="font-weight:bold;"></span><span style="font-weight:bold;color:#000000;"></span><span style="font-weight:bold;color:#000000;background-color:#00d7af;"> N E X T F L O W </span>  ~  version 25.10.4

Launching<span style="color:purple;"> `https://github.com/nf-core/metaboigniter` </span>[<span style="font-weight:bold;color:teal;">fervent_spence</span>] DSL2 - <span style="color:teal;">revision: 55d8254760 [2.0.1]</span>

<span style="color:olive;">WARN: Access to undefined parameter `monochromeLogs` -- Initialise it to a default value eg. `params.monochromeLogs = some_value`</span>
                                        
<span style="color:purple;">  nf-core/metaboigniter v2.0.1-g55d8254</span>

<span style="font-weight:bold;">Core Nextflow options</span>
  <span style="color:blue;">revision                                                                                          : </span><span style="color:green;">2.0.1</span>
  <span style="color:blue;">runName                                                                                           : </span><span style="color:green;">fervent_spence</span>
  <span style="color:blue;">containerEngine                                                                                   : </span><span style="color:green;">docker</span>
  <span style="color:blue;">launchDir                                                                                         : </span><span style="color:green;">/Users/heweb/Documents/repos/dsp_course_metabolomics_intro</span>
  <span style="color:blue;">workDir                                                                                           : </span><span style="color:green;">/Users/heweb/Documents/repos/dsp_course_metabolomics_intro/work</span>
  <span style="color:blue;">projectDir                                                                                        : </span><span style="color:green;">/Users/heweb/.nextflow/assets/nf-core/metaboigniter</span>
  <span style="color:blue;">userName                                                                                          : </span><span style="color:green;">heweb</span>
  <span style="color:blue;">profile                                                                                           : </span><span style="color:green;">docker,arm</span>
  <span style="color:blue;">configFiles                                                                                       : </span><span style="color:green;"></span>

<span style="font-weight:bold;">Generic controls</span>
  <span style="color:blue;">identification                                                                                    : </span><span style="color:green;">true</span>

<span style="font-weight:bold;">Mapping and Identification</span>
  <span style="color:blue;">mz_tolerance_pyopenms                                                                             : </span><span style="color:green;">20.0</span>
  <span style="color:blue;">rt_tolerance_pyopenms                                                                             : </span><span style="color:green;">5.0</span>
  <span style="color:blue;">sirius_sirius_ppm_max                                                                             : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">sirius_sirius_ppm_max_ms2                                                                         : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">run_ms2query                                                                                      : </span><span style="color:green;">true</span>
  <span style="color:blue;">run_sirius                                                                                        : </span><span style="color:green;">true</span>

<span style="font-weight:bold;">Annotation</span>
  <span style="color:blue;">algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms      : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms: </span><span style="color:green;">1.0</span>

<span style="font-weight:bold;">Alignment and Linking</span>
  <span style="color:blue;">algorithm_superimposer_scaling_bucket_size_mapalignerposeclustering_openms                        : </span><span style="color:green;">0.0050</span>
  <span style="color:blue;">algorithm_superimposer_shift_bucket_size_mapalignerposeclustering_openms                          : </span><span style="color:green;">3.0</span>
  <span style="color:blue;">algorithm_superimposer_max_shift_mapalignerposeclustering_openms                                  : </span><span style="color:green;">1000.0</span>
  <span style="color:blue;">algorithm_superimposer_max_scaling_mapalignerposeclustering_openms                                : </span><span style="color:green;">2.0</span>
  <span style="color:blue;">algorithm_pairfinder_second_nearest_gap_mapalignerposeclustering_openms                           : </span><span style="color:green;">2.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_rt_exponent_mapalignerposeclustering_openms                         : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_rt_weight_mapalignerposeclustering_openms                           : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_mz_exponent_mapalignerposeclustering_openms                         : </span><span style="color:green;">2.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_mz_weight_mapalignerposeclustering_openms                           : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_intensity_exponent_mapalignerposeclustering_openms                  : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_pairfinder_distance_intensity_weight_mapalignerposeclustering_openms                    : </span><span style="color:green;">0.0</span>
  <span style="color:blue;">algorithm_link_rt_tol_featurelinkerunlabeledkd_openms                                             : </span><span style="color:green;">30.0</span>
  <span style="color:blue;">algorithm_link_mz_tol_featurelinkerunlabeledkd_openms                                             : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">algorithm_distance_rt_exponent_featurelinkerunlabeledkd_openms                                    : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_distance_rt_weight_featurelinkerunlabeledkd_openms                                      : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_distance_mz_exponent_featurelinkerunlabeledkd_openms                                    : </span><span style="color:green;">2.0</span>
  <span style="color:blue;">algorithm_distance_mz_weight_featurelinkerunlabeledkd_openms                                      : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_distance_intensity_exponent_featurelinkerunlabeledkd_openms                             : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_distance_intensity_weight_featurelinkerunlabeledkd_openms                               : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_lowess_delta_featurelinkerunlabeledkd_openms                                            : </span><span style="color:green;">-1.0</span>
  <span style="color:blue;">model_linear_x_datum_min_maprttransformer_openms                                                  : </span><span style="color:green;">1.0E-15</span>
  <span style="color:blue;">model_linear_x_datum_max_maprttransformer_openms                                                  : </span><span style="color:green;">1.0E+15</span>
  <span style="color:blue;">model_linear_y_datum_min_maprttransformer_openms                                                  : </span><span style="color:green;">1.0E-15</span>
  <span style="color:blue;">model_linear_y_datum_max_maprttransformer_openms                                                  : </span><span style="color:green;">1.0E+15</span>
  <span style="color:blue;">model_b_spline_wavelength_maprttransformer_openms                                                 : </span><span style="color:green;">0.0</span>
  <span style="color:blue;">model_b_spline_num_nodes_maprttransformer_openms                                                  : </span><span style="color:green;">5</span>
  <span style="color:blue;">model_b_spline_boundary_condition_maprttransformer_openms                                         : </span><span style="color:green;">2</span>
  <span style="color:blue;">model_lowess_span_maprttransformer_openms                                                         : </span><span style="color:green;">0.666666666666667</span>
  <span style="color:blue;">model_lowess_num_iterations_maprttransformer_openms                                               : </span><span style="color:green;">3</span>
  <span style="color:blue;">model_lowess_delta_maprttransformer_openms                                                        : </span><span style="color:green;">-1.0</span>

<span style="font-weight:bold;">Re-Quantification</span>
  <span style="color:blue;">extract_mz_window_featurefindermetaboident_openms                                                 : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">extract_rt_window_featurefindermetaboident_openms                                                 : </span><span style="color:green;">0.0</span>
  <span style="color:blue;">extract_n_isotopes_featurefindermetaboident_openms                                                : </span><span style="color:green;">2</span>
  <span style="color:blue;">extract_isotope_pmin_featurefindermetaboident_openms                                              : </span><span style="color:green;">0.0</span>
  <span style="color:blue;">detect_peak_width_featurefindermetaboident_openms                                                 : </span><span style="color:green;">60.0</span>
  <span style="color:blue;">detect_min_peak_width_featurefindermetaboident_openms                                             : </span><span style="color:green;">0.2</span>
  <span style="color:blue;">detect_signal_to_noise_featurefindermetaboident_openms                                            : </span><span style="color:green;">0.8</span>
  <span style="color:blue;">model_add_zeros_featurefindermetaboident_openms                                                   : </span><span style="color:green;">0.2</span>
  <span style="color:blue;">model_check_min_area_featurefindermetaboident_openms                                              : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">model_check_boundaries_featurefindermetaboident_openms                                            : </span><span style="color:green;">0.5</span>
  <span style="color:blue;">model_check_width_featurefindermetaboident_openms                                                 : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">model_check_asymmetry_featurefindermetaboident_openms                                             : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">emgscoring_max_iteration_featurefindermetaboident_openms                                          : </span><span style="color:green;">100</span>

<span style="font-weight:bold;">Quantification</span>
  <span style="color:blue;">algorithm_signal_to_noise_peakpickerhires_openms                                                  : </span><span style="color:green;">0.0</span>
  <span style="color:blue;">algorithm_spacing_difference_gap_peakpickerhires_openms                                           : </span><span style="color:green;">4.0</span>
  <span style="color:blue;">algorithm_spacing_difference_peakpickerhires_openms                                               : </span><span style="color:green;">1.5</span>
  <span style="color:blue;">algorithm_missing_peakpickerhires_openms                                                          : </span><span style="color:green;">1</span>
  <span style="color:blue;">algorithm_signaltonoise_max_intensity_peakpickerhires_openms                                      : </span><span style="color:green;">-1</span>
  <span style="color:blue;">algorithm_signaltonoise_auto_max_stdev_factor_peakpickerhires_openms                              : </span><span style="color:green;">3.0</span>
  <span style="color:blue;">algorithm_signaltonoise_auto_max_percentile_peakpickerhires_openms                                : </span><span style="color:green;">95</span>
  <span style="color:blue;">algorithm_signaltonoise_auto_mode_peakpickerhires_openms                                          : </span><span style="color:green;">0</span>
  <span style="color:blue;">algorithm_signaltonoise_win_len_peakpickerhires_openms                                            : </span><span style="color:green;">200.0</span>
  <span style="color:blue;">algorithm_signaltonoise_bin_count_peakpickerhires_openms                                          : </span><span style="color:green;">30</span>
  <span style="color:blue;">algorithm_signaltonoise_min_required_elements_peakpickerhires_openms                              : </span><span style="color:green;">10</span>
  <span style="color:blue;">algorithm_signaltonoise_noise_for_empty_window_peakpickerhires_openms                             : </span><span style="color:green;">1.0E+20</span>
  <span style="color:blue;">algorithm_common_noise_threshold_int_featurefindermetabo_openms                                   : </span><span style="color:green;">10.0</span>
  <span style="color:blue;">algorithm_common_chrom_peak_snr_featurefindermetabo_openms                                        : </span><span style="color:green;">3.0</span>
  <span style="color:blue;">algorithm_common_chrom_fwhm_featurefindermetabo_openms                                            : </span><span style="color:green;">5.0</span>
  <span style="color:blue;">algorithm_mtd_mass_error_ppm_featurefindermetabo_openms                                           : </span><span style="color:green;">20.0</span>
  <span style="color:blue;">algorithm_mtd_min_trace_length_featurefindermetabo_openms                                         : </span><span style="color:green;">5.0</span>
  <span style="color:blue;">algorithm_mtd_max_trace_length_featurefindermetabo_openms                                         : </span><span style="color:green;">-1.0</span>
  <span style="color:blue;">algorithm_epd_min_fwhm_featurefindermetabo_openms                                                 : </span><span style="color:green;">1.0</span>
  <span style="color:blue;">algorithm_epd_max_fwhm_featurefindermetabo_openms                                                 : </span><span style="color:green;">60.0</span>
  <span style="color:blue;">algorithm_ffm_local_rt_range_featurefindermetabo_openms                                           : </span><span style="color:green;">10.0</span>

<span style="font-weight:bold;">Input/output options</span>
  <span style="color:blue;">input                                                                                             : </span><span style="color:green;">data/samplesheet.csv</span>
  <span style="color:blue;">outdir                                                                                            : </span><span style="color:green;">results</span>

<span style="font-weight:bold;">Institutional config options</span>
  <span style="color:blue;">config_profile_name                                                                               : </span><span style="color:green;">Metabonaut example dataset</span>
  <span style="color:blue;">config_profile_description                                                                        : </span><span style="color:green;">Example data from Metabonaut.</span>

<span style="font-weight:bold;">Max job request options</span>
  <span style="color:blue;">max_cpus                                                                                          : </span><span style="color:green;">8</span>
  <span style="color:blue;">max_memory                                                                                        : </span><span style="color:green;">14.GB</span>
  <span style="color:blue;">max_time                                                                                          : </span><span style="color:green;">6.h</span>

Only displaying parameters that differ from the pipeline defaults
------------------------------------------------------
If you use nf-core/metaboigniter for your analysis please cite:

- The pipeline
- The nf-core framework
  https://doi.org/10.1038/s41587-020-0439-x
- Software dependencies
  https://github.com/nf-core/metaboigniter/blob/master/CITATIONS.md
------------------------------------------------------
<span style="color:olive;">WARN: No Sirius user account information found. Please enter `--sirius_email` and `sirius_password`.</span>

[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_FEATUREFINDERMETABO                      -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_MAPALIGNERPOSECLUSTERING                 -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_MAPRTTRANSFORMER                         -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:ANNOTATION:OPENMS_METABOLITEADDUCTDECHARGER                    -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:ANNOTATION:PYOPENMS_C13DETECTION                               -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:LINKER:OPENMS_FEATURELINKERUNLABELEDKD                         -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_MSMAPPING                              -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:OPENMS_FILEFILTER                               -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_SPLITCONSENSUS                         -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_GENERATESEARCHPARAMS                   -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_CONCTSV_UNMAPPED                       -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:GENERAL_MERGEMSFILE                             -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:GENERAL_MERGEMGFFILE                            -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:SIRIUS_SEARCH                      -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:PYOPENMS_CONCTSVSIRIUS             -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:PYOPENMS_CONCTSVFINGERID           -
[<span style="color:blue;">-        </span>] NFC…R:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_MODELDOWNLOADER:MS2QUERY_DOWNLOADMODEL -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_CHECKMODELFILES         -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_SEARCH                  -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:PYOPENMS_CONCTSVMS2QUERY         -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:PYOPENMS_EXPORTIDENTIFICATION                                  -
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:MULTIQC                                                        -
<span style="color:olive;">WARN: The operator `first` is useless when applied to a value channel which returns a single value by definition</span>
<span style="color:olive;">WARN: Input `tuple` must define at least two elements -- Check process `NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_SEARCH`</span>

executor &gt;  local (1)
[<span style="color:blue;">81/f8c70e</span>] NFCORE_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_FEATUREFINDERMETABO<span style="color:olive;"> (MS_D_POS)</span>           [<span style="color:green;">100%</span>] 10 of 10<span style="color:green;"> ✔</span>
[<span style="color:blue;">31/91ac9e</span>] NFC…E_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_MAPALIGNERPOSECLUSTERING<span style="color:olive;"> (Multiple files)</span> [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">04/074ef6</span>] NFCORE_METABOIGNITER:METABOIGNITER:QUANTIFICATION:OPENMS_MAPRTTRANSFORMER<span style="color:olive;"> (MS_B_POS)</span>              [<span style="color:green;">100%</span>] 10 of 10<span style="color:green;"> ✔</span>
[<span style="color:blue;">2c/12d19b</span>] NFCORE_METABOIGNITER:METABOIGNITER:ANNOTATION:OPENMS_METABOLITEADDUCTDECHARGER<span style="color:olive;"> (MS_B_POS)</span>         [<span style="color:green;">100%</span>] 10 of 10<span style="color:green;"> ✔</span>
[<span style="color:blue;">c0/4e586a</span>] NFCORE_METABOIGNITER:METABOIGNITER:ANNOTATION:PYOPENMS_C13DETECTION<span style="color:olive;"> (MS_QC_POOL_4_POS)</span>            [<span style="color:green;">100%</span>] 10 of 10<span style="color:green;"> ✔</span>
[<span style="color:blue;">e2/abd21a</span>] NFCORE_METABOIGNITER:METABOIGNITER:LINKER:OPENMS_FEATURELINKERUNLABELEDKD<span style="color:olive;"> (Linked_data)</span>           [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">82/8de1f5</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_MSMAPPING<span style="color:olive;"> (Linked_data)</span>                [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">e5/29283a</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:OPENMS_FILEFILTER<span style="color:olive;"> (Linked_data)</span>                 [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">e9/d8a5d7</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_SPLITCONSENSUS<span style="color:olive;"> (Linked_data)</span>           [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">b8/913b64</span>] NFC…_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_GENERATESEARCHPARAMS<span style="color:olive;"> (Linked_data_part9)</span> [<span style="color:green;">100%</span>] 20 of 20<span style="color:green;"> ✔</span>
[<span style="color:blue;">9d/bf7756</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:PYOPENMS_CONCTSV_UNMAPPED<span style="color:olive;"> (MSMS_2_A_CE20_POS)</span>   [<span style="color:green;">100%</span>] 9 of 9<span style="color:green;"> ✔</span>
[<span style="color:blue;">58/a6b59f</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:GENERAL_MERGEMSFILE<span style="color:olive;"> (Linked_data)</span>               [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">61/30fee6</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:GENERAL_MERGEMGFFILE<span style="color:olive;"> (Linked_data)</span>              [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">54/2f5ab5</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:SIRIUS_SEARCH<span style="color:olive;"> (Linked_data)</span>        [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">8e/5be8f1</span>] NFC…IGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:PYOPENMS_CONCTSVSIRIUS<span style="color:olive;"> (sirius_Linked_data)</span> [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">-        </span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:SIRIUSMAPPED:PYOPENMS_CONCTSVFINGERID           -
[<span style="color:blue;">85/7f0e9f</span>] NFC…TION:MS2QUERYMAPPED:MS2QUERY_MODELDOWNLOADER:MS2QUERY_DOWNLOADMODEL<span style="color:olive;"> (Downloading model files)</span> [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">ea/59bd7e</span>] NFC…IGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_CHECKMODELFILES<span style="color:olive;"> (checking files)</span> [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">97/2b1f52</span>] NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_SEARCH<span style="color:olive;"> (Linked_data)</span>    [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">a1/66c3c6</span>] NFC…R:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:PYOPENMS_CONCTSVMS2QUERY<span style="color:olive;"> (ms2query_Linked_data)</span> [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">fe/fec7ef</span>] NFCORE_METABOIGNITER:METABOIGNITER:PYOPENMS_EXPORTIDENTIFICATION<span style="color:olive;"> (Linked_data)</span>                    [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
[<span style="color:blue;">64/c2f478</span>] NFCORE_METABOIGNITER:METABOIGNITER:MULTIQC                                                        [<span style="color:green;">100%</span>] 1 of 1<span style="color:green;"> ✔</span>
-<span style="color:purple;">[nf-core/metaboigniter]</span><span style="color:green;"> Pipeline completed successfully</span>-
<span style="color:olive;">WARN: The operator `first` is useless when applied to a value channel which returns a single value by definition</span>
<span style="color:olive;">WARN: Input `tuple` must define at least two elements -- Check process `NFCORE_METABOIGNITER:METABOIGNITER:IDENTIFICATION:MS2QUERYMAPPED:MS2QUERY_SEARCH`</span>

</pre>
</body>
</html>
