import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()
# Import edgeR package from R
ro.r('library(edgeR)')

def tmm_normalization(counts_df):
    # Convert the pandas DataFrame to an R dataframe
    counts_r_df = pandas2ri.py2rpy(counts_df)
    
    # Create DGEList object
    ro.globalenv['counts'] = counts_r_df
    ro.r('dge <- DGEList(counts=counts)')
    
    # Calculate normalization factors using TMM
    ro.r('dge <- calcNormFactors(dge, method="TMM")')
    ro.r('print(dge)')
    # Save the dge object to a file
    ro.r('write.csv(as.data.frame(dge$samples$norm.factors), file="normalization_factors.csv")')
    # Apply the normalization factors to the counts and return as a dataframe
    ro.r('normalized_counts <- as.data.frame(cpm(dge, normalized.lib.sizes=TRUE))')
    
    # Convert the normalized counts back to a pandas DataFrame
    normalized_counts_df = pandas2ri.rpy2py_dataframe(ro.globalenv['normalized_counts'])
    
    return normalized_counts_df


def manual_tmm_normalization(counts_df):
    # Convert the pandas DataFrame to an R dataframe
    counts_r_df = pandas2ri.py2rpy(counts_df)
    
    # Create DGEList object in R
    ro.globalenv['counts'] = counts_r_df
    ro.r('dge <- DGEList(counts=counts)')
    
    # Calculate normalization factors using TMM
    ro.r('dge <- calcNormFactors(dge, method="TMM")')
    
    # Extract normalization factors
    norm_factors = ro.r('dge$samples$norm.factors')
    
    # Normalize the factors by dividing by their mean
    ro.globalenv['norm_factors'] = norm_factors
    ro.r('norm_factors <- norm_factors / mean(norm_factors)')
    
    # Calculate effective library sizes
    ro.globalenv['rawdat'] = counts_r_df
    ro.r('effective.libsizes <- colSums(rawdat) * norm_factors')
    
    # Apply the normalization manually
    ro.r('normalized_counts <- sweep(rawdat, 2, mean(effective.libsizes) / effective.libsizes, "*")')
    
    # Round the normalized counts to one decimal place
    ro.r('normalized_counts <- round(normalized_counts, 1)')
    
    # Convert the normalized counts back to a pandas DataFrame
    normalized_counts_df = pandas2ri.rpy2py_dataframe(ro.globalenv['normalized_counts'])
    
    return normalized_counts_df



#normalized_counts_df = manual_tmm_normalization(df35)
#print(normalized_counts_df)