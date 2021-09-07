import pandas as pd


def aggregate_results(df):
    final_df = {
        'Rate': df['interval'].max(),
        'Max rate': df['rate'].max(),
        'Tip Pool Size': df['Tip Pool Size'].mean(),
        'Min Tip Pool Size': df['Tip Pool Size'].min(),
        'Max Tip Pool Size': df['Tip Pool Size'].max(),
        'Number of observations': df['rate'].count()
    }
    return pd.Series(final_df, index=['Rate', 'Max rate', 'Tip Pool Size', 'Min Tip Pool Size', 'Max Tip Pool Size',
                                      'Number of observations'])


def generate_interval(x):
    return int(x * 20) * 0.05


def group_data(results_df):
    grouped_results = results_df.sort_values('rate', ascending=True)
    grouped_results["interval"] = grouped_results["rate"].apply(generate_interval)
    grouped_results = grouped_results.groupby(["interval"]).apply(aggregate_results)

    return grouped_results


# TODO filter out the tip pool size outliers that are more than 200 far away
# from the maximum tip pool size for this interval
def filter_outliers(df):
    filtered_df = df
    return filtered_df


def save_data(df):
    df.to_csv('results.csv', index=False)


if __name__ == "__main__":
    DATA_PATH = "data"
    from read_data import read_data
    results = read_data(DATA_PATH)
    result = group_data(results)
    result.plot.bar(rot=0, y="Number of observations", x="rate", figsize=(15, 8))
