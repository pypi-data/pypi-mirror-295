# Hein HPLC - peak deconvolution and time course plot

## Description
This Dash web app aims to perform peak deconvolution without peak assignment or manual baseline correction. This app is developed by mainly referencing HPLC chromatograph. However, by modifying the default peak detection width, this app should be compatible with general peak analysis. It is also capable of processing multiple HPLC data and generating peak area over sample profile in csv.


## Installation - pip
```
pip install hein-hplc
```

## Usage
Run the app.py or use the command below. Click the url displayed in Terminal (default: [http://localhost:8050](http://localhost:8050)), upload .csv or .UV file to get started. Ctrl+C to stop the app.
```
hein-hplc
```


## Data format
### Chemstattion .UV
Support chemstation .UV file
### CSV
For data in .csv, column names are not required. For time course plot (example in [sample_data.csv](sample_data/sample_data.csv)), the column name should be TIME (HH:MM:SS).
You can append as many as columns with the same retention time scales.

| Retention Time minutes | 10:39:56 | 10:55:59 | 11:11:43 | ... |
|------------------------|----------|----------|----------|-----|
| 0.00125                | 0.42767  | 0.09733  | 0.02217  | ... |
| 0.00292                | 0.41933  | 0.086    | 0.01417  | ... |
| 0.00458                | ...      | ...      | ...      | ... |

## Authors
Ivory Zhang | Hein Lab ([ivoryzhang@chem.ubc.ca]())

## License

This project is licensed under the MIT License - see the [LICENSE](https://gitlab.com/heingroup/hein-hplc/-/blob/main/LICENSE) file for details.

## Publication
[v0.1.0](https://gitlab.com/heingroup/hein-hplc/-/tree/v0.1.0) 
was published in 

Liu, J.; Sato, Y.; Kulkarni, V. K.; Sullivan, A. I.; Zhang, W.; Crudden, C. M.; _Hein, J. E._ 
[Insights into the synthesis of NHC-stabilized Au nanoclusters through real-time reaction monitoring.](https://doi.org/10.1039/D3SC02077K)
Chem. Sci., 2023, 38(14), p. 10500-10507.

## App screenshot
![screenshot.png](https://gitlab.com/heingroup/hein-hplc/raw/main/screenshot.png)