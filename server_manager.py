from server import Server
from config import vk_api_token, group_id

server1 = Server(vk_api_token, group_id, "server1")
server1.start()
