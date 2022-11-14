#GADS Climate CHange Individual Project by Damilola Olaide Banjoko

#Climate Change Monitor to measure air pollution by location 

from flask import Flask, jsonify, request

app = Flask(__name__) 

@app.route('/', methods =['GET', 'POST'])
def main():
    if request.method == 'POST' and 'username' in request.form and 'city' in request.form and 'country' in request.form:
        username = request.form['username']
        city = request.form['city']
        country = request.form['country']

if __name__ == "__main__":
    app.run(debug=True)
