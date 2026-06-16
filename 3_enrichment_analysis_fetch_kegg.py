# %%
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pubchempy as pcp
from acore.io.kegg import lookup_cid_to_kegg_id


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

# %%
ms2query_results = pd.read_csv(fname_ms2query, index_col=0, sep="\t").drop_duplicates(
    subset=["inchikey", "smiles"]
)
ms2query_results.head()

# %%
to_lookup = ms2query_results[
    [
        "ms2query_model_prediction",
        "precursor_mz_difference",
        "precursor_mz_query_spectrum",
        "precursor_mz_analog",
        "inchikey",
        "analog_compound_name",
        "smiles",
    ]
].drop_duplicates(subset=["inchikey", "smiles"])
to_lookup

# %% [markdown]
# Find PubChem CIDs for the InChIKeys

# %%
for _inchikey in to_lookup.inchikey.unique():
    if _inchikey in compounds:
        continue
    compounds[_inchikey] = pcp.get_compounds(_inchikey, namespace="inchikey")
compounds

# %% [markdown]
# Then look up KEGG IDs for those CIDs

# %%
cids = [c.cid for pcp_list in compounds.values() for c in pcp_list if c.cid is not None]
kegg_compounds = lookup_cid_to_kegg_id(cids)
kegg_compounds


# %%
inchikey_to_kegg = []
for inchikey, pcp_list in compounds.items():
    for c in pcp_list:
        if c.cid is not None and c.cid in kegg_compounds:
            inchikey_to_kegg.append((inchikey, kegg_compounds[c.cid]))
inchikey_to_kegg

# %%
inchikey_to_kegg = pd.DataFrame(inchikey_to_kegg, columns=["inchikey", "kegg_id"])
inchikey_to_kegg

# %% [markdown]
# And finally find KEGG pathways for those KEGG IDs.
# inchikey_to_kegg = inchikey_to_kegg.join(
#     to_lookup.reset_index().set_index("inchikey"), on="inchikey"
# )
# inchikey_to_kegg

# %%
fname = "results_prepared/inchikey_to_kegg.csv"
inchikey_to_kegg.to_csv(fname, index=False)

# %% [markdown]
# Done.
