from collections import Counter
import pandas


def read_file(file):
    df = pandas.read_excel(file)
    return df
    # Store each column as a seperate dictionary


def get_cols(data):
    return data.columns.ravel()


def get_col_data(col, data):
    return data[col].tolist()


def matches(data):
    # Collections.counter
    # Each match is a value of 1
    return Counter(data)


def merge_values(val1, val2, val3, val4):
    val1 = 0 if val1 is None else val1
    val2 = 0 if val2 is None else val2
    val3 = 0 if val3 is None else val3
    val4 = 0 if val4 is None else val4
    return [val1, val2, val3, val4]


if __name__ == "__main__":
    file = "data.xlsx"
    data = read_file(file)
    cols = get_cols(data)

    hits = Counter()

    print("Getting matches")

    for col in cols:
        hits += matches(get_col_data(col, data))

    #matches_df = matches_df.sort_values(by=['Hits'], ascending=False)

    dataset1 = {}
    dataset2 = {}
    dataset3 = {}

    for key, val in hits.items():
        dataset1[key] = (data[cols[0]] == key).sum()
        dataset2[key] = (data[cols[1]] == key).sum()
        dataset3[key] = (data[cols[2]] == key).sum()
    
    final_dataset = {
    key: merge_values(hits.get(key), dataset1.get(key), dataset2.get(key), dataset3.get(key))
    for key in set(hits).union(dataset1, dataset2, dataset3)
}

    final_dataset_lst = []
    for key, val in final_dataset.items():
        final_dataset_lst.append((key, val[0], val[1], val[2], val[3]))
    
    print("Saving results")
    matches_df = pandas.DataFrame(final_dataset_lst, columns=['Gene', 'Total Hits', cols[0], cols[1], cols[2]])
    writer = pandas.ExcelWriter('raw_matches.xlsx', engine='xlsxwriter')
    matches_df.to_excel(writer)
    writer.save()

    
