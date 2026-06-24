
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p raw_data
cd raw_data

base_url="https://zenodo.org/records/10041900/files"
files=(
10__Sel_delta5_ex.raw
1__Sel_WT1_ex10.raw
2__Sel_WT2_ex10.raw
3__Sel_WT3_ex10.raw
4__Sel_WT4_ex10.raw
5__Sel_WT5_ex10.raw
11__Sel_WT1_stat10.raw
12__Sel_WT2_stat10.raw
13__Sel_WT3_stat10.raw
14__Sel_WT4_stat10.raw
15__Sel_WT5_stat10.raw
6__Sel_delta1_ex10.raw
7__Sel_delta2_ex10.raw
8__Sel_delta3_ex10.raw
9__Sel_delta4_ex10.raw
10__Sel_delta5_ex10.raw
16__Sel_delta1_stat10.raw
17__Sel_delta2_stat10.raw
18__Sel_delta3_stat10.raw
19__Sel_delta4_stat10.raw
20__Sel_delta5_stat10.raw
)

for file in "${files[@]}"; do
  echo "Downloading $file..."
  wget -nc "${base_url}/${file}"
done

echo "Download complete."


# wget https://zenodo.org/records/10041900/files/10__Sel_delta5_ex.raw
# wget https://zenodo.org/records/10041900/files/1__Sel_WT1_ex10.raw
# wget https://zenodo.org/records/10041900/files/2__Sel_WT2_ex10.raw
# wget https://zenodo.org/records/10041900/files/3__Sel_WT3_ex10.raw
# wget https://zenodo.org/records/10041900/files/4__Sel_WT4_ex10.raw
# wget https://zenodo.org/records/10041900/files/5__Sel_WT5_ex10.raw
# wget https://zenodo.org/records/10041900/files/11__Sel_WT1_stat10.raw
# wget https://zenodo.org/records/10041900/files/12__Sel_WT2_stat10.raw
# wget https://zenodo.org/records/10041900/files/13__Sel_WT3_stat10.raw
# wget https://zenodo.org/records/10041900/files/14__Sel_WT4_stat10.raw
# wget https://zenodo.org/records/10041900/files/15__Sel_WT5_stat10.raw
# wget https://zenodo.org/records/10041900/files/6__Sel_delta1_ex10.raw
# wget https://zenodo.org/records/10041900/files/7__Sel_delta2_ex10.raw
# wget https://zenodo.org/records/10041900/files/8__Sel_delta3_ex10.raw
# wget https://zenodo.org/records/10041900/files/9__Sel_delta4_ex10.raw
# wget https://zenodo.org/records/10041900/files/10__Sel_delta5_ex10.raw
# wget https://zenodo.org/records/10041900/files/16__Sel_delta1_stat10.raw
# wget https://zenodo.org/records/10041900/files/17__Sel_delta2_stat10.raw
# wget https://zenodo.org/records/10041900/files/18__Sel_delta3_stat10.raw
# wget https://zenodo.org/records/10041900/files/19__Sel_delta4_stat10.raw
# wget https://zenodo.org/records/10041900/files/20__Sel_delta5_stat10.raw
