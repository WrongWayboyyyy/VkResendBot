from os import environ


vk_api_token = environ["vk_api_token"]
vk_ids = list(map(int, environ["vk_ids"].split(',')))

vk_id = int(environ["vk_id"])
group_id = int(environ["group_id"])

