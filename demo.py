### 
import argparse
import json
import random
from string import Template
from typing import List

import torch
import uvicorn
from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from _html import _html

from run_multiple_choice import load_model, predict_example, input_ablation
from my_arguments import get_argparse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# parser = argparse.ArgumentParser()
# parser.add_argument("--args_config", default=None, type=str, required=True)
# args = parser.parse_args()
# load_model_args = json.load(open(args.args_config, "r"))
# load_model_args = torch.load('/home/saku/ws/transformers/models_roberta/roberta-large-race/training_args.bin')

load_model_args = get_argparse()
# model, ref_dataset, processor, tokenizer = None, None, None, None
model, ref_dataset, processor, tokenizer = load_model(load_model_args)
ref_idx_to_example_id = {i: example.example_id for i, example in enumerate(ref_dataset)}


class RequestBody(BaseModel):
    document: str = None
    question: str = None
    # options: List[str] = None
    option1: str = None
    option2: str = None
    option3: str = None
    option4: str = None
    example_id: str = None
    specification: str = None
    label: str = None

field_names = ["document", "question", "option1", "option2", "option3", "option4"]
# field_names = ["document", "question", "options_4"]


def convert_input_body_to_example(input_body):
    options = [
        input_body.option1,
        input_body.option2,
        input_body.option3,
        input_body.option4
    ]  # bad idea
    example = {'example_id': input_body.example_id,
               'question': input_body.question,
               'document': input_body.document,
               'options': options,
               'label': input_body.label or None,
               'specification': input_body.specification or None,
    }
    return example

def make_prediction(input_body):
    example = convert_input_body_to_example(input_body)
    label_result, prob_result = predict_example(load_model_args, model, example, processor, tokenizer)
    label_result = label_result.tolist()
    prob_result = prob_result.tolist()
    print(label_result, prob_result)
    return {"result": prob_result[0], "prediction": label_result[0]}
    # return model.predict(input_body)


def ablate_example(input_body):
    example = convert_input_body_to_example(input_body)    
    modified_example = input_ablation(input_body.specification, example)
    # return_example = {
    #     "example_id": modified_example.example_id,
    #     "document": modified_example.contexts[0],
    #     "question": modified_example.question,
    #     "label": modified_example.label or None,
    #     "specification": input_body.specification,
    # }
    for i, option in enumerate(modified_example["options"]):
        modified_example[f"option{i+1}"] = option
    return modified_example


@app.get("/", response_class=HTMLResponse)
def read_root():
    html = _html(title="mrc demo", field_names=field_names)
    return html

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None, r: str=None):
#     return {"item_id": item_id, "qqq": q, "r": r}

@app.get("/get-example")
def get_example():
    example = random.choice(ref_dataset)
    return_example = {
        "example_id": example.example_id,
        "document": example.contexts[0],
        "question": example.question,
        "label": example.label,
    }
    for i, option in enumerate(example.endings):
        return_example[f"option{i+1}"] = option
    return return_example

@app.post("/predict")
def predict(body: RequestBody):
    return make_prediction(body)

@app.post("/ablate")
def ablate(body: RequestBody):
    return ablate_example(body)

if __name__ == "__main__":
    # uvicorn.run('demo:app', reload=True)
    uvicorn.run(app)
    
