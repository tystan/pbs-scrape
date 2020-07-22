# pbs-scrape
Python script to web scrape the PBS item code descriptions

## Background
The Pharmaceutical Benefits Scheme (PBS) in Australia has a "schedule" of subsidised drugs. The list of these pharmaceuticals, identified by their `item_code` (with corresponding drug description) can be found on [this PBS webpage](https://www.pbs.gov.au/info/statistics/dos-and-dop/dos-and-dop) (look for the link [PBS item drug map (CSV xxx KB)](https://www.pbs.gov.au/statistics/dos-and-dop/files/pbs-item-drug-map.csv)).

However, the `item_code` descriptions in the above file can differ from those on the website [pbs.gov.au](https://www.pbs.gov.au)!

For example, `item_code="1975Y"`has differing descriptions:

| `item_code`  | Description  | Source  |
|---|---|---|
| `01975Y`  | QUININE Tablet containing quinine sulfate dihydrate 300 mg  | [PBS item drug map (CSV)](https://www.pbs.gov.au/statistics/dos-and-dop/files/pbs-item-drug-map.csv)  |
| `1975Y`  | QUININE quinine sulfate dihydrate 300 mg tablet, 50  | [pbs website](https://www.pbs.gov.au/medicine/item/1975y)  |

Although the above descriptions are roughly equivalent, the PBS supplied CSV has no indication of quantity while the PBS website associates the `item_code="1975Y"` with a pack of 50 tablets.

In many use cases of this information, pack size is important. I have written a Python script to add pack size specifically to the [PBS item drug map (CSV)](https://www.pbs.gov.au/statistics/dos-and-dop/files/pbs-item-drug-map.csv) file


## Usage

In `bash`/`cmd.exe`/`Terminal` run:
```bash
cd /location/of/downloaded/files
python3 pbs-item-code-descrip-scrape.py
```

The above assumes that the file `drug-items-list.scv` is in the same directory as `pbs-item-code-descrip-scrape.py`. You can of course substitute `drug-items-list.scv` with the most current version of [PBS item drug map (CSV)](https://www.pbs.gov.au/statistics/dos-and-dop/files/pbs-item-drug-map.csv) that you have downloaded.

### Output

A file `pbs-list-plus-web-decrip.csv` that is the input CSV file with the additional information found online appended to the `item_code` description field.

