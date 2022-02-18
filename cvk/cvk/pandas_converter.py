import pandas


def pandas_converter(dataframe: pandas.DataFrame) -> list:
    return [data for data in dataframe.itertuples(index=False)]
