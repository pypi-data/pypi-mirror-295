from .Uni_cfg import asyncio, Namespace, traceback, time, json, v_, time, os

from .Converters import primary_converter
from .Datas.Data import wrap_namespace

from .Bot_Under_Methods.Main_ import Main_Methods
from .Bot_Under_Methods.Message_ import Message_Methods
from .Bot_Under_Methods.Callback_ import Callback_Methods
from .Bot_Under_Methods.Inline_ import Inline_Methods
from .Bot_Under_Methods.Chat_ import Chat_Methods


from .Sides import rest_side, ssh_side


class Dispatcher(
	Message_Methods,
	Callback_Methods,
	Inline_Methods,
	Chat_Methods
	):

	def __init__(self, 
		bot_token: str,
		BAG: Namespace = None,
		test_bot_token: str = '', 
		testbot: bool = False, 
		allowed_updates: list = [
			"message", 
			"inline_query", 
			"callback_query",
			"chat_member",
			'message_reaction',
			'chat_join_request'
		],
		tasks: list = []
		):

		self.bot_token = bot_token
		self.test_bot_token = test_bot_token
		self.testbot = testbot
		self.cur_bot_token = bot_token if testbot == False else test_bot_token

		self.allowed_updates = allowed_updates
		self.tasks = tasks


	def run(self):

		print(time.time())
		asyncio.run(self.pooling())


	async def pooling(self):

		#print(f'BAG: {self.BAG}')

		for task_ in self.tasks:
			asyncio.create_task(task_)

		asyncio.create_task(self.autoupdate())


		offset = 1
		last_update_id = 0
		while True:
			try:

				updates_, json_updates_  = await Main_Methods.get_updates(
					bot_object= self, 
					offset=offset, 
					allowed_updates=self.allowed_updates,
					dict_=True
				)
				updates = updates_.result
				#json_updates_ = await updates_.to_dict()
				json_updates = json_updates_['result']

				print(updates)#дописать

				if len(updates) > 0:

					cur_update = updates[0]
					cur_json_update = json_updates[0]
					

					if cur_update.update_id != last_update_id:

						last_update_id = cur_update.update_id
						#print(cur_update)
						#logging.debug(updates)
						print(json.dumps(cur_json_update, indent=4))

						# print(f'ПОЛУЧИЛИ АПДЕЙТ: {time.time()}')
						# url = f'https://api.telegram.org/bot{self.cur_bot_token}/sendMessage'
						# data={"chat_id": 1939628022, "text": 'test'}
						# res = await rest_side.Rest.post(url=url, json=data)
						print(f'отправляем на обработку: {time.time()}')

						result = await primary_converter.process_update(update=cur_update, bot_object=self)
						offset=cur_update.update_id+1

				await asyncio.sleep(.01)
				#print('---')

			except Exception as e:
				try:
					traceback.print_exc()
				except Exception as e:
					pass
				continue






	async def autoupdate(self):

		while True:
			try:
				print(f'ЧЕКАЕМ ОБНОВУ ПАКЕТА')
				last_version = await self.get_last_version()
				print(f'CUR V: {v_} | LAST V: {last_version}')
				if v_ != last_version:
					print(f'версии разные')

					await ssh_side.send_ssh_query(hostname=self.BAG.hostserver.name, username=self.BAG.hostserver.username, password=self.BAG.hostserver.password, command=f'pip install UNI-botcore=={last_version}')
					await asyncio.sleep(1)
					await ssh_side.send_ssh_query(hostname=self.BAG.hostserver.name, username=self.BAG.hostserver.username, password=self.BAG.hostserver.password, command=f'pip install UNI-botcore=={last_version}')
					#await ssh_side.send_ssh_query(hostname=self.BAG.hostserver.name, username=self.BAG.hostserver.username, password=self.BAG.hostserver.password, command=f'pm2 restart {self.BAG.bot_name}')
					os.system(f'pm2 restart {self.BAG.bot_name}')

				await asyncio.sleep(120)
			except Exception as e:
				traceback.print_exc()
				pass


	async def get_last_version(self):

		last_v_query = await Main_Methods.get_last_uni_version()
		last_v = last_v_query.info.version
		return last_v