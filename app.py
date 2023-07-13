from flask import Flask, request, Response
from wrapsql import add_row, show_table, on_complete, on_error, get_id, Post, PostSchema
import json
import threading
import time
from calculation import start_calculation
import datetime
from marshmallow import ValidationError, Schema, fields

app = Flask(__name__)
@app.route("/calculations", methods=["POST", "GET"]) # Go to post route where the only method is a post 
def calculations():
	if request.method == "POST": 
		post_schema = PostSchema()
		data=json.loads(request.data)
		try:
			data=post_schema.load(data)
		except ValidationError as err:
			print(err.messages)
			print(err.valid_data)
			return Response(response=json.dumps(err.messages), status=400)
		id = add_row(data)

		calc=data['calculation_type']
		x=data['x_value']
		y=data['y_translation']
		# Run function in separate thread
		# Added id as an argument to start_calculation
		t = threading.Thread(target=start_calculation, args=(id, calc, x, y, on_complete, on_error)) 
		t.start()
		started={"id": id}
		return Response(response=json.dumps(started), status=201)

	if request.method == "GET":
		since = request.args.get('since')
		#print(f'since is: {since}')
		#if request.method == "GET":
		if since is None:
			return str(show_table())
		else:
			return str(show_table(since=since))


@app.route('/calculations/<id>')
def calculations_id(id=None):
	row = get_id(int(id))[0]
	return row.__json__()

if __name__ == "__main__": app.run(debug=True, port="8080", 
	host="0.0.0.0")



