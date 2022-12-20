# Installation
Install required python packages *pandas* and *Flask*
```bash
pip install pandas
pip install Flask
```

# Run
To run server execute scritp

## Windows
```cmd
run.bat
```

## Linux/Mac
First time, make script executable (**Only first time**)
```bash
chmod +x run.sh
```
Then execute
```bash
./run.sh
```

# Resources
https://sparkbyexamples.com/pandas/pandas-groupby-count-examples/
https://datatables.net/examples/basic_init/data_rendering.html

# Docker

Build docker image:
```bash
docker build -t iocapp/iocapp .
```

Run
```bash
docker run -p 80:80 iocapp/iocapp
```