#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

base_url="https://ftp.ebi.ac.uk/pub/databases/metabolights/studies/public/MTBLS8735/FILES"
files=(
  MS_2_A_POS.mzML
  MS_2_E_POS.mzML
  MS_2_STUDY_POOL_POS.mzML
  MS_A_POS.mzML
  MS_B_POS.mzML
  MS_C_POS.mzML
  MS_D_POS.mzML
  MS_E_POS.mzML
  MS_F_POS.mzML
  MSMS_2_A_CE20_POS.mzML
  MSMS_2_A_CE30_POS.mzML
  MSMS_2_A_CES_POS.mzML
  MSMS_2_E_CE20_POS.mzML
  MSMS_2_E_CE30_POS.mzML
  MSMS_2_E_CES_POS.mzML
  MSMS_2_STUDY_POOL_CE20_POS.mzML
  MSMS_2_STUDY_POOL_CE30_POS.mzML
  MSMS_2_STUDY_POOL_CES_POS.mzML
  MS_QC_POOL_1_POS.mzML
  MS_QC_POOL_2_POS.mzML
  MS_QC_POOL_3_POS.mzML
  MS_QC_POOL_4_POS.mzML
)

for file in "${files[@]}"; do
  echo "Downloading $file..."
  wget -nc "${base_url}/${file}"
done

echo "Download complete."

