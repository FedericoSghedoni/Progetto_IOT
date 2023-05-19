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

@blueprint.route('/pale')
def pale():
    with get_db() as conn:
        arduino_all_data = conn.execute('SELECT * FROM arduino').fetchall()
        
        turbine_data= conn.execute(
                        "SELECT subquery3.zone, subquery3.id, subquery3.date, subquery3.hour, subquery3.speed, subquery3.power, subquery3.current, subquery3.error "
                        "FROM ( "
                        "    SELECT subquery2.*, ROW_NUMBER() OVER (PARTITION BY subquery2.zone, subquery2.id ORDER BY subquery2.date DESC, subquery2.hour DESC) AS rn "
                        "    FROM ( "
                        "        SELECT t.* "
                        "        FROM arduino t "
                        "        ORDER BY t.zone, t.id, t.date DESC, t.hour DESC "
                        "    ) subquery2 "
                        ") subquery3 "
                        "WHERE subquery3.rn <= 3 "
                        "GROUP BY subquery3.zone, subquery3.id, subquery3.date, subquery3.hour, subquery3.speed, subquery3.power, subquery3.current, subquery3.error"
                    ).fetchall()


        arduino_recent_data = conn.execute('SELECT * '
                       'FROM arduino a '
                       'WHERE (zone, id, date, hour) IN ('
                           'SELECT zone, id, MAX(date), MAX(hour) '
                           'FROM arduino '
                           'GROUP BY zone, id)').fetchall()

    return render_template('home/pale.html', arduino_recent_data=arduino_recent_data, arduino_all_data=arduino_all_data, turbine_data=turbine_data)

@blueprint.route('/tables') 
def tables():
    with get_db() as conn:
        arduino = conn.execute('SELECT * FROM arduino').fetchall()
        turbine_data= conn.execute(
                        "SELECT subquery3.zone, subquery3.id, subquery3.date, subquery3.hour, subquery3.speed, subquery3.power, subquery3.current, subquery3.error "
                        "FROM ( "
                        "    SELECT subquery2.*, ROW_NUMBER() OVER (PARTITION BY subquery2.zone, subquery2.id ORDER BY subquery2.date DESC, subquery2.hour DESC) AS rn "
                        "    FROM ( "
                        "        SELECT t.* "
                        "        FROM arduino t "
                        "        ORDER BY t.zone, t.id, t.date DESC, t.hour DESC "
                        "    ) subquery2 "
                        ") subquery3 "
                        "WHERE subquery3.rn <= 3 "
                        "GROUP BY subquery3.zone, subquery3.id, subquery3.date, subquery3.hour, subquery3.speed, subquery3.power, subquery3.current, subquery3.error"
                    ).fetchall()
        #power = conn.execute('SELECT * FROM TurbineDataset').fetchall() 
        meteo=conn.execute('SELECT * FROM meteo').fetchall()

    return render_template('home/tables.html', pale=pale, arduino=arduino,meteo=meteo, turbine_data=turbine_data)

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

        arduino_recent_data = conn.execute("SELECT a.* "
                       "FROM arduino a "
                       "JOIN (SELECT zone, id, MAX(date || ' ' || hour) AS max_datetime "
                       "FROM arduino "
                       "GROUP BY zone, id) a2 ON a.zone = a2.zone AND a.id = a2.id AND (a.date || ' ' || a.hour) = a2.max_datetime").fetchall()

        #power = conn.execute('SELECT * FROM TurbineDataset').fetchall() #togli
        meteo=conn.execute('SELECT * FROM meteo').fetchall()

    return render_template('home/index.html', segment='index', arduino=arduino, hours=hours, speeds=speeds, 
                           arduino_recent_data=arduino_recent_data, meteo=meteo)
    

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
