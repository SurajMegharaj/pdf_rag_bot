from fastapi import FastAPI
from api import uploadapi, queryapi


app = FastAPI()

app.include_router(uploadapi.router,prefix='/api')
app.include_router(queryapi.router,prefix = '/api')

@app.get('/')
def read_root():
    return{'message' : 'Welcome to the pdf chatbot'}
