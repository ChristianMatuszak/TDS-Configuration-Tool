import tkinter as tk
import json


def read_tds():
    file1 = "tds-server.json"

    with open(file1, "r") as f1:
        tds = json.loads(f1.read())

    return tds


def read_schema():
    file1 = "schema.json"

    with open(file1, "r") as f1:
        schema = json.loads(f1.read())

    return schema


def save_tds():
    file1 = "tds-server.json"
