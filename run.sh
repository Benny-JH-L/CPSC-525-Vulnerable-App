py -m venv venv 
source venv/bin/activate
py .\env\Scripts\pip.exe install -r requirements.txt
py init_db.py
py app.py
