'''Initializes the FastAPI Application.'''


from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def read_root():
    return {'hello': 'world'}
