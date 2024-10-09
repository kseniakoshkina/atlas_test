import sys
import numpy as np
from scipy.stats import norm
import argparse
import csv
import warnings 
warnings.filterwarnings('ignore')


def read_tsv(tsv_file):
    """
    Reads a TSV file and returns it as a NumPy array.
    """
    try:
        matrix_stab = []
        with open(tsv_file, 'r') as tsv_in:
            reader = csv.reader(tsv_in, delimiter='\t')
            for item in reader:
                matrix_stab.append(item)
        
        matrix_stab = np.array(matrix_stab, dtype=float)
        return matrix_stab
    except Exception as e:
        print(f"Error reading TSV file {tsv_file}: {e}")
        sys.exit(1)


def read_vector(vector_file):
    """
    Reads a vector file and returns it as a NumPy array.
    """
    try:
        with open(vector_file, 'r') as vector_in:
            vector = vector_in.read().splitlines()
        
        vector = np.array(vector, dtype=float)
        return vector
    except Exception as e:
        print(f"Error reading vector file {vector_file}: {e}")
        sys.exit(1)


def find_probability(matrix, input_vector):
    """
    Finds the average probability of the input vector values based on the 
    cumulative distribution function (CDF) of the normal distribution derived 
    from the matrix.
    """
    mean = np.mean(matrix, axis=1)
    std = np.std(matrix, axis=1)

    z_scores = (input_vector - mean) / std
    probabilities = norm.cdf(z_scores)
    probabilities = probabilities[~np.isnan(probabilities)]

    return round(probabilities.mean(),3)


def analyze_microsatellite_stability(matrix, input_vector):
    """
    Analyzes the stability of microsatellites by comparing the input vector values 
    to a threshold of the mean + 3 standard deviations of each row in the matrix.
    """
    mean = np.mean(matrix, axis=1)
    std = np.std(matrix, axis=1)
    thresholds = mean + (3 * std)

    unstable_count = 0
    total_loci = len(input_vector)

    for i, value in enumerate(input_vector):
        if value > thresholds[i]:
            unstable_count += 1

    fraction_unstable = unstable_count / total_loci

    stability_status = 'Нестабильный' if fraction_unstable >= 0.2 else 'Стабильный'

    return stability_status


def main():
    """
    Main Function
    """
    parser = argparse.ArgumentParser(description="Run analysis on microsatellite stability \
    or find minimum confidence.")
    parser.add_argument('-f', '--function', 
                        choices=['analyze_microsatellite_stability', 'find_probability'], 
                        required=True, 
                        help="Select the function to execute")
    parser.add_argument('matrix_file', type=str, help="Path to the TSV file")
    parser.add_argument('vector_file', type=str, help="Path to the vector file")

    args = parser.parse_args()

    input_matrix = read_tsv(args.matrix_file)
    input_vector = read_vector(args.vector_file)
    
    if args.function == "analyze_microsatellite_stability":
        value = analyze_microsatellite_stability(input_matrix, input_vector)
        print(value)
    elif args.function == "find_probability":
        conf = find_probability(input_matrix, input_vector)
        print(conf)

    if len(input_matrix) != len(input_vector):
        print("Error: The matrix and vector lengths do not match.")
        sys.exit(1)


if __name__ == "__main__":
    main()