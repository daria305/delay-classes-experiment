import statistics

# Obs: Please make sure your points are independent!!!!
# So either generate the points from different simulations or
# calculate the correlation time and sample points apart enough from each other.


def calculate_confidence(df_col, n, confidence):
    sample_average = df_col.mean()
    sample_std = df_col.std()
    standard_error = sample_std / n ** 0.5

    # If the error bars you want to build are supposed to be around an estimation of an AVERAGE,
    # the error bar goes from lower_limit to higher_limit, where
    s = statistics.NormalDist(mu=0, sigma=1).inv_cdf(1 - (1 - confidence) / 2)
    confidence = s * standard_error
    lower_limit = sample_average - confidence
    higher_limit = sample_average + confidence
    # print("n", n, "sample_average", sample_average, "conf", confidence)

    return lower_limit, higher_limit


