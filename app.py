
from flask import Flask,request,jsonify, send_file, render_template
from flask_cors import CORS, cross_origin
from darf import darf

app = Flask(__name__) 
cors = CORS(app, resources={r"/": {"origins": "*.*"}})

# ROTAS

@app.route("/",  methods=['POST', 'GET']) 
@cross_origin()
def home():
    return jsonify({
        "api": "API FLASK",
        "version": "1.0.0"
    })

@app.route("/upload", methods=['POST', 'GET']) 
@cross_origin()
def upload(): 
    req = request.get_json()
    isert = darf.insertdata(req)
    print(isert)

    return send_file(isert, mimetype='application/zip')
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)