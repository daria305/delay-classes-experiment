import statistics

# Obs: Please make sure your points are independent!!!!
# So either generate the points from different simulations or
# calculate the correlation time and sample points apart enough from each other.

# INSERT HERE THE DATA FROM THE SIMULATION/EXPERIMENT
data = [1, 2, 3, 1, 2, 3]
# INSERT HERE THE CONFIDENCE YOU WANT
confidence = 0.95

N = len(data)
if N <=1:
  print("The sample is too small")

# Average and standard deviation from the sample
sample_average = sum(data)/N
sample_variance = sum([(data[i]-sample_average)**2 for i in range(N)])/(N-1)
sample_sd = (sample_variance)**0.5
standard_error = sample_sd/(N)**0.5

# If the error bars you want to build are supposed to be around an estimation of an AVERAGE,
# the error bar goes from lower_limit to higher_limit, where

s = statistics.NormalDist(mu=0, sigma=1).inv_cdf(1-(1-confidence)/2)
lower_limit = sample_average - s*standard_error
higher_limit = sample_average + s*standard_error