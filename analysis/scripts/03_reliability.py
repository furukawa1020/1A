import argparse
import math
from common import SCALE_ITEMS, read_rows, to_float, write_rows


def covariance_matrix(data):
    n = len(data)
    p = len(data[0])
    means = [sum(row[col] for row in data) / n for col in range(p)]
    matrix = []
    for i in range(p):
        line = []
        for j in range(p):
            value = sum((row[i] - means[i]) * (row[j] - means[j]) for row in data) / (n - 1)
            line.append(value)
        matrix.append(line)
    return matrix


def cronbach_alpha(matrix):
    p = len(matrix)
    total_variance = sum(matrix[i][j] for i in range(p) for j in range(p))
    item_variance = sum(matrix[i][i] for i in range(p))
    if p <= 1 or total_variance <= 0:
        return math.nan
    return (p / (p - 1)) * (1 - item_variance / total_variance)


def first_eigen(matrix, iterations=200):
    p = len(matrix)
    vector = [1 / math.sqrt(p)] * p
    for _ in range(iterations):
        next_vector = [sum(matrix[i][j] * vector[j] for j in range(p)) for i in range(p)]
        norm = math.sqrt(sum(value * value for value in next_vector))
        if norm == 0:
            break
        vector = [value / norm for value in next_vector]
    eigenvalue = sum(vector[i] * sum(matrix[i][j] * vector[j] for j in range(p)) for i in range(p))
    return eigenvalue, vector


def omega_total_approx(matrix):
    eigenvalue, vector = first_eigen(matrix)
    if eigenvalue <= 0:
        return math.nan
    loadings = [component * math.sqrt(eigenvalue) for component in vector]
    true_score_variance = sum(loadings) ** 2
    unique_variance = 0
    for index, loading in enumerate(loadings):
        unique_variance += max(matrix[index][index] - loading * loading, 0)
    denominator = true_score_variance + unique_variance
    if denominator <= 0:
        return math.nan
    return true_score_variance / denominator


def complete_item_matrix(rows, items):
    matrix = []
    for row in rows:
        values = [to_float(row.get(item)) for item in items]
        if all(not math.isnan(value) for value in values):
            matrix.append(values)
    return matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output", nargs="?", default="analysis/outputs/reliability.csv")
    args = parser.parse_args()

    rows = read_rows(args.input)
    results = []
    for scale, items in SCALE_ITEMS.items():
        matrix_data = complete_item_matrix(rows, items)
        if len(matrix_data) < 3:
            alpha = math.nan
            omega = math.nan
        else:
            cov = covariance_matrix(matrix_data)
            alpha = cronbach_alpha(cov)
            omega = omega_total_approx(cov)
        results.append(
            {
                "scale": scale,
                "n_observations": len(matrix_data),
                "cronbach_alpha": "" if math.isnan(alpha) else f"{alpha:.4f}",
                "omega_total_one_factor_approx": "" if math.isnan(omega) else f"{omega:.4f}",
                "note": "Omega is a one-factor approximation from the first covariance eigenvector.",
            }
        )

    write_rows(args.output, results)
    print(f"Wrote reliability results to {args.output}")


if __name__ == "__main__":
    main()

