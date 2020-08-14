# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests


token = "token"
group_id = "group_id"
group_id = int(group_id)
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id)
session = requests.Session()
upload = vk_api.VkUpload(vk_session)
attachments = []

def DeleteAllAttachments(attachments):
    while attachments:
            attachments.pop()

def SomeToOneAttachment(attachments):
    while len(attachments) > 1:      # Иногда может попасться баг, когда 2 одинаковых вложения
        attachments.pop()            # Не знаю, почему так происходит, но баг исправлен этим циклом

def IdentificationAttachment(attachment):               # Определение вложения по номеру
    if attachment == 1:                                                     # Поклон
        DeleteAllAttachments(attachments)
        photo = upload.photo_messages(photos='pictures/Greeting.jpg')[0]
        attachments.append(
            'photo{}_{}'.format(photo['owner_id'], photo['id']))
        SomeToOneAttachment(attachments)

    elif attachment == 2:                                                   # Проверка
        DeleteAllAttachments(attachments)                                           
        photo = upload.photo_messages(photos='pictures/Excellent.jpg')[0]
        attachments.append(
            'photo{}_{}'.format(photo['owner_id'], photo['id']))
        SomeToOneAttachment(attachments)

    else:
        DeleteAllAttachments(attachments)
   
    # TODO: при успешном прикладывании возвращать 0, иначе возвращать код ошибки и писать это в чат

def Send_Message(chat_id, attachment, message):         # Функция для отправки сообщений
    IdentificationAttachment(attachment = attachment)

    vk.messages.send(
        chat_id=chat_id,
        attachment=','.join(attachments),
        random_id=get_random_id(),
        message=message)

def main():
    print("Bot is working")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.text.lower() == "проверка":
                if event.from_chat:
                    Send_Message(
                        chat_id=event.chat_id,
                        attachment = 0,
                        message = ("Вложений - " + str(len(attachments))))

            elif event.obj.text == "👉🏻" or event.obj.text == "👉":
                if event.from_chat:
                    Send_Message(
                        chat_id = event.chat_id,
                        attachment = 0,
                        message = "NIGGA")

            elif 'поклон' in event.obj.text.lower().split():
                if event.from_chat:
                    try:
                        if (event.obj.text.lower().split()[1][0] == '['): # Проверка на наличие айди в сообщении
                            source = str(event.obj.from_id) # Тот, кто передает поклон
                            destination = event.obj.text.lower().split()[1] # Тот, кто получает поклон

                            destination = destination.replace(destination[0], '', 1)    # Удаление первого символа
                            j = destination.index('|')                                  # Ищем "перегородку"
                            destination = list(destination)                             # Переводим в другой тип для дальнейшей очистки
                            while j != len(destination):                                # Здесь начинается основная очистка
                                del destination[j]                                      # Удаляем все после "id12345..."
                            destination = ''.join(destination)                          # Соединяем все в строку

                            if source == "228631995":
                                if destination == "id228631995":    # Если создатель передает поклон сам себе
                                    Send_Message(
                                        chat_id = event.chat_id,
                                        attachment = 2,
                                        message = "Проверка прошла успешно")

                                else:                               # Если создатель передает поклон кому-то
                                    Send_Message(
                                        chat_id = event.chat_id,
                                        attachment = 1,
                                        message = "[" + destination + "|Вам] поклон от [id" + source + "|мистера Сальери].")
                                    

                            elif destination == "id228631995":  # Если кто-то хочет передать поклон дону
                                Send_Message(
                                    chat_id = event.chat_id,
                                    attachment = 1,
                                    message = "Вы не можете напасть на дона. [id" + source + "|Вам] поклон от [" + destination + "|мистера Сальери].")

                            else:                               # Если кто-то хочет передать поклон кому-то
                                Send_Message(
                                    chat_id = event.chat_id,
                                    attachment = 1,
                                    message = "[" + destination + "|Вам] поклон от [id" + source + "|заказчика].")
                    except IndexError:
                        pass

if __name__ == '__main__':
    main()