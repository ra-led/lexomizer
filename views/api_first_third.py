import json
from flask import request
from app import app
from utils import text_staff


@app.route('/api_first_third', methods=['POST'])
def api_first_third():
    params = request.get_json()

    per = text_staff.Person(
        app.config['trf'],
        orig_text=params['orig_text'],
        id_=0,
        gender=params['gender'],
        first_name=params['first_name'],
        last_name=params['last_name'],
        middle_name=params['middle_name']
    )
    per = text_staff.per_1_to_3(per, app.config['trf'])
    per = text_staff.postprocess_alias_1_to_3(per, app.config['trf'])

    return json.dumps({
        'result': per.postprocess(api=True)
    })
