# pca_outlier_filter
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
| '--threshold' | Z-score threshold for outlier detection          | Required|
| '--output'    | Output file for filtered GEPIDs                  | 2.0     |









