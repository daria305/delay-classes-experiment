from read_data import read_data_exp
from group_data import group_data
import matplotlib.pyplot as plt

DATA_PATH = "data"


def save_results_to_csv(df, filename):
    df.to_csv(filename, index=True, header=False)


def plot_count_scatter(result, result_filtered):

    _, ax = plt.subplots(2, 2)
    # count
    result.plot.bar(ax=ax[0, 0], y="Number of observations", x="Rate", figsize=(15, 8))
    result_filtered.plot.bar(ax=ax[0, 1], y="Number of observations", x="Rate", figsize=(15, 8), colormap="cubehelix")
    # scatter
    result.plot.scatter(ax=ax[1, 0], y="Tip Pool Size", x="Rate", figsize=(15, 8))
    result_filtered.plot.scatter(ax=ax[1, 1], y="Tip Pool Size", x="Rate", figsize=(15, 8), colormap="cubehelix")
    plt.show()


if __name__ == "__main__":
    results = read_data_exp(DATA_PATH)
    result = group_data(results, False)
    result_filtered = group_data(results, True)

    plot_count_scatter(result, result_filtered)
    save_results_to_csv(result, "results_08-09.csv")
    save_results_to_csv(result_filtered, "result_filtered_08-09.csv")






