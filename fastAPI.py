# RESTful API is that a Streamlit page is designed for interactive user interfaces, while a RESTful API is designed for machine-to-machine communication
# get and post decorrators are called  HTTP methods
# the string in the parenthesis in front of the HTTP methods is called end point.
# HTTP GET requests are used for retrieving data, while HTTP POST requests are
# used for submitting data to a server for processing or storage
# The endpoint URL serves as the user interface for the client, in that
# it defines the set of operations that the client can perform on the server.
# The client can specify the desired operation by sending a request with the
# appropriate HTTP method to the corresponding endpoint URL.


from fastapi import FastAPI, Response, Request
import uvicorn
import spacy
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pydantic
import pandas as pd
from fastapi.responses import JSONResponse
import requests
templates = Jinja2Templates(directory="templates")
app = FastAPI()
nlp = spacy.load("en_core_web_sm")
user_inputs = []
entities = []
# used to retrieve information from a server
# GET requests are typically used for read-only
# operations, where no modification to the
# server-side resources is required.
@app.get("/api")
def dataInsert():
    if len(user_inputs)==0:
        return "System is ON and you can use it to find NERs"
    else:
        return [x for x in entities]
    # return templates.TemplateResponse("input_form.html", {"request": request})

# When you enter the URL http://127.0.0.1:8000/get in your web browser and hit Enter,
# your browser automatically sends a GET request to the specified URL, and FastAPI's
# app.get() function handles the request and returns the response to your browser.

@app.post("/api")
async def get_ner(request: Request):
    data = await request.json()
    user_inputs.append(data)
    result_NER = nlp(user_inputs[-1])
    for ent in result_NER.ents:
        entities.append({"text": ent.text, "label": ent.label_})
    return {"entities": entities}


# The issue is that POST_request() is being called outside of the if __name__ == "__main__": block.
# When you call uvicorn.run(app, host="127.0.0.1", port=8000), the server is started and running on
# the main thread, and the execution of the program is blocked on this line. So, any code that comes
# after this line will not be executed until the server is stopped.
# To solve this issue, you need to move the call to POST_request() inside the if __name__ == "__main__": block.
# You can do this by adding POST_request() as a startup event for the uvicorn server, like this:
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)#, on_startup =POST_request)




# this will run the api and reload it if any changes happens
#  uvicorn fastAPI:app --reload
# you have to choose between uvicorn.run(app, host="127.0.0.1", port=8000)
# and the code in the previous line. One of them is terminal specific.


# In RESTful API design, each endpoint (or URL) is responsible for performing
# a specific operation. When designing a web service, it's a common practice
# to define a corresponding GET endpoint for each POST endpoint. The GET endpoint
# typically returns the resource that was created or updated by the POST endpoint.
# So, if you want to retrieve information from the server, you should use a GET request.
# If you want to make a change to the server-side resources, you should use a POST request.
# In a RESTful API, user input can be a part of both GET and POST requests.
#
# In a GET request, user input is typically passed as a query parameter in the URL. For example, if you want to
# search for a product with ID 123, you can pass the ID as a query parameter
# like this: http://example.com/products?id=123. In this case, the id=123 part is the user input that is passed
# as a query parameter in the GET request.
# In a POST request, user input is typically passed as the body of the request. For example, if you want to create
# a new user, you can pass the user's details (such as name, email, password) as the body of the POST request.
# So, whether the user input is counted as part of a GET or POST request depends on how it is passed to the API.
# Yes, that's correct. In general, HTTP GET requests are used to retrieve data or content from a server and display
# it on a web page or client. In contrast, HTTP POST requests are used to send data to a server to create or update
# a resource. So, if you want to display something on a web page, it should be retrieved using a GET request.