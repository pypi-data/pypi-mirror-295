from pathlib import Path
import pandas as pd
import numpy as np
from collections import defaultdict

def calculate_distance_significance(output_dir="output/seeds", save_path=None, sort_by="median", genesOFinterest=None):
    """
    Calculates gene distance consistency for each gene across multiple seeds, sorts by median/mean and standard deviation,
    and saves each gene's results in a separate file.

    Parameters:
    - output_dir: Directory containing the input files.
    - save_path: Path to save the sorted results (optional).
    - sort_by: 'median' or 'mean' to specify the sorting criteria (default is 'median').
    - genesOFinterest: List of genes of interest to process (optional). If None, processes all available genes.
    """

    if genesOFinterest is None:
        raise ValueError("genesOFinterest must be provided as a list of genes to analyze.")

    for gene in genesOFinterest:
        gene_results = defaultdict(list)

        # Step 1: Gather distances for the current gene from multiple seed files
        for file in Path(output_dir).glob(f"Genes_ranking_with_seed_*_for_{gene}_DTW.txt"):
            try:
                df = pd.read_csv(file, sep="\t")
                for gene_name, distance in df[['gene_name', 'distance']].values:
                    gene_results[gene_name].append(distance)
            except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
                print(f"Error processing file {file}: {e}")
                continue

        # Step 2: Convert the defaultdict to a DataFrame for this gene
        gene_df = pd.DataFrame({
            'gene_name': list(gene_results.keys()),
            'distances': list(gene_results.values())
        })

        # Step 3: Calculate median/mean and standard deviation for this gene
        if sort_by == "median":
            gene_df['central_tendency'] = gene_df['distances'].apply(np.median)
        elif sort_by == "mean":
            gene_df['central_tendency'] = gene_df['distances'].apply(np.mean)
        else:
            raise ValueError("Invalid sort_by value. Use 'median' or 'mean'.")

        gene_df['std_deviation'] = gene_df['distances'].apply(np.std)

        # Step 4: Sort by central_tendency and std_deviation
        gene_df.sort_values(by=['central_tendency', 'std_deviation'], ascending=[True, True], inplace=True)

        # Step 5: Save each gene's DataFrame to a separate file
        if save_path:
            gene_save_path = Path(output_dir).parent / f"{gene}_distance_statistics.txt"
            gene_df.to_csv(gene_save_path, sep="\t", index=False)
            print(f"Saved results for gene {gene} to {gene_save_path}")

    print("All genes processed and saved.")

'''
from pathlib import Path
import pandas as pd
import numpy as np
from collections import defaultdict

def calculate_distance_significance(output_dir="output/seeds", save_path=None, sort_by="median"):
    """
    Calculates gene distance consistency across multiple seeds, sorts by median/mean and standard deviation,
    and returns a DataFrame with gene_name, median/mean distance, std_deviation, and list of distances.
    
    Parameters:
    - output_dir: Directory containing the input files.
    - save_path: Path to save the sorted results (optional).
    - sort_by: 'median' or 'mean' to specify the sorting criteria (default is 'median').
    """

    # Step 1: Gather distances for each gene from multiple seed files
    all_results = defaultdict(list)
    for file in Path(output_dir).glob("Genes_ranking_with_seed_*_DTW.txt"):
        try:
            df = pd.read_csv(file, sep="\t")
            for gene_name, distance in df[['gene_name', 'distance']].values:
                all_results[gene_name].append(distance)
        except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            print(f"Error processing file {file}: {e}")
            continue

    # Step 2: Convert the defaultdict to a DataFrame
    combined_df = pd.DataFrame({
        'gene_name': list(all_results.keys()),
        'distances': list(all_results.values())
    })

    # Step 3: Calculate median/mean and standard deviation
    if sort_by == "median":
        combined_df['central_tendency'] = combined_df['distances'].apply(np.median)
    elif sort_by == "mean":
        combined_df['central_tendency'] = combined_df['distances'].apply(np.mean)
    else:
        raise ValueError("Invalid sort_by value. Use 'median' or 'mean'.")

    combined_df['std_deviation'] = combined_df['distances'].apply(np.std)

    # Step 4: Sort by central_tendency and std_deviation
    combined_df.sort_values(by=['central_tendency', 'std_deviation'], ascending=[True, True], inplace=True)

    # Step 5: Reorder columns to keep only the relevant information
    final_df = combined_df[['gene_name', 'central_tendency', 'std_deviation', 'distances']]

    # Step 6: Save to file if save_path is provided
    if save_path:
        final_df.to_csv(save_path, sep="\t", index=False)

    return final_df
    '''