echo "Installing packages..."
# Install python3
sudo apt update
sudo apt install python3
# Install pip
sudo apt install python3-pip

echo "Installing python packages..."
# PIP
pip install -r requirements.txt

echo "Start crawling script..."
# Start crawling
python3 ./src/crawler.py

echo "Start preprocessing script..."
python3 ./src/preprocessing.py

echo "Start noise generator script..."
# Add the script here
python3 ./src/noise_generation.py

echo "Start statistics script..."
python3 ./src/statistics.py

