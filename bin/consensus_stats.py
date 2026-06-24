!/usr/bin/env python3
"""
consensus_stats.py -- print FileInfo-style statistics for a consensusXML.

Mimics the output of the OpenMS `FileInfo` TOPP tool (with -i for identification
statistics, -m for intensity/meta statistics) for ConsensusMap inputs.

Usage:
    python bin/consensus_stats.py path/to/file.consensusXML
"""
from collections import Counter

import numpy as np
import pyopenms as oms


def summarize(values):
    """Return (min, max, mean, median, stddev) for a 1-D iterable."""
    a = np.asarray(list(values), dtype=float)
    if a.size == 0:
        return (float("nan"),) * 5
    return (a.min(), a.max(), a.mean(), np.median(a), a.std())


def consensus_file_info(path: str) -> None:
    cmap = oms.ConsensusMap()
    oms.ConsensusXMLFile().load(path, cmap)
    cmap.updateRanges()  # required before getMin*/getMax* are valid

    headers = cmap.getColumnHeaders()       # dict: map_index -> ColumnHeader
    n_consensus = cmap.size()

    # ---- per-map element counts + global accumulators -------------------
    per_map = Counter()                     # how many consensus features touch map i
    size_dist = Counter()                   # distribution of consensus sizes (#sub-features)
    charge_dist = Counter()
    intensities, qualities, widths = [], [], []
    rt_vals, mz_vals = [], []
    n_assigned_pep = 0

    for cf in cmap:
        size_dist[cf.size()] += 1
        charge_dist[cf.getCharge()] += 1
        intensities.append(cf.getIntensity())
        qualities.append(cf.getQuality())
        widths.append(cf.getWidth())
        rt_vals.append(cf.getRT())
        mz_vals.append(cf.getMZ())
        n_assigned_pep += len(cf.getPeptideIdentifications())
        for fh in cf.getFeatureList():
            per_map[fh.getMapIndex()] += 1

    # ---- header block ---------------------------------------------------
    print(f"File name : {path}")
    print(f"File type : consensusXML")
    print()
    print(f"Number of consensus features: {n_consensus}")
    print(f"Number of input maps        : {len(headers)}")
    print()

    # ---- ranges (FileInfo-style) ---------------------------------------
    print("Ranges:")
    print(f"  retention time: {cmap.getMinRT():12.2f} .. {cmap.getMaxRT():12.2f}")
    print(f"  mass-to-charge: {cmap.getMinMZ():12.4f} .. {cmap.getMaxMZ():12.4f}")
    print(f"  intensity     : {cmap.getMinIntensity():12.4g} .. {cmap.getMaxIntensity():12.4g}")
    print()

    # ---- per-map breakdown ---------------------------------------------
    print("Input maps (column headers):")
    print(f"  {'idx':>4}  {'#elements':>10}  {'label':<16}  filename")
    for idx in sorted(headers):
        h = headers[idx]
        label = h.label if isinstance(h.label, str) else h.label.decode()
        fname = h.filename if isinstance(h.filename, str) else h.filename.decode()
        print(f"  {idx:>4}  {per_map.get(idx, 0):>10}  {label:<16}  {fname}")
    print()

    # ---- consensus size distribution -----------------------------------
    print("Consensus size distribution (sub-features per consensus feature):")
    for s in sorted(size_dist):
        print(f"  size {s:>3}: {size_dist[s]:>8}")
    full = size_dist.get(len(headers), 0)
    if n_consensus:
        print(f"  fully-quantified (all {len(headers)} maps): "
              f"{full} ({100.0 * full / n_consensus:.1f}%)")
    print()

    # ---- charge distribution -------------------------------------------
    print("Charge distribution:")
    for z in sorted(charge_dist):
        print(f"  charge {z:>2}: {charge_dist[z]:>8}")
    print()

    # ---- intensity / quality statistics (FileInfo -m) ------------------
    imin, imax, imean, imed, istd = summarize(intensities)
    qmin, qmax, qmean, qmed, qstd = summarize(qualities)
    print("Intensity statistics (consensus level):")
    print(f"  min={imin:.4g}  max={imax:.4g}  mean={imean:.4g}  "
          f"median={imed:.4g}  stddev={istd:.4g}")
    print("Quality statistics:")
    print(f"  min={qmin:.4f}  max={qmax:.4f}  mean={qmean:.4f}  "
          f"median={qmed:.4f}  stddev={qstd:.4f}")
    print()

    # ---- identification statistics (FileInfo -i) -----------------------
    prot_ids = cmap.getProteinIdentifications()
    unassigned = cmap.getUnassignedPeptideIdentifications()
    n_prot_hits = sum(len(pi.getHits()) for pi in prot_ids)
    print("Identification statistics:")
    print(f"  protein identification runs : {len(prot_ids)}")
    print(f"  total protein hits          : {n_prot_hits}")
    print(f"  assigned peptide IDs        : {n_assigned_pep}")
    print(f"  unassigned peptide IDs      : {len(unassigned)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Print FileInfo-style statistics for a consensusXML file."
    )
    parser.add_argument("input", help="Path to input consensusXML file")
    args = parser.parse_args()
    consensus_file_info(args.input)
