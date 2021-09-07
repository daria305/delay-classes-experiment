from read_data import read_data
from group_data import group_data

DATA_PATH = "data"

# TODO plots...


if __name__ == "__main__":
    results = read_data(DATA_PATH)
    results = group_data(results)
    # print(results.head())
    # fig = results.plot.bar(rot=0, y="Number of observations", x="Rate", figsize=(15, 8))





