import statistics

# Obs: Please make sure your points are independent!!!!
# So either generate the points from different simulations or
# calculate the correlation time and sample points apart enough from each other.


def calculate_confidence(df_col, n, confidence, std=0, avg=0):
    sample_std = std
    sample_average = avg
    if std == 0:
        sample_std = df_col.std()
    if avg == 0:
        sample_average = df_col.mean()

    standard_error = sample_std / n ** 0.5

    # If the error bars you want to build are supposed to be around an estimation of an AVERAGE,
    # the error bar goes from lower_limit to higher_limit, where
    s = statistics.NormalDist(mu=0, sigma=1).inv_cdf(1 - (1 - confidence) / 2)
    lower_limit = sample_average - s * standard_error
    higher_limit = sample_average + s * standard_error
    # print("n", n, "sample_average", sample_average, "conf", confidence)

    return lower_limit, higher_limit, confidence

