
import os
import glob

from flask import flash,request,redirect,url_for,send_file
from flask.templating import render_template
from  flaskproject import app
from flaskproject.models import start,status,stop,restart,snap_id,awr_report



@app.route('/tom_server', methods=('GET','POST'))
def tom_server():
    if request.method == 'POST':
        servers_name = request.form['servers'].split(",")
        snap_ids = request.form['snap_ids'].split(",")
        action_name= request.form['status']

        error = None
        if error is None:
            if action_name == 'status':
                for server_name in servers_name:
                    status(server_name)
                        #server_name = threading.Thread(target=models.status, args=(server_name,))
                        #server_name.start()
            elif action_name == 'start':
                for server_name in servers_name:
                    start(server_name)

            elif action_name =='stop':
                for server_name in servers_name:
                    stop(server_name)

            elif action_name == 'restart':
                for server_name in servers_name:
                    restart(server_name)
            elif action_name == 'snap_id':
                snap_id()
            elif action_name == 'awr_report':
                awr_report(snap_ids)
                #return send_file('/root/FlaskProject/flaskproject/awrreports/DPD8_30012020.html', attachment_filename='DPD8_30012020.html')
     

                #flash(error, 'error')

    return render_template('tom_server.html')


@app.route('/download', methods=('GET','POST'))
def download():
    list_of_files = glob.glob('/root/FlaskProject/flaskproject/awrreports/*.html')
    latest_file = max(list_of_files, key=os.path.getctime)
    #flash(latest_file)
    return send_file(latest_file, attachment_filename=latest_file)
