# %% [markdown]
# # Enrichment analysis
#
# Reference:
# - module documetentation
# - api-example for enrichment analysis

# %% tags=["hide-input"]
from collections import defaultdict

import acore
import pandas as pd


def parse_compound_pathway_mapping(raw_mapping: str) -> dict[str, list[str]]:
    """Parse tab-delimited KEGG-style compound/pathway mappings into a dictionary."""
    compound_to_pathways: defaultdict[str, list[str]] = defaultdict(list)

    for line in raw_mapping.strip().strip("'").splitlines():
        compound_id, pathway_id = line.split("\t", maxsplit=1)
        compound_to_pathways[compound_id].append(pathway_id)

    return dict(compound_to_pathways)


compounds = {}


# %% [markdown]
# ## List relevant files
# - ms2query based annotations (contains smiles and inchikeys)
# - ancova results (contains feature IDs and p-values)


# %% tags=["parameters"]
fname_ms2query = "results_prepared/output_ms2query_Linked_data.tsv"
fname_ancova = "results_prepared/ancova_results.csv"
fname_pathways_map = "results_prepared/pathways_map.tsv"
fname_inchikey_to_kegg = "results_prepared/inchikey_to_kegg.csv"
fname_annotations = "results_prepared/link_compound_pathway.tsv"

# %% [markdown]
# ## Kegg annotations
# Can be downloaded from KEGG:
# - https://rest.kegg.jp/link/compound/pathway

# %% tags=["hide-input"]
annotations = pd.read_csv(
    fname_annotations,
    sep="\t",
    header=None,
    names=[
        "pathway_id",
        "compound_id",
    ],
)
_ = annotations.insert(1, "Source", "KEGG")
annotations["pathway_id"] = (
    annotations["pathway_id"].str.strip().str.replace("path:", "")
)
annotations["compound_id"] = (
    annotations["compound_id"].str.strip().str.replace("cpd:", "")
)
annotations.set_index("compound_id", inplace=True)
annotations

# %% [markdown]
# ## Pathway mapping: fetch names

# %%
pathways_map = pd.read_csv(
    fname_pathways_map, sep="\t", header=None, names=["pathway_id", "pathway_name"]
)
pathways_map.head()

# %% [markdown]
# exclude some generic pathways?

# %%
mask = pathways_map["pathway_name"].str.contains("pathways", case=False)
pathways_map.loc[mask]

# %% [markdown]
# Can be downloaded from KEGG:
# - https://rest.kegg.jp/link/compound/pathway


# %% [markdown]
# ## Filtering pathways
# filter some generic pathways if you want.

# %% tags=["hide-input"]
view = annotations.groupby("pathway_id").size().sort_values(ascending=False)
view.plot(
    kind="line", figsize=(10, 5), marker="."
)
view

# %% [markdown]
# Some pathway maps:
# - [map01100](https://rest.kegg.jp/get/path:map01100/image)
# - [map01110](https://rest.kegg.jp/get/path:map01110/image)
# - [map01120](https://rest.kegg.jp/get/path:map01120/image)
# - [map01130](https://rest.kegg.jp/get/path:map01130/image)
#
# For example map00010:
# - see conf map [conf map of map00010](https://rest.kegg.jp/get/path:map00010/conf)
# ![path:map00010/image](https://rest.kegg.jp/get/path:map00010/image)
#
# Additional information for map00010 and map00030:
# - https://rest.kegg.jp/get/path:map00030+path:map00010

# %%
ms2query_results = pd.read_csv(fname_ms2query, index_col=0, sep="\t").drop_duplicates(
    subset=["inchikey", "smiles"]
)
ms2query_results.head()

# %%
inchikey_to_kegg = pd.read_csv(fname_inchikey_to_kegg, index_col=0).astype({"id": str})
inchikey_to_kegg

# %% [markdown]
# ## Reload analysis of covariance (ANCOVA) results
#

# %% tags=["hide-input"]
ancova = pd.read_csv(fname_ancova, index_col=0)
ancova.index = ancova.index.astype(str)
ancova

# %% [markdown]
# Let's see if we could identify features from the differential regulations
# analysis using the available MS2 annotations. We will use the `inchikey_to_kegg`
# mapping from `3_enrichment_analysis_fetch_kegg.ipnnb`, which was pre-executed and the
# results stored. Rerun with new data!

# %% tags=["hide-input"]
inchikey_to_kegg  # .loc[ids_found_inMS2]

# %%
regex_filter = "pval|padj|reject|FC"
ids_found_inMS2 = inchikey_to_kegg['id'].unique().tolist()
ancova.loc[ids_found_inMS2].filter(regex=regex_filter).sort_values('pvalue')

# %% [markdown]
# Make the few identified features significant for illustration purposes.

# %%
ancova.loc[ids_found_inMS2, "pvalue"] = 0.01
ancova.loc[ids_found_inMS2].filter(regex=regex_filter).sort_values("pvalue")

# %% [markdown]
# Let's manually update some compound IDs for the few features we identified.
# - chose one compound per feature

# %% tags=["hide-input"]
inchikey_to_kegg

# %%
rename_index = {
    "9988206023938663754": "C12048",
    "11438838801741346891": "C03194",  # C02962
    "15780731469960021248": "C00193",
}
ancova = ancova.rename(index=rename_index)

# %%
ancova.loc[rename_index.values()].filter(regex=regex_filter).sort_values("pvalue")


# %% [markdown]
# ## Enrichment analysis
# We will use the annoations fetched from KEGG to perform the enrichment analysis.

# %% tags=["hide-input"]
annotations = annotations.rename_axis("identifier").reset_index()
annotations

# %%
ret = acore.enrichment_analysis.run_up_down_regulation_enrichment(
    regulation_data=ancova.rename_axis("identifier").reset_index(),
    annotation=annotations,
    identifier="identifier",
    annotation_col='pathway_id',
    pval_col="pvalue",
    min_detected_in_set=1,
    lfc_cutoff=0.012,
)
ret

# %%
ancova.loc[rename_index.values()].filter(regex=regex_filter).sort_values("pvalue")

# %% [markdown]
# Why do we only see one compound?

# %%
annotations.loc[annotations.identifier.isin(inchikey_to_kegg.kegg_id)]
