from confidence_interval import calculate_confidence
import pandas as pd
import os
import numpy as np

# analytical data generation
LAM = 20
H_SMALL = 1
H_LARGE = 40
ITERATIONS = 100


def read_data_exp(path_to_data):
    results_df = pd.DataFrame(columns=["totalMPS", "TPS", "rate", "Tip Pool Size"])
    dir_names = [x[0] for x in os.walk(path_to_data)]
    for subDir in dir_names:
        if subDir == os.path.join('.', path_to_data):
            continue
        file_names = [(root, files) for root, dirs, files in os.walk(subDir)]

        for experiment in file_names:
            mps_file, tips_file, times_file = get_filenames_in_exp(experiment)
            if mps_file == "" or tips_file == "" or times_file == "":
                continue
            df = read_mps_file(mps_file)
            tips_df = read_tips_file(tips_file)
            times_df = read_times_file(times_file)
            df = pd.merge(df, tips_df, on=['Time', 'Time'])
            results_df = process_experiment_data(times_df, df, results_df)
    return results_df


def process_experiment_data(param_df, data_df, results_df):
    for idx, row in param_df.iterrows():
        start_time = row['start']
        stop_time = row['stop'] + pd.Timedelta(seconds=10)
        test_df = data_df[(data_df["Time"] > start_time) & (data_df["Time"] < stop_time)]

        # take only data points close to max rate
        max_rate = test_df["Message Per Second"].max()
        test_df = test_df[abs(test_df["Message Per Second"] - max_rate) < max_rate * 0.2]

        # get observation with max tip pool size
        test_df_sorted_mps = test_df.sort_values('Message Per Second', ascending=False).head(1)
        # test_df_sorted_tips = test_df.sort_values('Tips', ascending=False).head(1)

        total_mps = test_df_sorted_mps["Message Per Second"].iloc[0]
        tps = test_df_sorted_mps["Transaction Per Second"].iloc[0]
        rate = round(tps / total_mps, 2)
        tips = test_df_sorted_mps["Tips"].max()

        results_df = results_df.append({"totalMPS": total_mps, "TPS": tps, "rate": rate, "Tip Pool Size": tips},
                                       ignore_index=True)
    return results_df


def get_filenames_in_exp(experiment):
    print("Next file", experiment[0], "\n")
    mps_file, tips_file, times_file = "", "", ""
    for file in experiment[1]:
        if file.startswith('Message'):
            mps_file = os.path.join(experiment[0], file)
        if file.startswith('Tips'):
            tips_file = os.path.join(experiment[0], file)
        if file.startswith('times'):
            times_file = os.path.join(experiment[0], file)
    return mps_file, tips_file, times_file


def read_mps_file(file):
    with open(file) as rf:
        df = pd.read_csv(rf, sep=',')
    df["Time"] = pd.to_datetime(df["Time"])
    df.columns = ["Time", "Message Per Second", "Transaction Per Second", "dRNG Message Per Second",
                  "Faucet Message Per Second", "Statements Per Second"]
    return df


def read_tips_file(file):
    with open(file) as rf:
        df = pd.read_csv(rf, sep=',')
    df["Time"] = pd.to_datetime(df["Time"])
    df.columns = ["Time", "Tips"]
    return df


def read_times_file(file):
    with open(file) as rf:
        df = pd.read_csv(rf, sep=',')
    df["start"] = pd.to_datetime(df["start"])
    df["stop"] = pd.to_datetime(df["stop"])
    df.columns = ["rate", "mps", "tps", "start", "stop"]
    return df


def load_sim_data(path, n_conf, conf_lvl):
    file_names = [os.path.join(x[0], x[2][0]) for x in os.walk(path) if not x[0] == path]
    corresponding_k = [int(x[0][-1]) for x in os.walk(path) if not x[0] == path]
    data_df_list = []
    for file_name in file_names:
        with open(file_name) as rf:
            df = pd.read_csv(rf, sep=',')
            df.columns = ["Rate", "col2", "col3", "TPS", "STD"]
            data_df_list.append(df)
    for df in data_df_list:
        df["Lower conf"] = df.apply(lambda row: row["TPS"] - row["STD"], axis=1)
        df["Higher conf"] = df.apply(lambda row: row["TPS"] + row["STD"], axis=1)
        # df["Lower conf"] = df.apply(apply_confidence, args=[n_conf, conf_lvl, "lower"], axis=1)
        # df["Higher conf"] = df.apply(apply_confidence, args=[n_conf, conf_lvl, "higher"], axis=1)

    return data_df_list, corresponding_k


def apply_confidence(row, n_conf, conf_lvl, flag=""):
    lower, higher, confidence = calculate_confidence(row["TPS"], n_conf, conf_lvl, row["STD"], row["TPS"])
    if flag == "lower":
        return lower
    if flag == "higher":
        return higher
    return confidence


def analytic_val(p, k):
    if p == 1:
        p = .999
    val = LAM * k / (k - 1) * (p * H_LARGE + (1 - p) * H_SMALL)
    for _ in range(ITERATIONS):
        val = LAM * H_SMALL + val / k / \
              (1 - p) * (1 - p * np.exp(-k * LAM * (1 - p) * (H_LARGE - H_SMALL) / val))
    return val


def generate_analytical_data(k):
    x = np.arange(100) / 100.
    y = analytic_vec(x, k)
    x_critical = H_LARGE * (k - 1) / (2 * H_SMALL + (k + 1) * H_LARGE)
    return x, y, x_critical


def analytic_vec(X, k):
    y = np.zeros(len(X))
    for i in range(len(X)):
        y[i] = analytic_val(X[i], k)
    return y


if __name__ == "__main__":
    DATA_PATH = "data-raw"
    # results = read_data_exp(DATA_PATH)
    SIM_PATH = "data-sim"
    dfs, ks = load_sim_data(SIM_PATH, 1000, 0.95)


