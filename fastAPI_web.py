from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import spacy

app = FastAPI()
templates = Jinja2Templates(directory="templates")
save_data = []

def NER(input_data):
    nlp = spacy.load("en_core_web_sm")
    data= []
    result = nlp(input_data)
    for ent in result.ents:
        data.append(ent.text, ent.label_)
    save_data.append(data)

@app.get("/")
def form_post(request: Request):
    result = templates.TemplateResponse('home.html', context={'request': request})
    return result

@app.post("/")
def get_ner(inputs: str = Form(None)):
    if inputs is None:
        return {"result": "Please enter some text in the form above."}
    else:
        NER(inputs)
        return {"result": save_data[-1]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastAPI_web:app", host="127.0.0.1", port=8000, reload=True)