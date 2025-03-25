from pydantic import BaseModel
import pathlib
import sys
from flask import Flask, request

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
DIR = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(DIR))
print("DIR", DIR)   

from pkg.core.func_creator import FunctionCreator 
from pkg.domain.models import Runtime

app = Flask(__name__)
core = FunctionCreator()

class FunctionRequest(BaseModel):
    path: str
    runtime: Runtime


@app.route('/', methods=['POST'])
async def handle_request():
    """Handle both HTTP and CloudEvent requests"""
    try:
        # Determine if this is a CloudEvent
        if "ce-type" in request.headers:
            data = (await request.json())["data"]
        else:
            data = await request.json()
        
        func_request = FunctionRequest(**data)
        response = await core.execute(
            path=func_request.path,
            runtime=func_request.runtime
        )
        
        return response.dict()
    except Exception as e:
        return {"error": str(e)} 
if __name__ == '__main__':
    app.run()
