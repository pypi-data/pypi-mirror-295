from ..Uni_cfg import asyncio, Namespace, time
from ..Sides import rest_side
from ..Datas import Data
from ..Datas.Data import CustomNamespace


async def send_query(bot_object: Namespace, data: dict, method: str) -> dict:

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))

	#print(f'кидаем запрос к серверу: {time.time()}')
	url = f'https://api.telegram.org/bot{bot_object.cur_bot_token}/{method}'
	res = await rest_side.Rest.post(url=url, json=data)
	#return await Data.wrap_dict(res.json), res.json

	#print(f'получили ответ от сервера: {time.time()}')
	#print(f'RES JSON: {res.json}')
	return CustomNamespace(res.json['result']) if 'result' in res.json.keys() else res.json