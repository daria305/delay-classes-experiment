import pandas as pd
from confidence_interval import calculate_confidence


def aggregate_results(df):
    # print("col for rate", round(df['interval'].max(), 2))
    n = len(df['Tip Pool Size'])
    lower_limit, higher_limit, confidence = calculate_confidence(df['Tip Pool Size'], n, 0.95)
    final_df = {
        'Rate': round(df['interval'].max(), 2),
        'Max rate': df['rate'].max(),
        'Tip Pool Size': round(df['Tip Pool Size'].mean()),
        'Min Tip Pool Size': df['Tip Pool Size'].min(),
        'Max Tip Pool Size': df['Tip Pool Size'].max(),
        'Number of observations': round(df['rate'].count()),
        'Lower conf': lower_limit,
        'Higher conf': higher_limit,
        'Confidence %': round(confidence/df['Tip Pool Size'].mean()*100, 2)
    }
    return pd.Series(final_df, index=['Rate', 'Max rate', 'Tip Pool Size', 'Min Tip Pool Size', 'Max Tip Pool Size',
                                      'Number of observations', 'Lower conf', 'Higher conf', 'Confidence %'])


def generate_interval(x):
    return round(int(x * 20) * 0.05, 2)


def group_data(results_df, filter_threshold, start_filter_rate):
    results = results_df.sort_values('rate', ascending=True)
    results["interval"] = results["rate"].apply(generate_interval)
    if filter_threshold > 0:
        filter_result = filter_outliers(results, filter_threshold, start_filter_rate)
        results = results[filter_result]
    grouped_results = results.groupby(["interval"]).apply(aggregate_results)
    # print("results grouped shape", grouped_results.shape)
    return grouped_results


def filter_outliers(df, filter_threshold, start_filter_rate):
    max_tips_df = df.groupby(["interval"]).apply(get_max_tips)

    max_dict = {}  # dictionary of the maximum tip pool size for interval
    for index, row in max_tips_df.iterrows():
        max_dict[row['Rate']] = row['Max Tip Pool Size']

    # filter out the tip pool size outliers that are more than 200 far away
    filtered_df = df.apply(filter_condition, args=[max_dict, filter_threshold, start_filter_rate], axis=1)

    return filtered_df


def filter_condition(row, max_dict, filter_threshold, start_filter_rate):
    if row['interval'] > start_filter_rate:
        return abs(row['Tip Pool Size'] - max_dict[row['interval']]) <= filter_threshold
    return True


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
    result = group_data(results, 0, 0)
    result_filtered = group_data(results, 100, 0)

