# CutA study

Untargeted metabolomics of `Synechococcus elongatus sp. PCC 7942 WT` 
or delta CutA in exponential or stationary phase. 

5 or 10 uL injections on LC/MS column (10uL will be used).

## Article


Wagner BC, Steuer-Lodd K, Geibel C, Stadelmann A, Rapp J, Link H, Schramm T, Boodaghian N,
Hsiao A, Nussbaum E, Grenzendorfer HP, Albrecht R, Hartmann MD, Forchhammer K, Selim KA,
Hughes CC, Petras D. Native metabolomics identifies pteridines as CutA ligands and
modulators of copper binding. Proc Natl Acad Sci U S A. 2025 Dec 2;122(48):e2509468122.
doi: 10.1073/pnas.2509468122. Epub 2025 Nov 25. PMID: 41289401; PMCID: PMC12685090.

[[LINK]](https://pmc.ncbi.nlm.nih.gov/articles/PMC12685090/)

## Injection Order

See csv file extracted from `20230710_V28_9_SelWtvsMutant.sld` in
`20230710_V28_9_SelWtvsMutant.csv`.


## Files

- Zenodo: https://zenodo.org/records/10041900
- Massive: https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000092427

```
bash download.sh
mkdir -p mzML_10micro
ThermoRawFileParser -d raw_data -o mzML_10micro -m 0 -f 2
```
 
