import pandas as pd
import sys
import argparse
import warnings 
warnings.filterwarnings('ignore')

def read_tsv(tsv_file):
    """
    Reads a TSV file and returns it as a Pandas DataFrame.
    """
    try:
        return pd.read_csv(tsv_file, sep='\t', index_col=0, header=0)
    except Exception as e:
        print(f"Error reading TSV file {tsv_file}: {e}")
        sys.exit(1)


def detect_real_variants(df):
    """
    Detects Real Variant without Artifacts
    """
    detected_variants = []
    for variant_name, samples in df.iterrows():
        for sample_name, freq in samples.items():
            if (0.05 < freq < 0.95) or (freq >= 0.98):
                detected_variants.append(f"{sample_name} - {variant_name}")
                
    return detected_variants

    
def main():
    """
    Main Function
    """
    parser = argparse.ArgumentParser(description="Collect SNPs without artifacts")
    parser.add_argument('tsv_file', type=str, help="Path to the TSV file")

    args = parser.parse_args()
    input_df = read_tsv(args.tsv_file)

    real_variants = detect_real_variants(input_df)
    for variant in real_variants:
        print(variant)


if __name__ == "__main__":
    main()