import requests


domen = "http://localhost:5000"
requests.post(domen + "/add_to_es", json={'text': 'sometext'})
