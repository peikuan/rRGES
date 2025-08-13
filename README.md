# rRGES Calculator
The rRGES Calculator is a tool for analyzing small-molecule compounds up- and down-regulated gene sets to calculate representative reverse gene expression signature (rRGES) scores. This tool is particularly useful in drug repurposing and discovery.

# requirements
pandas>=1.3.0

numpy>=1.21.0

scikit-learn>=1.0.0

tqdm>=4.0.0

# outlier filtered

python outlier_detection.py \
    --gepid example/Schizophrenia.txt \
    --data log2FC.txt \
    --output example/Schizophrenia_outlier_filter.txt
    
  
# Argument
| Argument      | Description                                      | Default |
|---------------|--------------------------------------------------|---------|
| '--gepid'     | File containing GEPIDs to process (one per line) | Required|
| '--data'      | Tab-separated file with log2FC data              | Required|
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
| '--output'    | Output file for small-molecule compounds         | Required|





