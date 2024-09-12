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
		allowed_updates: list = [],
		dict_: bool = False
		):

		data = {'offset': offset, 'limit': limit, 'timeout': timeout, 'allowed_updates': allowed_updates}

		url = f'https://api.telegram.org/bot{bot_object.cur_bot_token}/getUpdates'
		res = await rest_side.Rest.post(url=url, json=data)

		if dict_ == False:
			return CustomNamespace(res.json)
		else:
			return CustomNamespace(res.json), res.json



	async def get_last_uni_version():

		url = f'https://pypi.org/pypi/toncenter-sdk-python/json'
		res = await rest_side.Rest.get(url=url)

		return CustomNamespace(res.json)


	# 	async def check_library_update(library_name):
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f"https://pypi.org/pypi/{library_name}/json") as response:
    #         data = await response.json()
    #         latest_version = data['info']['version']
    #         print(f"The latest version of {library_name} is {latest_version}")