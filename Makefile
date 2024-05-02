VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
STREAMLIT = $(VENV)/bin/streamlit

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

app: $(VENV)/bin/activate
	$(STREAMLIT) run app.py --server.port 7004

vote: $(VENV)/bin/activate
	$(PYTHON) vote.py

clean:
	rm -rf __pycache__
	rm -rf $(VENV)