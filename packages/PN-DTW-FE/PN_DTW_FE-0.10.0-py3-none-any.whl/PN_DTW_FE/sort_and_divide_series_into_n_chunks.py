import pandas as pd
def sort_and_divide_series_into_n_chunks(series, total_chunks):
    """
    Sorts a pandas Series in descending order and divides it into a specified number of chunks,
    preserving the index.
    
    Parameters:
    - series: A pandas Series to sort and divide.
    - total_chunks: The desired total number of chunks.
    
    Returns:
    - A list of pandas Series, each representing a chunk.
    """
    # Step 1: Sort the series in descending order while preserving the index
    sorted_series = series.sort_values(ascending=False)
    
    # Calculate the size of each chunk
    n = len(sorted_series)
    chunk_size = max(n // total_chunks, 1)  # Ensure at least one element per chunk
    
    # Determine the number of chunks that will have an extra element
    extra = n % total_chunks
    
    chunks = []
    start_index = 0
    for i in range(total_chunks):
        # Chunks with an extra element
        if i < extra:
            end_index = start_index + chunk_size + 1
        else:
            end_index = start_index + chunk_size
        # Use iloc to preserve the original index of each chunk
        chunks.append(sorted_series.iloc[start_index:end_index])
        start_index = end_index
    
    return chunks