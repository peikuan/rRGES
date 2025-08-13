import pandas as pd
import numpy as np
from collections import defaultdict
import argparse
import os

def main(gepid,output):
    # GEPID file
    with open(gepid, 'r') as f:
        gepids = [line.strip() for line in f.readlines() if line.strip()]
    
    # RGES score file
    matrix_df = pd.read_csv('data/RGES.txt', sep='\t')
    
    id_columns = [col for col in matrix_df.columns if col in gepids]
    if not id_columns:
        print("Error: No matching GEPIDs found in RGES file.")
        return
        
    selected_df = matrix_df[['Compounds'] + id_columns].copy()
    
    #Pert_id and Drug
    compounds_split = selected_df['Compounds'].str.split('_', n=2, expand=True)
    selected_df['Pert_id'] = compounds_split[0]
    selected_df['Drug'] = compounds_split[1]
    pert_to_drug = selected_df.drop_duplicates('Pert_id').set_index('Pert_id')['Drug'].to_dict()
    
    #min-max normalization
    value_columns = id_columns
    value_df = selected_df[value_columns]
    min_vals = value_df.min()
    max_vals = value_df.max()
    range_vals = max_vals - min_vals
    range_vals[range_vals == 0] = 1
    normalized_df = (2*(value_df - min_vals) / range_vals)-1
    normalized_df['Pert_id'] = selected_df['Pert_id']
    
    #minimum normalized value for each Pert_id
    pert_values = defaultdict(list)
    
    for col in gepids:
        #RGES<0
        mask_negative = selected_df[col] < 0
        if not mask_negative.any():
            continue
        
        filtered_df = normalized_df.loc[mask_negative, ['Pert_id', col]].copy()
        filtered_df.rename(columns={col: 'norm_value'}, inplace=True)
        
        #group by Pert_id
        min_values = filtered_df.groupby('Pert_id')['norm_value'].min().reset_index()
        
        #minimum value for each row
        for _, row in min_values.iterrows():
            pert_id = row['Pert_id']
            norm_val = row['norm_value']
            pert_values[pert_id].append(norm_val)
    
    #rRGES
    results = []
    for pert_id, values in pert_values.items():
        if values:
            rrges = np.mean(values)
            results.append({
                'Pert_id': pert_id,
                'Drug': pert_to_drug.get(pert_id, ''),
                'rRGES': rrges
            })
    
    if not results:
        print("No results after processing.")
        return
    
    #Rank
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by='rRGES', ascending=True)
    results_df['Rank'] = range(1, len(results_df) + 1)
    
    #moa
    moa_df = pd.read_csv('data/moa.txt', sep='\t')
    drug_to_moa = moa_df.set_index('drug')['moa'].to_dict()
    results_df['moa'] = results_df['Drug'].str.lower().map(lambda x: drug_to_moa.get(x, '-'))
    results_df['Drug'] = results_df['Drug']


    #output
    output_df = results_df[['Rank', 'Pert_id', 'Drug', 'rRGES', 'moa']]
    output_df.to_csv(output, sep='\t', index=False)
    print(f"Results saved to {output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate rRGES scores from RGES data')
    parser.add_argument('--gepid', required=True, help='File containing GEPIDs to process (one per line)')
    parser.add_argument('--output', default='output.txt', help='Output file for small-molecule compounds')
    
    args = parser.parse_args()
    
    main(args.gepid,args.output)






