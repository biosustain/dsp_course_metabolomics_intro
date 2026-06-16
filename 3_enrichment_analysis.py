# %% [markdown]
# # Enrichment analysis

# %%
from collections import defaultdict
from pathlib import Path

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


# %% tags=["parameters"]
fname_ms2query = "results_prepared/output_ms2query_Linked_data.tsv"
fname_ancova = "results_prepared/ancova_results.csv"
fname_pathways_map = "results_prepared/pathways_map.tsv"
fname_inchikey_to_kegg = "results_prepared/inchikey_to_kegg.csv"


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


# %%
fname_annotations = Path(".") / "link_compound_pathway.tsv"
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
# ## Filtering pathways
# filter some generic pathways?

# %%
annotations.groupby("pathway_id").size().sort_values(ascending=False)


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

# %% markdown
annotations.groupby("pathway_id").size().sort_values(ascending=False).plot(
    kind="line", figsize=(10, 5), marker="."
)

# %%
ms2query_results = pd.read_csv(fname_ms2query, index_col=0, sep="\t").drop_duplicates(
    subset=["inchikey", "smiles"]
)
ms2query_results.head()

# %%
inchikey_to_kegg = pd.read_csv(fname_inchikey_to_kegg, index_col=0).astype({"id": str})
inchikey_to_kegg

# %% [markdown]
# ## Map features to MS2Query results
#
# - only needed as features identifies are based on xcms and ms2query results are based on
#   metaboigniter, so the feature IDs don't match. If we use features from metaboigniter
#   for the differential analysis, we could have avoided this step.
#

# %%
ancova = pd.read_csv(fname_ancova, index_col=0)
ancova.index = ancova.index.astype(str)
ancova

# %%
regex_filter = "pval|padj|reject|FC"
ids_found_inMS2 = inchikey_to_kegg['id'].unique().tolist()
ancova.loc[ids_found_inMS2].filter(regex=regex_filter).sort_values('pvalue')

# %%
ancova.loc[ids_found_inMS2, "pvalue"] = 0.01
ancova.loc[ids_found_inMS2].filter(regex=regex_filter).sort_values("pvalue")

# %%
inchikey_to_kegg #.loc[ids_found_inMS2]

# %%
rename_index = {
    "9988206023938663754": "C12048",
    "11438838801741346891": "C03194",  # C02962
    "15780731469960021248": "C00193",
}
ancova = ancova.rename(index=rename_index)

# %%
ancova.loc[rename_index.values()].filter(regex=regex_filter).sort_values("pvalue")

# %%
annotations = annotations.rename_axis("identifier").reset_index()
annotations

# %% [markdown]
# ## Enrichment analysis

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
