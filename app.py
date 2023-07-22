from flask import Flask, request, jsonify
import dao
import services


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/identify",methods=['POST'])
def identify():
    try:
        data = request.json
        if 'email' in data and 'phoneNumber' in data :
            email = data['email']
            phoneNumber = data['phoneNumber']
            componentId=services.identify_operations(email,phoneNumber)
            output = services.generate_output_from_DB(componentId)
            return output,200
        else :
            return jsonify({'error':'Invalid JSON data. Missing Parameters'}),400
    
    except Exception as e:
         return jsonify({'error':str(e)}),500


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5432)