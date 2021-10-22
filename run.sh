#!/bin/bash
conda env create -f environment.yml

python -m playwright install
python main.py
python download.py

rm data.json