EXTRACT_PATH="artifacts/data"


mkdir -p "$EXTRACT_PATH" 2>/dev/null


# Load and export .env
if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi

# Download data
echo "Downloading data..."
kaggle datasets download yelp-dataset/yelp-dataset -p artifacts/data

# Unzip data
unzip "$EXTRACT_PATH/yelp-dataset.zip" -d "$EXTRACT_PATH" && rm "$EXTRACT_PATH/yelp-dataset.zip"

echo "Unzipping data..."
echo "Done."
