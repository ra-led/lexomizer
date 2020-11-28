import json
from flask import request, render_template
from app import app
from utils import text_staff


@app.route('/first_third', methods=['POST'])
def first_third():
    params = request.form.to_dict()
    
    per = text_staff.Person(
        app.config['trf'],
        orig_text=params['text'],
        id_=params['person_id'],
        gender=params['gender'],
        first_name=params['first_name'],
        last_name=params['last_name'],
        middle_name=params['middle_name']
    )
    per = text_staff.per_1_to_3(per, app.config['trf'])
    per = text_staff.postprocess_alias_1_to_3(per, app.config['trf'])
    
    return json.dumps({'y': per.postprocess()})
