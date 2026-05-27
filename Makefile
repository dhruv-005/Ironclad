# 🛡️ Ironclad Makefile

.PHONY: install run test clean db

install:
	pip install -r requirements.txt

run:
	streamlit run app.py

db:
	python init_db.py

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f temp/*.jpg

check:
	python -c "import faiss, cv2, insightface, streamlit; print('All OK')"
