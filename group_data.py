import pandas as pd


def aggregate_results(df):
    final_df = {
        'Rate': round(df['interval'].max(), 2),
        'Max rate': df['rate'].max(),
        'Tip Pool Size': round(df['Tip Pool Size'].mean()),
        'Min Tip Pool Size': df['Tip Pool Size'].min(),
        'Max Tip Pool Size': df['Tip Pool Size'].max(),
        'Number of observations': round(df['rate'].count())
    }
    return pd.Series(final_df, index=['Rate', 'Max rate', 'Tip Pool Size', 'Min Tip Pool Size', 'Max Tip Pool Size',
                                      'Number of observations'])


def generate_interval(x):
    return round(int(x * 20) * 0.05, 2)


def group_data(results_df, filter_enabled):
    results = results_df.sort_values('rate', ascending=True)
    results["interval"] = results["rate"].apply(generate_interval)
    print("results shape", results.shape)
    if filter_enabled:
        filter_result = filter_outliers(results)
        results = results[filter_result]
        print("results filtered shape", results.shape)
    grouped_results = results.groupby(["interval"]).apply(aggregate_results)
    print("results grouped shape", grouped_results.shape)
    return grouped_results


def filter_outliers(df):
    max_tips_df = df.groupby(["interval"]).apply(get_max_tips)

    max_dict = {}  # dictionary of the maximum tip pool size for interval
    for index, row in max_tips_df.iterrows():
        max_dict[row['Rate']] = row['Max Tip Pool Size']

    # filter out the tip pool size outliers that are more than 200 far away
    filtered_df = df.apply(filter_condition, args=[max_dict], axis=1)

    return filtered_df


def filter_condition(row, max_dict):
    return abs(row['Tip Pool Size'] - max_dict[row['interval']]) <= 200


def get_max_tips(df):
    max_tips_df = {
        'Rate': df['interval'].max(),
        'Max Tip Pool Size': df['Tip Pool Size'].max(),
    }

    return pd.Series(max_tips_df, index=['Rate', 'Max Tip Pool Size'])





if __name__ == "__main__":
    DATA_PATH = "data"
    from read_data import read_data_exp
    results = read_data_exp(DATA_PATH)
    result = group_data(results, False)
    result_filtered = group_data(results, True)

