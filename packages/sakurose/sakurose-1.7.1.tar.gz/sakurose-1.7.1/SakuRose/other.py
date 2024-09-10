import json
import math
import operator
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import pytz
import time
import requests
import threading
import re
import subprocess

active_apis = {}
paused_apis = {}

def shell(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def test():
    return "SakuRose working correctly."

def parse_time(time_str):
    time_units = {
        's': 1,              # segundos
        'm': 60,             # minutos
        'h': 3600,           # horas
        'd': 86400,          # días
        'w': 604800,         # semanas
        'mo': 2592000,       # meses (30 días)
        'y': 31536000        # años (365 días)
    }
    
    pattern = r"(\d+)([smhdwmo]+)"
    matches = re.findall(pattern, time_str)
    total_seconds = 0
    
    for value, unit in matches:
        total_seconds += int(value) * time_units[unit]
    
    return total_seconds

def uptime(api_link, cooldown="5m"):
    if api_link in active_apis:
        print(f"Ya hay un uptime activo para la API: {api_link}")
        return
    
    cooldown_seconds = parse_time(cooldown)
    
    def run_uptime():
        while api_link in active_apis:
            if api_link in paused_apis:
                time.sleep(1)
                continue
            try:
                response = requests.get(api_link)
                if response.status_code == 200:
                    print(f"Solicitud exitosa: {response.status_code}")
                else:
                    print(f"Error en la solicitud: {response.status_code}")
            except Exception as e:
                print(f"Error al hacer la solicitud: {e}")
            time.sleep(cooldown_seconds)
    
    active_apis[api_link] = threading.Thread(target=run_uptime)
    active_apis[api_link].start()

def stop_uptime(api_link):
    if api_link not in active_apis:
        print(f"No hay uptime activo para la API: {api_link}")
        return
    del active_apis[api_link]
    if api_link in paused_apis:
        del paused_apis[api_link]
    print(f"Uptime detenido para la API: {api_link}")

def pause_uptime(api_link, pause_time=None):
    if api_link not in active_apis:
        print(f"No hay uptime activo para la API: {api_link}")
        return
    
    paused_apis[api_link] = True
    print(f"Uptime pausado para la API: {api_link}")
    
    if pause_time:
        pause_seconds = parse_time(pause_time)
        def resume_after_pause():
            time.sleep(pause_seconds)
            if api_link in paused_apis:
                resume_uptime(api_link)
        threading.Thread(target=resume_after_pause).start()

def resume_uptime(api_link):
    if api_link not in active_apis or api_link not in paused_apis:
        print(f"No hay uptime pausado para la API: {api_link}")
        return
    del paused_apis[api_link]
    print(f"Uptime reanudado para la API: {api_link}")

us_timezones = [
    'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
    'America/Phoenix', 'America/Anchorage', 'America/Indiana/Indianapolis', 'Pacific/Honolulu'
]

def time_converter(tiempo, tz_database="America/Mexico_City"):
    try:
        tz = pytz.timezone(tz_database)
    except pytz.UnknownTimeZoneError:
        tz = pytz.timezone("America/Mexico_City")
    
    es_eeuu = tz_database in us_timezones
    
    try:
        if tiempo.isdigit():
            unix_time = int(tiempo)
            dt = datetime.fromtimestamp(unix_time, tz)
            if es_eeuu:
                return dt.strftime('%m/%d/%Y-%H:%M')
            else:
                return dt.strftime('%d/%m/%Y-%H:%M')
        else:
            if '-' not in tiempo:
                tiempo += '-12:00'
            dt = datetime.strptime(tiempo, '%d/%m/%Y-%H:%M')
            dt_tz = tz.localize(dt)
            unix_time = int(dt_tz.timestamp())
            return unix_time
    except ValueError:
        return "Formato de tiempo inválido. Asegúrate de usar el formato dd/mm/yyyy o dd/mm/yyyy-HH:MM."

passdef = os.environ['passwordefault']
gmaildef = os.environ['gmaildefault']

def gmail_send(destinatario, asunto, contenido, remitente=None, contraseña=None):
    remitente_default = gmaildef
    contraseña_default = passdef
    
    remitente = remitente if remitente else remitente_default
    contraseña = contraseña if contraseña else contraseña_default

    try:
        msg = EmailMessage()
        msg.set_content(contenido)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contraseña)
            smtp.send_message(msg)

        print(f'Correo enviado a {destinatario} exitosamente.')

    except Exception as e:
        print(f'Error al enviar correo: {e}')

def caption(text: str, image_url: str) -> str:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(BytesIO(response.content))
    
    font_size = int(image.size[1] * 0.1)
    font = ImageFont.truetype("arial.ttf", font_size)

    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    new_height = image.size[1] + int(image.size[1] * 0.2)
    new_image = Image.new('RGB', (image.size[0], new_height), (255, 255, 255))

    draw = ImageDraw.Draw(new_image)
    
    text_x = (new_image.size[0] - text_width) / 2
    text_y = 0
    draw.rectangle([(0, text_y), (new_image.size[0], text_height)], fill="white")
    draw.text((text_x, text_y), text, font=font, fill="black")

    new_image.paste(image, (0, text_height))

    temp_path = "temp_image.png"
    new_image.save(temp_path)
    
    time.sleep(60)
    
    os.remove(temp_path)
    
    return temp_path

def calculate(operation: str) -> float:
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '×': operator.mul,
        '/': operator.truediv,
        '÷': operator.truediv,
        '**': operator.pow,
        '//': operator.floordiv,
        '%': operator.mod,
        '^': operator.pow,
    }
    
    funcs = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log,
        'log10': math.log10,
        'factorial': math.factorial,
        'pow': math.pow,
        'exp': math.exp,
        'ceil': math.ceil,
        'floor': math.floor,
    }

    small_numbers = {
        '⁰': 0,
        '¹': 1,
        '²': 2,
        '³': 3,
        '⁴': 4,
        '⁵': 5,
        '⁶': 6,
        '⁷': 7,
        '⁸': 8,
        '⁹': 9,
        '⁻': -1,
        '⁽': '(', 
        '⁾': ')'
    }

    small_fractions = {
        '½': 0.5,
        '⅓': 1/3,
        '⅔': 2/3,
        '¼': 0.25,
        '¾': 0.75,
        '⅕': 0.2,
        '⅖': 0.4,
        '⅗': 0.6,
        '⅘': 0.8,
        '⅙': 1/6,
        '⅚': 5/6,
        '⅐': 1/7,
        '⅛': 0.125,
        '⅜': 0.375,
        '⅝': 0.625,
        '⅞': 0.875,
    }

    def convert_small_numbers(text: str) -> str:
        for uni, num in small_numbers.items():
            text = text.replace(uni, str(num))
        return text

    def convert_small_fractions(text: str) -> str:
        for frac, value in small_fractions.items():
            text = text.replace(frac, f'**{value}')
        return text

    try:
        operation = convert_small_numbers(operation)
        operation = convert_small_fractions(operation)

        for func in funcs:
            if operation.startswith(func):
                arg_str = operation[len(func):].strip("()")
                arg = float(arg_str)
                return funcs[func](arg)
        
        for op in ops:
            if op in operation:
                if op == '^':
                    left, right = map(str.strip, operation.split(op))
                    right = float(right)
                    return ops[op](float(left), right)
                else:
                    left, right = map(str.strip, operation.split(op))
                    left, right = float(left), float(right)
                    return ops[op](left, right)

        raise ValueError("Operación no reconocida o mal formada")
    
    except (ValueError, TypeError) as e:
        raise ValueError(f"Error al calcular la operación: {e}")