# activate the environment
source venv/bin/activate

# download necessary packages
pip install -r requirements.txt

# initialize values
python init_db.py

# run the web application
python app.py
