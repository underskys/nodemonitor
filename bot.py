__version__ = "0.1.0"
__name__ = "nodemonitor"
__author__ = "Dmitry Shtro (underskys)"

import os
import sys
import socket
import subprocess
import logging
import version
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN_FILE = "telegram_bot_token.txt"
OWNER_ID = None

def check_new_version(local_version):
    try:
        remote_version = subprocess.check_output(["git", "ls-remote", "--tags", "https://gitlab.com/your-repository.git"]).decode("utf-8").strip().split("\n")[-1].split("/")[-1]
        return remote_version.strip("v") != local_version
    except Exception as e:
        print(f"Error checking for new version: {e}")
        return False

logging.basicConfig(level=logging.INFO)

def read_token():
    if os.path.exists(TOKEN_FILE) and os.path.getsize(TOKEN_FILE) > 0:
        with open(TOKEN_FILE, "r") as token_file:
            return token_file.read().strip()
    return None

def write_token(token):
    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(token)

def init_token():
    token = input("Type your TOKENID: ").strip()
    write_token(token)
    return token

def get_top_process():
    result = subprocess.run(["ps", "-eo", "pid,pcpu,pmem,command", "--sort=-pcpu"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    header, *processes = lines

    pid, cpu, mem, command = processes[0].split(None, 3)
    return int(pid), command

def get_host_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

def start(update: Update, context: CallbackContext):
    global OWNER_ID

    if OWNER_ID is None:
        OWNER_ID = str(update.effective_user.id)
    elif str(update.effective_user.id) != OWNER_ID:
        update.message.reply_text("Доступ запрещен.")
        return

    hostname, ip_address = get_host_info()
    pid, command = get_top_process()
    update.message.reply_text(f"Monitoring started.\nHost: {hostname}\nIP: {ip_address}\nProcess: {pid} ({command})")

    context.job_queue.run_repeating(monitor_process, interval=60, first=0, context=update.effective_chat.id)

def monitor_process(context: CallbackContext):
    chat_id = context.job.context
    pid, command = get_top_process()
    
    try:
        os.kill(pid, 0)
    except OSError:
        hostname, ip_address = get_host_info()
        context.bot.send_message(chat_id, f"Process {pid} ({command}) has terminated.\nHost: {hostname}\nIP: {ip_address}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        token = init_token()
    else:
        token = read_token()
        if token is None:
            token = init_token()

    updater = Updater(token)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if check_new_version(version.__version__):
        print("New version is available.")
    main()