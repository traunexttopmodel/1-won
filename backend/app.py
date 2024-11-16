import flask
from flask_restful import Resource, Api
from main import main  # Import function

app = flask.Flask(__name__)
api = Api(app)

# Create a Resource that calls your function and returns the output
class CallFunction(Resource):
    def get(self):
        # Call the function from your other Python file
        result = main()
        return {'result': result}  # Return the result as JSON

# Add the resource to the API
api.add_resource(CallFunction, '/main')  # Accessible at /call-function

if __name__ == '__main__':
    app.run(debug=True)