import pandas as pd
import numpy as np
from scipy.stats import shapiro
def optimize_chunks_for_normality_pandas(series_list, num_new_chunks, seed, random):
    # Concatenate and shuffle series while preserving indices
    combined_series = pd.concat(series_list)
    shuffled_series = combined_series.sample(frac=1, random_state=random)

    # Calculate chunk sizes and split into new chunks
    total_elements = len(shuffled_series)
    chunk_sizes = [total_elements // num_new_chunks + (1 if i < total_elements % num_new_chunks else 0) for i in range(num_new_chunks)]
    new_chunks = [shuffled_series.iloc[start_idx:start_idx + size].reset_index() for start_idx, size in zip(np.cumsum([0] + chunk_sizes[:-1]), chunk_sizes)]

    best_score = -np.inf
    np.random.seed(seed)
    for _ in range(10000):  # Iteration limit for optimization attempts
        for n in range(len(new_chunks)):
            # Randomly select two chunks to swap a single element between
            i, j = np.random.randint(0, len(new_chunks), size=2)
            
            if len(new_chunks[i]) > 3 and len(new_chunks[j]) > 3:
                # Randomly select indices within each chunk to swap
                a, b = np.random.randint(0, len(new_chunks[i]), size=1)[0], np.random.randint(0, len(new_chunks[j]), size=1)[0]
                
                # Swap the elements (both "index" and value columns)
                new_chunks[i].iloc[a], new_chunks[j].iloc[b] = new_chunks[j].iloc[b].copy(), new_chunks[i].iloc[a].copy()
                
                # Check if swaps improved normality
                current_scores = [shapiro(chunk.drop(columns=chunk.columns[0]))[1] for chunk in new_chunks if len(chunk) > 3]
                current_score = np.mean(current_scores)
                
                if current_score > best_score:
                    best_score = current_score
                else:
                    # Revert swap if it didn't improve
                    new_chunks[i].iloc[a], new_chunks[j].iloc[b] = new_chunks[j].iloc[b].copy(), new_chunks[i].iloc[a].copy()
    
    # Convert the first column back to index for each chunk
    optimized_chunks = [chunk.set_index(chunk.columns[0]) for chunk in new_chunks]

    # Combine optimized chunks back into a single series, preserving original indices
    #optimized_series = pd.concat(optimized_chunks).sort_index()
    
    return optimized_chunks, best_score