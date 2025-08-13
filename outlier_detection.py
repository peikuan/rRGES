import pandas as pd
import numpy as np
import sys
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import mahalanobis
import argparse

def main(gepid,data,output):
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
 

    #PCA data
    data = sub_df[valid_ids].values.T
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    #PCA
    pca = PCA(n_components=2)
    pca_scores = pca.fit_transform(data_scaled)
    cov_matrix = np.cov(pca_scores.T)
    inv_cov = np.linalg.inv(cov_matrix)
    center = np.mean(pca_scores, axis=0)

    mahalanobis_dist = []
    for i in range(len(pca_scores)):
        mahalanobis_dist.append(mahalanobis(pca_scores[i], center, inv_cov))
    
    #z-score
    mean_dist = np.mean(mahalanobis_dist)
    std_dist = np.std(mahalanobis_dist)
    z_scores = (mahalanobis_dist - mean_dist) / std_dist

    #outliers
    outliers = np.where(abs(z_scores) >= 1.5)[0]
    non_outlier_ids = [valid_ids[i] for i in range(len(valid_ids)) if i not in outliers]

    #print mahalanobis_dist and z-score
    print("ID\tmahalanobis_dist\tZ-Score")
    for i, id in enumerate(valid_ids):
        print(f"{id}\t{mahalanobis_dist[i]:.6f}\t{z_scores[i]:.6f}")

    #output
    with open(args.output, 'w') as f:
        f.write("\n".join(non_outlier_ids))
    
    print(f"\nNon_Outlier IDs saved to {args.output}")
    print(f"Original IDs: {len(gepids)}, After filtering: {len(non_outlier_ids)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PCA-based outlier detection')
    parser.add_argument('--gepid', required=True, help='Input ID file')
    parser.add_argument('--data', required=True, help='Input PCA data file')
    parser.add_argument('--output', required=True, help='Output filtered ID file')
    args = parser.parse_args()

    main(args.gepid,args.data,args.output)




