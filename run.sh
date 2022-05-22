echo "Installing packages..."
# Install python3
sudo apt update
sudo apt install python3
# Install pip
sudo apt install python3-pip

echo "Downloading word list file..."
# Download word list
./src/download_wordlist.sh

echo "Start crawling script..."
# Start crawling
python3 ./src/crawler.py
