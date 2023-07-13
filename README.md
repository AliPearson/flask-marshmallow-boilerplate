### Docker:
- To build locally
sudo docker build -t alice-flask .

- Get the image id from this
sudo docker image ls

- To run on port 8080
sudo docker run -d -p 8080:8080 <IMAGE_ID>

### To test (also in pytests in Docker)
- Open a python console with poetry in a new terminal: `poetry run python`
	In the console:
	- Post request
	requests.post('http://10.0.0.78:8080/post', '{"x_value": 1.88, "calculation_type": "red", "y_translation": 7}').text

	- Get request to show all table
	requests.get('http://10.0.0.78:8080/calculations').text

	- Get request with id
	requests.get('http://10.0.0.78:8080/calculations/1').text

	- Get request with since query
	requests.get('http://10.0.0.78:8080/calculations?since=100').text


### Notes
- The poetry link in the test is deprecated. The poetry
   documentation even says do not install poetry this way
   https://python-poetry.org/docs/.
- poetry init, go through options. Creates pyproject.toml poetry is
   basically like conda. A virtual environment to manage packages.
- 'poetry shell' opens the environment (like conda activate my_env)
- poetry add <package name> --> Add package to environment, then can do
   poetry run python app.py and it will work.
- Container is a running image, e.g alice-app.
- Image is created that gets everything ready to go. When we do docker
   run .. it becomes a container and the app is live.
- Making a SQL table in memory in one script means it could not be
   accessed by app.py script.
- Flask accesses the requests to the database using threads.
- We need to put the db on the disc so that is can be accessed by
   multiple threads.
- Had to add id argument to start_calculation so I can update the table.
- json was fiddly, going between strings and dictionaries and json
- Choice between datetime.time() and time.time() for on_complete and
   on_error was tricky. datetime is pretty but need time in second for
   since query.
- In dockerfile, could remake poetry and add everything again or I have
   just copied my existing .toml file.
