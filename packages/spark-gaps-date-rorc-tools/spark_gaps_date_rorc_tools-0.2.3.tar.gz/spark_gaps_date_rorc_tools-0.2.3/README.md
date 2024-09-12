# spark_gaps_date_rorc_tools


[![Github License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Updates](https://pyup.io/repos/github/woctezuma/google-colab-transfer/shield.svg)](pyup)
[![Python 3](https://pyup.io/repos/github/woctezuma/google-colab-transfer/python-3-shield.svg)](pyup)
[![Code coverage](https://codecov.io/gh/woctezuma/google-colab-transfer/branch/master/graph/badge.svg)](codecov)




spark_gaps_date_rorc_tools is a Python library that implements get gaps dates
## Installation

The code is packaged for PyPI, so that the installation consists in running:
```sh
pip install spark-gaps-date-rorc-tools 
```


## Usage

wrapper take gaps dates

```sh
config.yaml
===========
  conf:
    t_psan_test:
      table_path: "/data/master/psan/data/t_psan_test/"
      supplies : [
          "/data/master/psan/data/t_ksag_test/",
          "/data/master/psan/data/t_psan_test/"
      ]
    t_kctk_cust_rating_atrb:
      table_path: ""
      supplies : []



example1: file.py
=================
from spark_gaps_date_rorc_tools import show_gaps_date
df_pivot = show_gaps_date(spark=spark,
                          config_path_name="config.yaml",
                          table_rorc=["t_psan_xxx"]
                          hdfs_uri="hdfs://pedaaslive.scmx2p100.isi",
                          filter_date_initial="202101",
                          filter_date_final="202112")

Spark Style Dataframe: file.py
==============================                     
df_pivot.show2(limit=10)



Pandas Style Dataframe: file.py
==============================                 
df_pivot2 = df_pivot.toPandas()                      
df_pivot2.show2()

```

## License

[Apache License 2.0](https://www.dropbox.com/s/8t6xtgk06o3ij61/LICENSE?dl=0).


## New features v1.0

 
## BugFix
- choco install visualcpp-build-tools



## Reference

 - Jonathan Quiza [github](https://github.com/jonaqp).
 - Jonathan Quiza [RumiMLSpark](http://rumi-ml.herokuapp.com/).
 - Jonathan Quiza [linkedin](https://www.linkedin.com/in/jonaqp/).
