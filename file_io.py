import tkinter as tk
import json


def read_tds():
    file = "tds-server.json"

    with open(file, "r") as f:
        tds = json.loads(f.read())

    return tds


def read_schema():
    file = "schema.json"

    with open(file, "r") as f:
        schema = json.loads(f.read())

    return schema


"""def save_tds():
    file1 = "tds-server.json"
"""
