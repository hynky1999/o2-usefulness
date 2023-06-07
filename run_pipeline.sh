python -m etl.run --config etl_config.json && \
python -m nbconvert --to html --no-input --execute --output-dir=reports/ --output=report.html explore/exploration.ipynb
