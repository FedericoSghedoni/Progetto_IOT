from flask import render_template, request, Blueprint, g, current_app
from jinja2 import TemplateNotFound
import sqlite3

blueprint = Blueprint('home', __name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@blueprint.route('/forecast') #ho tolto la pagina
def forecast():
    with get_db() as conn:
        power = conn.execute('SELECT * FROM TurbineDataset').fetchall()

    return render_template('home/forecast.html', power=power)

@blueprint.route('/pale')
def pale():
    with get_db() as conn:
        arduino_all_data = conn.execute('SELECT * FROM arduino').fetchall()

        arduino_recent_data = conn.execute('SELECT * '
                       'FROM arduino a '
                       'WHERE (zone, id, date, hour) IN ('
                           'SELECT zone, id, MAX(date), MAX(hour) '
                           'FROM arduino '
                           'GROUP BY zone, id)').fetchall()

    return render_template('home/pale.html', arduino_recent_data=arduino_recent_data, arduino_all_data=arduino_all_data)

@blueprint.route('/tables') 
def tables():
    with get_db() as conn:
        arduino = conn.execute('SELECT * FROM arduino').fetchall()
        power = conn.execute('SELECT * FROM TurbineDataset').fetchall()
        meteo=conn.execute('SELECT * FROM meteo').fetchall()

    return render_template('home/tables.html', pale=pale, arduino=arduino, power=power,meteo=meteo)

@blueprint.route('/index')
def index():
    with get_db() as conn:
        data = conn.execute("SELECT hour, speed FROM arduino ORDER BY hour").fetchall()

        hours = []
        speeds = []

        for row in data:
            hours.append(row['hour'])
            speeds.append(row['speed'])

        arduino = conn.execute('SELECT * FROM arduino').fetchall()

        arduino_recent_data = conn.execute('SELECT * '
                       'FROM arduino a '
                       'WHERE (zone, id, date, hour) IN ('
                           'SELECT zone, id, MAX(date), MAX(hour) '
                           'FROM arduino '
                           'GROUP BY zone, id)').fetchall()

        power = conn.execute('SELECT * FROM TurbineDataset').fetchall()
        meteo=conn.execute('SELECT * FROM meteo').fetchall()

    return render_template('home/index.html', segment='index', arduino=arduino, hours=hours, speeds=speeds, 
                           arduino_recent_data=arduino_recent_data, power=power, meteo=meteo)
    

@blueprint.route('/<template>')
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
