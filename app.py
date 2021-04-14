
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, render_template, request
from psycopg2 import connect
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

app.config['dbconfig'] = dict(
                            host='videos.mysql.pythonanywhere-services.com',
                            user='videos',
                            database='videos$default',
                            password='Manofaction.1',
                            )

@app.route('/')
def hello_world():
    conn = connect(**app.config['dbconfig'])
    cursor = conn.cursor()

    cursor.execute('select links from videos')
    links = cursor.fetchall()[0]

    return render_template('index.html',links=links)



@app.route('/add', methods=['POST'])
def add_video():
    try:
        conn = connect(**app.config['dbconfig'])
        cursor = conn.cursor()

        _SQL = '''insert into videos
                  (links)
                  values
                  (%s)'''

        cursor.execute(_SQL, (request.form['links'], ))
        conn.commit()
        cursor.close()
        conn.close()

        return 'Added'
    except Exception as err:
        return str(err)



@app.route('/videos', methods=['POST'])
@cors
def video():
    '''Returns a JSON list of video links uploaded'''
    conn = connect(**app.config['dbconfig'])
    cursor = conn.cursor()

    cursor.execute('select links from videos')
    links = cursor.fetchall()[0]
    return jsonify(links)

if __name__=='__main__': app.run(port=9999)
