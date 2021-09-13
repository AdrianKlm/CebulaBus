# CebulaBus
Termux:

    pkg install git
    pkg install python
    git clone https://github.com/AdrianKlm/CebulaBus.git
    cd cebulabus
    python -m venv cebulabus-env
    source cebulabus-env/bin/activate
    pip install -r requirements.txt
    chmod +x cebulabus.py
    nohup python -u cebulabus.py > cebulabus.log &
    tail -f cebulabus.log
