import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import random
from config import vk_ids
from config import vk_id
import requests


def photo_download(url):
    r = requests.get(url, stream=True)
    r.raw.decode_content = True
    buffer = r.raw
    return buffer.data


def photo_upload(url, data):
    files = {'photo': ("file.png", data, 'multipart/form-data')}
    r = requests.post(url, files=files)
    return r.json()


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message, attachment):
        try:
            self.vk_api.messages.send(
                peer_id=send_id,
                message=message,
                random_id=random.randint(0, 10000000),
                attachment=attachment
            )
        except vk_api.exceptions.ApiError:
            print ("zanyatonahuy")

    def start(self):
        for event in self.long_poll.listen():
            if event.object.from_id == vk_id and event.type == VkBotEventType.MESSAGE_NEW:
                for current_id in vk_ids:
                    upload_server = self.vk_api.photos.getMessagesUploadServer(peer_id=vk_id)
                    attachments = []
                    for attachment in event.object['attachments']:
                        sizes = attachment['photo']['sizes']
                        url = sizes[-1]['url']
                        photo_raw = photo_download(url)
                        photo_data = photo_upload(upload_server['upload_url'], data=photo_raw)
                        photo_api_data = self.vk_api.photos.saveMessagesPhoto(**photo_data)
                        attachments.append(f"photo{photo_api_data[0]['owner_id']}_{photo_api_data[0]['id']}")
                    self.send_msg(send_id=current_id, message=event.object.text, attachment=','.join(attachments))
            print(event)
