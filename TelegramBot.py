import telepot
import time,os
import json
from rich.panel import Panel as nel
from rich.console import Console
from rich.tree import Tree
import threading
import requests
import random

console = Console()
root_tree = Tree("Pesan baru!")
i = 0

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.80",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]
user_agentss = random.choice(user_agents)

def init():
    # Inisialisasi bot
    bot = telepot.Bot(check_token(token))
    bot.message_loop(handle_message)

    print('Bot berhasil dijalankan!')

# Memulai thread untuk input pengguna
    input_thread = threading.Thread(target=user_input)
    input_thread.daemon = True
    input_thread.start()

def start():
  try:
    i = 0
    while True:
        print("Runtime:", i, "Detik", end="\r")
        i = i + 1
        time.sleep(1)
  except KeyboardInterrupt:
        print("Bot dimatikan.")

def check_token(token):
    if os.path.exists('token.txt'):
        print("File token.txt ditemukan.")
        print("Sedang mengecek token...")
        token = read_token()
        return token
        init()
        start()
    else:
        print("File token.txt tidak ditemukan.")
        get_token()

def get_token():
    console.print(nel('[bold cyan]Silahkan masukkan token bot telegram'))
    token1 = input(">>>")
    if token1 == "":
        console.print(nel("Tidak boleh kosong!"))
        get_token()
    else:
        with open('token.txt', 'w') as f:
            f.write(token1 + '\n')
        print("Sukses menyimpan token!")

def read_token():
    with open('token.txt', 'r') as w:
        poken = w.read()
        return poken

def display_bot_response(response):
    console.print(nel(f'[bold green]Ada pesan nih!'))

def send1():
    console.print(nel(root_tree))

def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        command = msg['text']
        sender_name = msg['from']['first_name']
        sender_username = msg['from']['username']
        sender_chat_id = msg['from']['id']

        user_message = f'Pesan dari {sender_name} (@{sender_username}) dengan Chat ID {sender_chat_id} Pesan: {command}'
        user_branch = root_tree.add(user_message)

        if command == '/start':
            response = 'HALLO!\nSelamat datang di Bimz Bot Beta V0.1\nKirim /menu untuk melihat fitur lainnya.'
            bot.sendMessage(chat_id, response)
            display_bot_response(response)
            bot_message = f'[bold green]Bot membalas: {response}'
            user_branch.add(bot_message)

        console.print(nel(root_tree))
        
        if command.startswith('/spam'):
            spam_text = command[7:]
            nomor = spam_text
            if spam_text:
                headers = {
                    "Host": "m.misteraladin.com",
                    "accept-language": "id",
                    "sec-ch-ua-mobile": "?1",
                    "content-type": "application/json",
                    "accept": "application.json, text/plain, */*",
                    "user-agent": user_agentss,
                    "x-platform": "mobile-web",
                    "sec-ch-ua-platform": "Android",
                    "origin": "https://m.misteraladin.com",
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": "https://m.misteraladin.com/account",
                    "accept-encoding": "gzip, deflate, br",
                }
        
                data = {
                    "phone_number_country_code": "62",
                    "phone_number": nomor,
                    "type": "register",
                }
        
                try:
                    # Kirim permintaan HTTP ke URL
                    response = requests.post("https://m.misteraladin.com/api/members/v2/otp/request", headers=headers, data=json.dumps(data))
                    
                    if response.status_code == 200:
                        response ='Pesan spam berhasil dikirim.'
                        bot.sendMessage(chat_id, response)
                        display_bot_response(response)
                        bot_message = f'[bold green]Bot membalas: {response}'
                        user_branch.add(bot_message)
                        send1()
                    else:
                        response = 'Terjadi kesalahan saat mengirim pesan spam.'
                        bot.sendMessage(chat_id, response)
                        display_bot_response(response)
                        bot_message = f'[bold green]Bot membalas: {response}'
                        user_branch.add(bot_message)
                        send1()
                except Exception as e:
                    response = f'Gagal mengirim pesan spam: {str(e)}'
                    bot.sendMessage(chat_id, response)
                    display_bot_response(response)
                    bot_message = f'[bold green]Bot membalas: {response}'
                    user_branch.add(bot_message)
                    send1()
            else:
                response ='Anda harus menyertakan teks setelah /spam  ex:/spam 812xxxxxxx'
                bot.sendMessage(chat_id, response)
                display_bot_response(response)
                bot_message = f'[bold green]Bot membalas: {response}'
                user_branch.add(bot_message)
                send1()

def user_input():
    while True:
        user_input = input()
        if user_input == 'clear':
            os.system("clear")


check_token()
