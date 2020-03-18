###
import argparse
import copy
import json
import random
from string import Template
from typing import List

import torch
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from _html import _html

from run_multiple_choice import load_model, predict_example, input_ablation
from my_arguments import get_argparse

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")

load_model_args = get_argparse()
model, ref_dataset, processor, tokenizer = load_model(load_model_args)
ref_idx_to_example_id = {i: example.example_id for i, example in enumerate(ref_dataset)}

option_num = len(processor.get_labels())

field_names = ["document", "question", "option_header"]
for i in range(option_num):
    field_names.append(f'option{i+1}')

original_example = None


class RequestBody(BaseModel):
    document: str = None
    question: str = None
    for i in range(option_num):
        locals()["__annotations__"][f"option{i+1}"] = str
    example_id: str = None
    specification: str = None
    label: str = None


def convert_input_body_to_example(input_body):
    options = [getattr(input_body, f'option{i+1}') for i in range(option_num)]
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


def ablate_example(input_body):
    example = convert_input_body_to_example(input_body)
    modified_example = input_ablation(input_body.specification, example, tokenizer)
    for i, option in enumerate(modified_example["options"]):
        modified_example[f"option{i+1}"] = option
    return modified_example


@app.get("/", response_class=HTMLResponse)
def read_root():
    html = _html(title="mrc demo", field_names=field_names)
    return html


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
    global original_example
    original_example = copy.deepcopy(return_example)
    return return_example


@app.get("/revert")
def get_original():
    if original_example:
        return original_example


@app.post("/predict")
def predict(body: RequestBody):
    return make_prediction(body)


@app.post("/ablate")
def ablate(body: RequestBody):
    return ablate_example(body)


if __name__ == "__main__":
    # uvicorn.run('demo:app', reload=True)
    uvicorn.run(app)

