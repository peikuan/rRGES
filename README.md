# nRRGES Calculator

# outlier filtered
python pca_outlier_filter.py \
    --gepid example/Schizophrenia.txt \
    --data log2FC.txt \
    --threshold 2 \
    --output example/Schizophrenia_outlier_filter.txt
  
# Argument
| Argument      | Description                                      | Default |
|---------------|--------------------------------------------------|---------|
| '--gepid'     | File containing GEPIDs to process (one per line) | Required|
| '--data'      | Tab-separated file with PCA data                 | Required|
| '--threshold' | Z-score threshold for outlier detection          | 2.0     |
| '--output'    | Output file for filtered GEPIDs                  | Required|



# rRGES
python rRGES_calculator.py \
    --gepid example/Schizophrenia_outlier_filter.txt \
    --rges  data/RGES.txt \
    --output Schizophrenia_rRGES.txt
    
# Argument
| Argument      | Description                                      | Default |
|---------------|--------------------------------------------------|---------|
| '--gepid'     | File containing GEPIDs to process (one per line) | Required|
| '--rges'      | Tab-separated file with RGES data                | Required|
| '--output'    | Output file for small-molecule compounds         | 2.0     |





