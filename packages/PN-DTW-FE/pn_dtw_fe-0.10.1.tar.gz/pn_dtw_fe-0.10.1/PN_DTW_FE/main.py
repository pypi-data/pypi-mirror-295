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
from .tmm import tmm_normalization, manual_tmm_normalization
from fastdtw import fastdtw

def PNdtwFE(input_file, genesOFinterest, thresholds, desired_chunks, seed=42, run_seed_consistency=False, save_path=None, normalization=False):
    """
    Performs PN-DTW-FE analysis for multiple genes of interest and optionally runs SeedConsistency analysis if multiple seeds are provided.
    Ranks genes based on the average distance across multiple genes of interest.

    Args:
        input_file: Path to the input CSV file.
        genesOFinterest: List of genes of interest.
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

    if normalization:
        df35 = manual_tmm_normalization(df35)
        df35 = df35.reset_index()
        df35.rename(columns={'index': 'attribution'}, inplace=True)
        df35.set_index('attribution', inplace=True)
        print(df35.index)
    else:
        print("Skipping normalization.")


    # Handle seed range
    if ':' in str(seed):
        start, end = map(int, seed.split(':'))
        seed_values = range(start, end + 1)
    else:
        seed_values = [int(seed)]

    output_dir = "output/seeds"
    os.makedirs(output_dir, exist_ok=True)

    all_gene_distances = {}

    # Split thresholds into a list and map them to genes
    thresholds = list(map(int, thresholds.split(',')))

    for i, geneOFinterest in enumerate(genesOFinterest):
        print(geneOFinterest)
        threshold = thresholds[i]
        GeneOfInterest_expression = df35.loc[geneOFinterest]
        below_threshold, above_threshold = exclude_and_assign_above_threshold(GeneOfInterest_expression[:], threshold)
        total_chunks = desired_chunks + 1
        chunks = sort_and_divide_series_into_n_chunks(below_threshold, total_chunks)

        gene_distances = {}

        for seed in seed_values:
            optimized_chunks, best_score = optimize_chunks_for_normality_pandas(chunks[0:desired_chunks], desired_chunks, seed=seed, random=seed)
            new_chunks_series = [chunk[geneOFinterest] for chunk in optimized_chunks]
            bell_shaped_chunks = [sort_and_merge_series(chunk) for chunk in new_chunks_series]
            final_chunks_with_spacers = merge_bell_shaped_with_spacers_pandas(chunks, bell_shaped_chunks)
            final_chunks_with_spacers_series = pd.concat([above_threshold, final_chunks_with_spacers])
            sorted_row_indices = final_chunks_with_spacers_series.index.tolist()
            df_35 = df35[sorted_row_indices]

            df_sorted = df_35.reset_index()
            tor_expression = df_sorted[df_sorted['attribution'] == geneOFinterest].iloc[:, 1:].values.flatten()

            gene_expressions = []
            for _, row in df_sorted.iterrows():
                gene_expressions.append(row)

            pattern_similarities = {}

            for gene_expression in gene_expressions:
                if tor_expression.ndim != 1 or gene_expression.ndim != 1:
                    print(f"Error: One of the input arrays is not 1-D.")
                    continue
                distance, _ = fastdtw(np.array(tor_expression).flatten(), np.array(gene_expression.iloc[1:].values).flatten())
                gene_name = gene_expression[0]
                if gene_name not in gene_distances:
                    gene_distances[gene_name] = []
                gene_distances[gene_name].append(distance)

            # Save the gene rankings for the current gene of interest and seed
            output_filename = os.path.join(output_dir, f"Genes_ranking_with_seed_{seed}_for_{geneOFinterest}_DTW.txt")
            df_similarities = pd.DataFrame({'gene_name': gene_distances.keys(), 'distance': [np.mean(d) for d in gene_distances.values()]})
            df_similarities.to_csv(output_filename, sep="\t", index=False)
            print(f"Analysis completed for gene {geneOFinterest} with seed {seed}. Output saved to {output_filename}.")

        # Store the average distance for each gene across all seeds for this gene of interest
        for gene_name, distances in gene_distances.items():
            if gene_name not in all_gene_distances:
                all_gene_distances[gene_name] = []
            all_gene_distances[gene_name].append(np.mean(distances))
        #print(all_gene_distances)

    if run_seed_consistency:
        seed_consistency_df = calculate_distance_significance(output_dir=output_dir, save_path=save_path, genesOFinterest=genesOFinterest)
        print(f"SeedConsistency analysis completed. Results saved to {save_path}.")

    # Compute the final ranking based on the average of averages
    final_ranking = {gene: np.mean(distances) for gene, distances in all_gene_distances.items()}
    final_sorted_ranking = dict(sorted(final_ranking.items(), key=lambda item: item[1]))

    # Save the final ranking
    final_df = pd.DataFrame({'gene_name': final_sorted_ranking.keys(), 'average_distance': final_sorted_ranking.values()})
    final_output_filename = os.path.join(output_dir, "Final_Genes_Ranking_Average_DTW.txt")
    final_df.to_csv(final_output_filename, sep="\t", index=False)
    print(f"Final ranking based on average distances saved to {final_output_filename}.")

    
def run_pndtwfe():
    parser = argparse.ArgumentParser(description='Run PN_DTW_FE analysis', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, required=True, help='Input CSV file')
    parser.add_argument('--geneOFinterest', type=str, required=True, help='Comma-separated list of genes of interest')
    #parser.add_argument('--threshold', type=int, required=True, help='Threshold value')
    parser.add_argument('--threshold', type=str, required=True, help='Comma-separated list of threshold values')
    parser.add_argument('--desired_chunks', type=int, required=True, help='Number of desired chunks')
    parser.add_argument('--seed', type=str, required=True, help='Seed values (single value or range: start:end)')
    parser.add_argument('--run_seed_consistency', action='store_true', help='Perform SeedConsistency analysis')
    parser.add_argument('--save_path', type=str, help='Path to save the SeedConsistency results')
    parser.add_argument('--normalization', action='store_true', help='Apply TMM normalization if set to True, otherwise no normalization')

    args = parser.parse_args()

    # Split the comma-separated gene list into a list of strings
    genes_of_interest = args.geneOFinterest.split(',')

    PNdtwFE(args.input, genes_of_interest, args.threshold, args.desired_chunks, seed=args.seed, run_seed_consistency=args.run_seed_consistency, save_path=args.save_path, normalization=args.normalization)

def run_seedconsistency():
    parser = argparse.ArgumentParser(description='Run SeedConsistency analysis', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory containing the seed files')
    parser.add_argument('--save_path', type=str, required=True, help='Path to save the SeedConsistency results')

    args = parser.parse_args()
    calculate_distance_significance(args.output_dir, save_path=args.save_path)

if __name__ == "__main__":
    run_pndtwfe()