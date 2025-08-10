# rRGES
python pca_filter.py \
    --id_file path/to/id.txt \
    --pca_file path/to/pca.txt \
    --output_file path/to/filtered_ids.txt
    [--threshold 2.0]
    
| Argument       | Description                                      | Default |
|----------------|--------------------------------------------------|---------|
| `--id_file`    | File containing IDs to process (one per line)    | Required|
| `--pca_file`   | Tab-separated file with PCA data                 | Required|
| `--output_file`| Output file for filtered IDs                     | Required|
| `--threshold`  | Z-score threshold for outlier detection          | 2.0     |
| `--verbose`    | Show detailed processing information             | False   |

