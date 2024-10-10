# DS2002-Data-Project-1

This project was done in combination with Shevya Panda (pmu4rr).

### This project requires a python venv with python3.11 to run it correctly

To create said venv, ensure you have python3.11 installed, navigate to the project directory on your terminal, and run:

```
python3.11 -m venv venv
```

After this is done running, run this command in your terminal to activate the environment (Unix)

```
source venv/bin/activate
```

For Windows (PSL), run

```
.\venv\Scripts\Activate.ps1
```

Then, finally, run

```
pip install -r requirements.txt
```

To run the ETL pipeline, just run

```
python3 run.py
```

And follow the instructions!

All output data will be in the output subfolder. If this folder does not exist, the pipeline will not work.

A list of cryptocurrencies can be found [here](https://coinmarketcap.com/all/views/all/).
