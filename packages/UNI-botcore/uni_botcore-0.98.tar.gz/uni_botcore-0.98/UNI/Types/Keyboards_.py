from ..Uni_cfg import asyncio, Namespace
from ..Datas import Data


class InlineKeyboardMarkup():

	def __init__(self, row: int = 1):

		self.row = row
		self.raw_keyboard = {'inline_keyboard': []}

	def __repr__(self):
		return str(self.raw_keyboard)

	def __str__(self):
		return str(self.raw_keyboard)


	def add(
		self,
		text: str,
		url: str = '',
		callback_data: str = '',
		web_app: dict = {},
		login_url: dict = {},
		switch_inline_query: str = '',
		switch_inline_query_current_chat: str = '',
		switch_inline_query_chosen_chat: dict = {},
		callback_game: dict = {},
		pay: bool = False
		):


		cleaned_json = Data.rebuild_json_(locals())

		self.raw_keyboard['inline_keyboard'].append([cleaned_json])

		return self


	def insert(
		self,
		text: str,
		url: str = '',
		callback_data: str = '',
		web_app: dict = {},
		login_url: dict = {},
		switch_inline_query: str = '',
		switch_inline_query_current_chat: str = '',
		switch_inline_query_chosen_chat: dict = {},
		callback_game: dict = {},
		pay: bool = False
		):

		last_block = None

		if len(self.raw_keyboard['inline_keyboard']) == 0:
			self.raw_keyboard['inline_keyboard'].append([])
			last_block = self.raw_keyboard['inline_keyboard'][0]
		else:
			self.raw_keyboard['inline_keyboard'][len(self.raw_keyboard['inline_keyboard'])-1]
			last_block = self.raw_keyboard['inline_keyboard'][len(self.raw_keyboard['inline_keyboard'])-1]


		if len(last_block) < self.row:

			cleaned_json = Data.rebuild_json_(locals())
			del cleaned_json['last_block']
			last_block.append(cleaned_json)
		else:

			cleaned_json = Data.rebuild_json_(locals())
			del cleaned_json['last_block']
			self.raw_keyboard['inline_keyboard'].append([cleaned_json])

		return self



class InlineQueryResultsButton():

	def __init__(
		self, 
		text: str, 
		web_app: dict = {}, 
		start_parameter: str = ''
		):

		self.text = text
		self.web_app = web_app
		self.start_parameter = start_parameter

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))