"""Main module."""
import os
import sys
import argparse

sys.path.insert(0, os.path.abspath(".."))

from quant_trading.datasets.stock_dataset import StockDataset
from quant_trading.datasets import preprocessor


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-date",
        dest="start_date",
        default="2015-01-01",
        help="extracts data from the specified start-date (default: 2015-01-01)",
    )
    parser.add_argument(
        "--end-date",
        dest="end_date",
        default="2015-12-01",
        help="extracts data until the specified end-date, (default: 2015-12-01)",
    )
    parser.add_argument(
        "--do-extract-save",
        dest="do_extract_save",
        action="store_true",
        help="extracts and saves the pulled range to csv file",
    )
    parser.add_argument(
        "--do-extract-from-file",
        dest="do_extract_from_file",
        action="store_true",
        help="extracts the pulled range data from csv file",
    )

    return parser.parse_args()


def run(args):
    stock_data = StockDataset()
    start_date = args.start_date
    end_date = args.end_date

    if args.do_extract_save:
        symbols = None
        indicators = ["Close"]

        print("Extract from {} to {}...".format(start_date, end_date))
        df = stock_data.extract_range(start_date, end_date, indicators, symbols)
        print(df.head())

        print("Save to csv file...")
        stock_data.output_writer(df, f"data-{start_date}_{end_date}.csv")

    if args.do_extract_from_file:
        print("Read from csv file...")
        df = stock_data.output_reader(f"data-{start_date}_{end_date}.csv")
        print(df.head())

        X_train, y_train, X_test, y_test = preprocessor.run(df)
        print(f"X_train: {type(X_train)}, y_train: {type(y_train)}")
        print(X_train.shape, y_train.shape)  # (486, 977, 30, 1) (486, 977, 1)
        print(f"X_test: {type(X_test)}, y_test: {type(y_test)}")
        print(X_test.shape, y_test.shape)  # (486, 222, 30, 1) (486, 222, 1)


if __name__ == "__main__":
    args = parse_args()

    run(args)
