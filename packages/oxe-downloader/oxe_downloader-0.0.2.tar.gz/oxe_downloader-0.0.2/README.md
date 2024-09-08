# Downloader for Open-X Embodiment Datasets

An unofficial downloader for [Open-X Embodiment Datasets](https://robotics-transformer-x.github.io/).

This README will guide through downloading the Open-X Embodiment Datasets.

## Download the datasets

1. Check available datasets and their corresponding metadata in [the dataset spreadsheet](https://docs.google.com/spreadsheets/d/1rPBD77tk60AEIGZrGSODwyyzs5FgCU9Uz3h-3_t2A9g/edit#gid=0)
* **Warning** The images in `utokyo_saytap_converted_externally_to_rlds` seem to be corrupted.
2. After installing with something like `pip install -e .` use dataset_download --help for usage details. By default, the Python script will download all 53 datasets, amounting to a total size of approximately 4.5TB.
3. Follow [this guide](https://cloud.google.com/storage/docs/gsutil_install#linux) to setup `gsutil`
4. Start downloading to `~/oxe/`:
    ```
    oxe_download -p ~/oxe/
    ```

This section was last updated on 9/8/2024.

## Install the tool

1. Install python dependencies
    ```
    pip install -r requirements.txt
    ```
2. Install the package

    ```
    pip install -e .
    ```

## Acknowledgment

See original acknowledgment [here](https://github.com/LostXine/open_x_pytorch_dataloader).
