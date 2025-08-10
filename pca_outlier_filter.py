import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.stats import zscore
import argparse

def main(gepid,data,output,threshold):
    #GEPID file
    with open(args.gepid, 'r') as f:
        gepids = [line.strip() for line in f.readlines() if line.strip()]

    #PCA data
    pca_df = pd.read_csv(args.data, sep='\t')


    valid_ids = [col for col in gepids if col in pca_df.columns]
    if not valid_ids:
        print("No matching GEPIDs found in data file")
        return

    #filter NaN
    sub_df = pca_df[['gene_id'] + valid_ids].copy()
    sub_df = sub_df.dropna(axis=0)

    #chech
    if len(sub_df) < 2:
        print("Insufficient data after filtering NA rows")
        return

    #PCA data
    data = sub_df[valid_ids].values.T

    pca = PCA(n_components=2)
    components = pca.fit_transform(data)
    pc1 = components[:, 0]
    pc2 = components[:, 1]

    #z-score
    z1 = zscore(pc1)
    z2 = zscore(pc2)
    print("ID\tPC1_zscore\tPC2_zscore")
    for i, id in enumerate(valid_ids):
        print(f"{id}\t{z1[i]:.4f}\t{z2[i]:.4f}")

    #outlier
    valid_mask = (np.abs(z1) < args.threshold) & (np.abs(z2) < args.threshold)
    filtered_ids = [valid_ids[i] for i in range(len(valid_ids)) if valid_mask[i]]

    #output
    with open(args.output_file, 'w') as f:
        f.write("\n".join(filtered_ids))

    print(f"\nFiltered IDs saved to {args.output_file}")
    print(f"Original IDs: {len(gepids)}, After filtering: {len(filtered_ids)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PCA-based outlier detection')
    parser.add_argument('--gepid', required=True, help='Input ID file')
    parser.add_argument('--data', required=True, help='Input PCA data file')
    parser.add_argument('--output', required=True, help='Output filtered ID file')
    parser.add_argument('--threshold', type=float, default=2.0, help='Z-score threshold (default: 2.0)')
    args = parser.parse_args()

    main(args.gepid,args.data,args.output,args.threshold)
