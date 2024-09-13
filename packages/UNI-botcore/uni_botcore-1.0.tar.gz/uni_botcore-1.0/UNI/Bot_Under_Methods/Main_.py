from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from ..Datas.Data import CustomNamespace


class Main_Methods():

	async def get_updates(
		bot_object: Namespace, 
		offset: int = 0, 
		limit: int = 100, 
		timeout: int = 0, 
		allowed_updates: list = []
		):

		data = {'offset': offset, 'limit': limit, 'timeout': timeout, 'allowed_updates': allowed_updates}

		url = f'https://api.telegram.org/bot{bot_object.cur_bot_token}/getUpdates'
		res = await rest_side.Rest.post(url=url, json=data)
		return CustomNamespace(res.json)#await Data.wrap_dict(res.json), res.json


	async def get_last_uni_version():

		url = f'https://pypi.org/pypi/UNI-botcore/json'
		res = await rest_side.Rest.get(url=url)

		return CustomNamespace(res.json)