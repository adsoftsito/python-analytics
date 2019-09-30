# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from flask import Flask
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests

app = Flask(__name__)


@app.route('/calculate')
def calculate():
    return_str = ''
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])
    return_str += 'x dot y : {}'.format(str(np.dot(x, y)))
    return return_str


@app.route('/reglineal')
def reglineal():
    return_str = ''
    data=pd.read_csv("day.csv")
    import statsmodels.formula.api as smf

    lm= smf.ols(formula= "cnt~weathersit", data=data).fit()
    lm.params
    print(lm.summary())
    return_str += str(lm.rsquared) + ' , ' + str(lm.rsquared_adj)
    return return_str

@app.route('/ols')
def ols():
    return_str = 'ok'
    resp = requests.get('https://upheld-castle-251021.appspot.com/censos?entidad=30&municipio=118')
    #resp = requests.get('https://upheld-castle-251021.appspot.com/entidades')
   
    if resp.status_code != 200:
    # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    #for todo_item in resp.json():
    #    print('{} {}'.format(todo_item['actividad_economica'], todo_item['ue']))
        #return_str += '{} {}'.format(todo_item['cve_ent'], todo_item['entidad'])
    #print ( json_normalize(resp.json()) )
    data=json_normalize(resp.json())
    #print (data)

    df = data[['cve_mun', 'a211a']]
    #ue = [item['cve_ent'] for item in data]
    #a211a = [item['entidad'] for item in data]
    #ratings = [item['rating'] for item in data]
    #vendors = [item['vendors'][0]['display'] if len(item['vendors']) != 0 else 'N/A' for item in data]
    #paths = [item['paths'][0]['path_label'] for item in data]
    #skillLevel = [item['difficulty']['display'] for item in data]
    #links = [base + item['seoslug'] for item in data]

    #df=  pd.DataFrame(
    #  {'ue': ue,
    #   'a211a': a211a
    #  })
    #df = data['ue','a211a']
    import statsmodels.formula.api as smf
    #print (df)
    lm= smf.ols(formula= "cve_mun~a211a", data=df).fit()
    #print (lm.params)
    print(lm.summary())
    return_str += str(lm.rsquared) + ' , ' + str(lm.rsquared_adj)

    return return_str

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)
