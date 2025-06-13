"""
Script to download RetailRocket e-commerce dataset files from Kaggle.

"""

import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_dataset():
    api = KaggleApi()
    api.authenticate()

    dataset = 'retailrocket/ecommerce-dataset'
    download_path = os.path.join(os.path.dirname(__file__))

    print("Downloading RetailRocket dataset to:", download_path)
    api.dataset_download_files(dataset, path=download_path, unzip=True)
    print("Download complete.")

if __name__ == "__main__":
    download_dataset()
