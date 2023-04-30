#!/bin/bash
cd /opt/nodemonitor/ 
pip3 install virtualenv
virtualenv venv
source venv/bin/activate

update_script() {
    echo "Updating start.sh from the repository..."
    curl -O https://raw.githubusercontent.com/underskys/nodemonitor/main/start.sh
    chmod +x start.sh
}

download_files() {
    echo "Downloading bot.py from the repository..."
    curl -O https://raw.githubusercontent.com/underskys/nodemonitor/main/bot.py

    echo "Downloading version.py from the repository..."
    curl -O https://raw.githubusercontent.com/underskys/nodemonitor/main/version.py
}

if [ "$1" == "update" ]; then
    update_script
    download_files
    exit 0
fi

if [ ! -f "./bot.py" ]; then
    download_files
fi

curl -O https://raw.githubusercontent.com/underskys/nodemonitor/main/version.py

# Check if the downloaded version.py has the same version as in bot.py
if python -c "import version; from bot import check_new_version; print(check_new_version(version.__version__))" | grep -q "True"; then
    echo "New version is available."
fi

echo "Installing required packages..."
pip install python-telegram-bot==13.7

echo "Starting bot.py with --init..."
nohup python3 bot.py --init &

# Deactivate the virtual environment when done
deactivate