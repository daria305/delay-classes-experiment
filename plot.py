from read_data import read_data_exp, load_sim_data, generate_analytical_data
from group_data import group_data
import matplotlib.pyplot as plt

DATA_PATH = "data-raw"
SIM_PATH = "data-sim"

# Graphs properties
LINE_WIDTH = 4
LINE_WIDTH_BLACK = 2
COLORS = ["lightblue", "orange", "red"]
FIG_SIZE = (16, 8)
MARKER_SIZE = 10

SMALL_SIZE = 11
MEDIUM_SIZE = 16
BIGGER_SIZE = 12

def save_results_to_csv(df, filename):
    df.to_csv(filename, index=True, header=False)


def plot_count_scatter(result, result_filtered):
    fig, ax = plt.subplots(2, 2)
    # count
    result.plot.bar(ax=ax[0, 0], y="Number of observations", x="Rate", figsize=FIG_SIZE)
    result_filtered.plot.bar(ax=ax[0, 1], y="Number of observations", x="Rate", figsize=FIG_SIZE, colormap="cubehelix")
    # scatter
    result.plot.scatter(ax=ax[1, 0], y="Tip Pool Size", x="Rate", figsize=FIG_SIZE)
    ax[1, 0].fill_between(result["Rate"], (result["Lower conf"]), (result["Higher conf"]), color='b', alpha=.1)

    result_filtered.plot.scatter(ax=ax[1, 1], y="Tip Pool Size", x="Rate", figsize=FIG_SIZE, colormap="cubehelix")
    ax[1, 1].fill_between(result_filtered["Rate"], (result_filtered["Lower conf"]), (result_filtered["Higher conf"]),
                          color='b', alpha=.1)

    plt.show()


def plot_exp_data(fig, ax, df, style="fill_between"):
    if style == "fill_between":
        ax.plot(df["Rate"], df["Tip Pool Size"], label="k=2", marker="+", markersize=MARKER_SIZE,
                linestyle="None", markeredgewidth=2, color="red")
        ax.fill_between(df["Rate"], (df["Lower conf"]), (df["Higher conf"]), color='k', alpha=.1)
    if style == "errorbar":
        ax.errorbar(df["Rate"], df["Tip Pool Size"], yerr=df["Higher conf"] - df["Tip Pool Size"], label="k=2",
                    marker=".", markersize=MARKER_SIZE, linestyle="None", markeredgewidth=3, color="red",
                    dash_capstyle="projecting", capsize=2)
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
    dfs, ks = load_sim_data(SIM_PATH, 100000, 0.99)

    for i, df in enumerate(dfs):
        k_label = "k=" + str(ks[i])
        ax.plot(df["Rate"], df["TPS"], linewidth=LINE_WIDTH, label=k_label, color=COLORS[i])
        ax.fill_between(df["Rate"], (df["Lower conf"]), (df["Higher conf"]), color=COLORS[2], linewidth=LINE_WIDTH)

    return fig, ax, ks


def plot_final_fig2(results_df, filename):
    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': MEDIUM_SIZE, "xtick.labelsize": SMALL_SIZE, "ytick.labelsize": SMALL_SIZE})  # must set in top

    fig, ax, ks = plot_sim_data(fig, ax)

    plot_analytical_data(fig, ax, ks)
    plt.xlabel("Proportion of value messages", fontsize=MEDIUM_SIZE)
    plt.ylabel("Tip pool size", fontsize=MEDIUM_SIZE)
    plt.legend(loc='best')

    plt.xlim([0, 1])
    plt.ylim([0, 1500])

    plt.savefig(filename + '_exp' + '.eps', format='eps')
    plt.show()

    fig, ax = plt.subplots()
    plt.rcParams.update({'font.size': MEDIUM_SIZE, "xtick.labelsize": SMALL_SIZE-1, "ytick.labelsize": SMALL_SIZE-1})  # must set in top

    plot_analytical_data(fig, ax, [2])
    plot_exp_data(fig, ax, results_df, style="errorbar")
    plt.xlabel("Proportion of value messages", fontsize=MEDIUM_SIZE)
    plt.ylabel("Tip pool size", fontsize=MEDIUM_SIZE)
    plt.xlim([0, 1])
    plt.ylim([0, 1500])
    plt.legend(loc='best')
    plt.savefig(filename + '_sim' + '.eps', format='eps')
    plt.show()


if __name__ == "__main__":
    results = read_data_exp(DATA_PATH)
    result = group_data(results, 0, 0)
    result_filtered = group_data(results, 200, 0.5)

    plot_count_scatter(result, result_filtered)

    plot_final_fig2(group_data(results, 200,  0.5), "final")
