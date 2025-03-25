# JWT Tutorial

## Run Frontend

```
npm install
npm run dev
```

Access frontend at `http://localhost:5173/`

## Run Backend

```
pip install -r requirements.txt
```

For session ID demo run the following backend:

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

For JWT demo run the following backend:

```
uvicorn mainjwt:app --host 0.0.0.0 --port 8000 --reload
```

The backend server will start on port `http://0.0.0.0:8000`
