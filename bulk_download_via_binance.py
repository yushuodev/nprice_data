import os
import glob
import pandas as pd
from binance_bulk_downloader.downloader import BinanceBulkDownloader
import argparse

def bulk_dl():
    downloader = BinanceBulkDownloader(data_type="metrics", asset="um")
    downloader.run_download()

def data_process(ticker):
    csv_dir = f'./data/futures/um/daily/metrics/{ticker}'
    output_file = f'{ticker}_metrics.csv'

    file_pattern = os.path.join(csv_dir, f'{ticker}-metrics-*.csv')
    file_list = glob.glob(file_pattern)

    dfs = []
    for file in file_list:
        df = pd.read_csv(file)
        dfs.append(df)

    process_df = pd.concat(dfs, ignore_index=True)
    process_df.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, default="BTCUSDT", help="Ticker that will download")

    args = parser.parse_args()
    coin = args.ticker

    if not (os.path.isdir(".\data")):
        print("No bulk data, downloading...")
        bulk_dl()

    print("bulk download completed, processing data...")
    data_process(coin)

