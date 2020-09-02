from server import Server
from config import vk_api_token, group_id
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

server1 = Server(vk_api_token, group_id, "server1")
server1.start()
