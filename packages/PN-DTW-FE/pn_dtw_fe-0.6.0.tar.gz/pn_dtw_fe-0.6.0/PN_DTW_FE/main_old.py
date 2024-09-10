import argparse
import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from .exclude_and_assign_above_threshold import exclude_and_assign_above_threshold
from .sort_and_divide_series_into_n_chunks import sort_and_divide_series_into_n_chunks
from .optimize_chunks_for_normality_pandas import optimize_chunks_for_normality_pandas
from .sort_and_merge_series import sort_and_merge_series
from .merge_bell_shaped_with_spacers_pandas import merge_bell_shaped_with_spacers_pandas
from .calculate_distance_significance import calculate_distance_significance

def PNdtwFE(input_file, geneOFinterest, threshold, desired_chunks, seed=42, run_seed_consistency=False, save_path=None):
    """
    Performs PN-DTW-FE analysis and optionally runs SeedConsistency analysis if multiple seeds are provided.

    Args:
        input_file: Path to the input CSV file.
        geneOFinterest: The gene of interest.
        threshold: The threshold value for splitting expression data.
        desired_chunks: The desired number of chunks.
        seed: Seed value(s) (single value or range: start:end).
        run_seed_consistency: Boolean flag to indicate whether to run SeedConsistency analysis.
        save_path: Path to save the SeedConsistency results.

    Returns:
        None
    """
    df35 = pd.read_csv(input_file, sep='\t')
    df35.set_index(df35.columns[0], inplace=True)

    GeneOfInterest = geneOFinterest
    GeneOfInterest_expression = df35.loc[GeneOfInterest]

    below_threshold, above_threshold = exclude_and_assign_above_threshold(GeneOfInterest_expression[:], threshold)
    total_chunks = desired_chunks + 1
    chunks = sort_and_divide_series_into_n_chunks(below_threshold, total_chunks)

    # Handle seed range
    if ':' in str(seed):
        start, end = map(int, seed.split(':'))
        seed_values = range(start, end + 1)
    else:
        seed_values = [int(seed)]

    # Create output directory if it doesn't exist
    output_dir = "output/seeds"
    os.makedirs(output_dir, exist_ok=True)

    for seed in seed_values:
        optimized_chunks, best_score = optimize_chunks_for_normality_pandas(chunks[0:desired_chunks], desired_chunks, seed=seed, random=42)
        new_chunks_series = [chunk[GeneOfInterest] for chunk in optimized_chunks]
        bell_shaped_chunks = [sort_and_merge_series(chunk) for chunk in new_chunks_series]
        final_chunks_with_spacers = merge_bell_shaped_with_spacers_pandas(chunks, bell_shaped_chunks)
        final_chunks_with_spacers_series = pd.concat([above_threshold, final_chunks_with_spacers])
        sorted_row_indices = final_chunks_with_spacers_series.index.tolist()
        df_35 = df35[sorted_row_indices]

        df_sorted = df_35.reset_index()
        tor1_expression = df_sorted[df_sorted['attribution'] == GeneOfInterest].iloc[:, 1:].values.flatten()

        gene_expressions = []
        for _, row in df_sorted.iterrows():
            gene_expressions.append(row)

        pattern_similarities = {}
        paths = {}

        for gene_expression in gene_expressions:
            if tor1_expression.ndim != 1 or gene_expression.ndim != 1:
                print(f"Error: One of the input arrays is not 1-D.")
                continue
            distance, path = fastdtw(np.array(tor1_expression).flatten(), np.array(gene_expression.iloc[1:].values).flatten(), dist=euclidean)
            gene_name = gene_expression[0]
            pattern_similarities[gene_name] = distance
            paths[gene_name] = path

        # Sorting genes by their DTW distance to tor1_expression (lower distance means more similar)
        sorted_distances = dict(sorted(pattern_similarities.items(), key=lambda item: item[1]))

        # Creating list of dictionaries for DataFrame
        data_rows = [{'gene_name': gene_name, 'distance': sorted_distances[gene_name], 'path': paths[gene_name]} 
                     for gene_name in sorted_distances]

        df_similarities = pd.DataFrame(data_rows)
        output_filename = os.path.join(output_dir, f"Genes_ranking_with_seed_{seed}_DTW.txt")
        df_similarities.to_csv(output_filename, sep="\t", index=False)
        print(f"Analysis completed for seed {seed}. Output saved to {output_filename}.")

    # Run SeedConsistency if requested
    if run_seed_consistency:
        seed_consistency_df = calculate_distance_significance(output_dir, save_path=save_path)
        print(f"SeedConsistency analysis completed. Results saved to {save_path}.")


def run_pndtwfe():
    parser = argparse.ArgumentParser(description='Run PN_DTW_FE analysis', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, required=True, help='Input CSV file')
    parser.add_argument('--geneOFinterest', type=str, required=True, help='Gene of Interest')
    parser.add_argument('--threshold', type=int, required=True, help='Threshold value')
    parser.add_argument('--desired_chunks', type=int, required=True, help='Number of desired chunks')
    parser.add_argument('--seed', type=str, required=True, help='Seed values (single value or range: start:end)')
    parser.add_argument('--run_seed_consistency', action='store_true', help='Perform SeedConsistency analysis')
    parser.add_argument('--save_path', type=str, help='Path to save the SeedConsistency results')

    args = parser.parse_args()
    PNdtwFE(args.input, args.geneOFinterest, args.threshold, args.desired_chunks, seed=args.seed, run_seed_consistency=args.run_seed_consistency, save_path=args.save_path)

def run_seedconsistency():
    parser = argparse.ArgumentParser(description='Run SeedConsistency analysis', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory containing the seed files')
    parser.add_argument('--save_path', type=str, required=True, help='Path to save the SeedConsistency results')

    args = parser.parse_args()
    calculate_distance_significance(args.output_dir, save_path=args.save_path)

if __name__ == "__main__":
    run_pndtwfe()