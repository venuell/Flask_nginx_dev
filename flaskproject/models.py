import subprocess
from flask import flash,send_file
import time

tomcatShutdownPeriod = 10

def isProcessRunning(server_name):
    pStatus = True
    tProcess = subprocess.Popen(["ssh",server_name,"ps -ef | grep -v grep | grep 'jmxremote.port=' | wc -l"], stdout=subprocess.PIPE)
    out, err = tProcess.communicate()
    if out=='':
        flash("could not connect/execute on server" +server_name ,"error")
        return
    elif int(out) <1:
        pStatus = False
    return pStatus

def status(server_name):
    if isProcessRunning(server_name):
        tPid = subprocess.Popen(["ssh",server_name,"ps -ef | grep -v grep | grep 'jmxremote.port=' | awk \'{print $2}\'"], stdout=subprocess.PIPE)
        out, err = tPid.communicate()
        flash ("Tomcat process on " +server_name +" is running with PID " + str(out),"success")
    else:
        flash ("Tomcat process on " +server_name +" is not running", "error")



def start(server_name):
    if isProcessRunning(server_name):
        flash ("Tomcat process on " +server_name +"  is already running", "success")
    else:
        flash ("Starting the tomcat on " +server_name, "success")
        subprocess.call(["ssh",server_name,"service tomcat_xe_DPD8_8100 start"])
        status(server_name)

def stop(server_name):
    if isProcessRunning(server_name):
        flash ("Stopping the tomcat on " +server_name,"success" )
        subprocess.call(["ssh",server_name,"service tomcat_xe_DPD8_8100 stop"])
        #time.sleep(tomcatShutdownPeriod)
        status(server_name)
        if isProcessRunning(server_name):
            tPid = subprocess.Popen(["ssh",server_name,"ps -ef | grep -v grep | grep 'jmxremote.port=///' | awk \'{print $2}\'"], stdout=subprocess.PIPE)
            out, err = tPid.communicate()
            subprocess.Popen(["kill -9 " + out])
            flash ("Tomcat on " +server_name +" failed to shutdown, so killed with PID " + out,"success")
    else:
        flash("Tomcat process on " +server_name +" is not running","success")

def restart(server_name):
    stop(server_name)
    start(server_name)
    
def snap_id():
    tSid = subprocess.Popen(["ssh","svc_oracle@perfpbnrduva01","/home/svc_oracle/awr_report/snap.sh"], stdout=subprocess.PIPE)
    out, err = tSid.communicate()
    flash ("snap id is " + str(out).strip())


def awr_report(snap_ids):
    tAid = subprocess.Popen(["ssh", "svc_oracle@perfpbnrduva01","/home/svc_oracle/awr_report/gen_awr.sh",snap_ids[0],snap_ids[1]], stdout=subprocess.PIPE)
    out, err = tAid.communicate()
    #flash(out)
    if str(out).find("Report written to"):
        flash("AWR report created "+ "DPD8_"+snap_ids[0]+"_"+snap_ids[1]+".html" )
        tScid = subprocess.Popen(["scp","svc_oracle@perfpbnrduva01:/home/svc_oracle/awr_report/reports/$(ls -t /home/svc_oracle/awr_report/reports/ |head -n 1)","/root/FlaskProject/flaskproject/awrreports"], stdout=subprocess.PIPE)
        out, err = tScid.communicate()

   
