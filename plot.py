from read_data import read_data_exp, load_sim_data, generate_analytical_data
from group_data import group_data
import matplotlib.pyplot as plt

DATA_PATH = "data-raw"
SIM_PATH = "data-sim"

# Graphs properties
LINE_WIDTH = 4
LINE_WIDTH_BLACK = 2
COLORS = ["lightblue", "orange", "green"]


def save_results_to_csv(df, filename):
    df.to_csv(filename, index=True, header=False)


def plot_count_scatter(result, result_filtered):
    fig, ax = plt.subplots(2, 2)
    # count
    result.plot.bar(ax=ax[0, 0], y="Number of observations", x="Rate", figsize=(15, 8))
    result_filtered.plot.bar(ax=ax[0, 1], y="Number of observations", x="Rate", figsize=(15, 8), colormap="cubehelix")
    # scatter
    result.plot.scatter(ax=ax[1, 0], y="Tip Pool Size", x="Rate", figsize=(15, 8))
    ax[1, 0].fill_between(result["Rate"], (result["Lower conf"]), (result["Higher conf"]), color='b', alpha=.1)

    result_filtered.plot.scatter(ax=ax[1, 1], y="Tip Pool Size", x="Rate", figsize=(15, 8), colormap="cubehelix")
    ax[1, 1].fill_between(result_filtered["Rate"], (result_filtered["Lower conf"]), (result_filtered["Higher conf"]),
                          color='b', alpha=.1)

    plt.show()


def plot_exp_data(fig, ax, df):
    ax.plot(df["Rate"], df["Tip Pool Size"], label="k=2, Exp", marker="+", markersize=14,
            linestyle="None", markeredgewidth=2, color="red")
    ax.fill_between(df["Rate"], (df["Lower conf"]), (df["Higher conf"]), color='k', alpha=.1)

    # ax.errorbar(df["Rate"], df["Tip Pool Size"], yerr=df["Higher conf"] - df["Tip Pool Size"], label="k=2, Exp",
    #             marker=".", markersize=14, linestyle="None", markeredgewidth=2, color="red")
    return fig, ax


def plot_analytical_data(fig, ax, ks):
    not_added_label = True
    for k in ks:
        x, y, _ = generate_analytical_data(k)
        if not_added_label:
            ax.plot(x, y, linewidth=LINE_WIDTH_BLACK, label="Analytical", color="black", linestyle="dashed")
            not_added_label = False
        else:
            ax.plot(x, y, linewidth=LINE_WIDTH_BLACK, color="black", linestyle="dashed")

    return fig, ax


def plot_sim_data(fig, ax):
    dfs, ks = load_sim_data(SIM_PATH)

    for i, df in enumerate(dfs):
        k_label = "k=" + str(ks[i]) + ", Sim"
        ax.plot(df["Rate"], df["TPS"], linewidth=LINE_WIDTH, label=k_label, color=COLORS[i])

    return fig, ax, ks


def plot_final_fig2(results_df, plot_title):
    fig, ax = plt.subplots()
    fig, ax, ks = plot_sim_data(fig, ax)
    fig, ax = plot_exp_data(fig, ax, results_df)

    plot_analytical_data(fig, ax, ks)

    plt.xlabel("Proportion of value messages")
    plt.ylabel("Tip pool size")
    plt.xlim([0, 1])
    plt.ylim([0, 1400])
    plt.legend(loc='best')
    plt.title(plot_title)
    plt.savefig(plot_title + '.pdf', format='pdf')
    plt.show()


if __name__ == "__main__":
    results = read_data_exp(DATA_PATH)
    result = group_data(results, 0, 0)
    result_filtered = group_data(results, 200, 0)

    plot_count_scatter(result, result_filtered)

    plot_final_fig2(group_data(results, 0,  0.5), "No filtering")
    plot_final_fig2(group_data(results, 400, 0.5), "filter 400")
    plot_final_fig2(group_data(results, 350,  0.5), "filter 350")
    plot_final_fig2(group_data(results, 200,  0.5), "filter 200")
