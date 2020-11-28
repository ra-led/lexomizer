#!/usr/bin/env python3
from flask import Flask, render_template
import pymorphy2
from utils.text_staff import Transformer
from pytrovich.maker import PetrovichDeclinationMaker

app = Flask(__name__)
app.config['trf'] = Transformer(
    morph=pymorphy2.MorphAnalyzer(),
    alias_maker=PetrovichDeclinationMaker()
)

from views import first_third

@app.route('/')
def index():
    return render_template('index.html')
