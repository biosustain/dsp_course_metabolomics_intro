# %%
import json
import pandas as pd
from pathlib import Path

data_dir = Path(__file__).parent / "mzml_10micro"

rows = []
for json_file in sorted(data_dir.glob("*.json")):
    with open(json_file) as f:
        raw = json.load(f)

    row = {"filename": json_file.stem}
    for section, entries in raw.items():
        for entry in entries:
            key = f"{section}.{entry['name']}"
            row[key] = entry["value"]
    rows.append(row)

df = pd.DataFrame(rows).set_index("filename")
print(df.shape)
print(df.head())

# %%
df.to_csv("thermorawfile_metadata.csv")

# %%
sel_columns = [
    # "FileProperties.Pathname",
    # "FileProperties.Version",
    "FileProperties.Content Creation Date",
    "InstrumentProperties.Thermo Scientific instrument model",
    # "InstrumentProperties.instrument attribute",
    # "InstrumentProperties.instrument serial number",
    # "InstrumentProperties.Software Version",
    # "InstrumentProperties.firmware version",
    "MsData.Number of MS1 spectra",
    "MsData.Number of MS2 spectra",
    "MsData.MS min charge",
    "MsData.MS max charge",
    "MsData.MS min RT",
    "MsData.MS max RT",
    "MsData.MS min MZ",
    "MsData.MS max MZ",
    "ScanSettings.scan start time",
    "ScanSettings.expected runtime",
    "ScanSettings.mass resolution",
    # "ScanSettings.mass unit",
    "ScanSettings.Number of scans",
    # "ScanSettings.Retention time range",
    "ScanSettings.Mz range",
    "ScanSettings.beam-type collision-induced dissociation",
    # "ScanSettings.MS scan range",
    # "SampleData.sample number",
    # "SampleData.Vial",
    # "SampleData.injection volume setting",
    # "SampleData.Row",
    # "SampleData.dilution factor",
    # "SampleData.device acquisition method",
]
df[sel_columns]

# %%
