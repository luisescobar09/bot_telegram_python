import sys, os, datetime, requests, json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from os import remove
from os import path

token = "1719347357:AAHNHLmsFkAiYg4LK3Z5-bTu9FQAn_3EKPg"

now = datetime.datetime.now()
mexico_time = now - datetime.timedelta(hours =  6)
mexico_hour = int(mexico_time.strftime("%H"))
#print(mexico_hour)

def start(bot, update):
    try:
        username = update.message.from_user.username + "\n\nEnvía una imagen para saber qué tipo de señal de transito es (requiere imagenes con tamaño grande)."
        if mexico_hour >= 0 and mexico_hour <= 11:
            message = "Buenos días " + username
        elif mexico_hour >= 12 and mexico_hour <= 18:
            message = "Buenas tardes " + username 
        elif mexico_hour >= 19 and mexico_hour <= 23:
            message = "Buenas noches " + username
        else:
            message = "Hola " + username
        update.message.reply_text(message)
    except Exception as error:
        print("Error 001: {}".format(error.args[0]))

def echo(bot, update):
    try:
        text = update.message.text
        update.message.reply_text(text)
    except Exception as error:
        print("Error 002 {}".format(error.args[0]))

def help(bot, update):
    try:
        message = "Puedes enviar texto o imagenes con tamañao grande."
        update.message.reply_text(message)
    except Exception as error:
        print("Error 003 {}".format(error.args[0]))

def error(bot, update, error):
    try:
        print(error)
    except Exception as e:
        print("Error 004 {}".format(e.args[0]))

def getImage(bot, update):
    try:
        message = "Recibiendo imagen"
        update.message.reply_text(message)

        file = bot.getFile(update.message.photo[-1].file_id)
        id = file.file_id

        filename = os.path.join("imagenes/", "{}.jpg".format(id))
        file.download(filename)
        
        message = "Imagen guardada"
        update.message.reply_text(message)

        files = { "myfile": open(filename, "rb") }
        message = "Procesando imagen"
        update.message.reply_text(message)
        result = requests.post("https://8080-silver-herring-vjtlg583.ws-us03.gitpod.io/index", files = files) 

        signal = result.json()
        items = signal[list(signal.keys())[0]]
        for i in items:      #accedemos a cada elemento de la lista (en este caso cada elemento es un dictionario)
            title = i["resultado"]
            description = i["descripcion"]

        message = "Resultado: "+title+"\nDescripción: "+description
        update.message.reply_text(message)

        if path.exists(filename):
            remove(filename)


    except Exception as e:
        print("Error 007: {}".format(e.args[0]))

def main():
    try:
        update = Updater(token)
        dp = update.dispatcher

        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))

        dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_handler(MessageHandler(Filters.photo, getImage))

        dp.add_error_handler(error)

        update.start_polling()
        update.idle()
    except Exception as e:
        print("Error 005: {}".format(e.args[0]))
        
if __name__ == "__main__":

    try:
        main()
    except Exception as error:
        print("Error 006 {}".format(error.args[0]))