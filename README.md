# huckberry-clone

FastAPI ecommerce platform inspired by huckberry

## Setup
### Prerequisites
Python3 and pip

### How to run
- Download and extract the project files
- Go to the root directory of the project
- Initialize a virtual environement, download the required packages
```bash
python -m venv .venv
pip install -r requirements.txt
```
- Start the ASGI server
```bash
uvicorn main:app --reload
```
- On your browser open http://localhost:8000 or http://127.0.0.1:8000
- Login with the default admin;
username: admin |
password: admin123
- Or register as a regular user

Access API documentation at: http://127.0.0.1:8000/docs