from ..Uni_cfg import asyncio, Namespace
from ..Types.Keyboards_ import InlineKeyboardMarkup
from ..Types.Message_Content_ import InputMessageContent

from ..Datas import Data



class InlineQueryResult():

	def __init__(self):
		
		self.result_ = []

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))


	class InlineQueryResultArticle():

		def __init__(
			self,
			id: str,
			title: str,
			input_message_content: InputMessageContent,
			type: str = 'article',
			reply_markup: InlineKeyboardMarkup = {},
			url: str = '',
			hide_url: bool = False,
			description: str = '',
			thumbnail_url: str = '',
			thumbnail_width: int = 0,
			thumbnail_height: int = 0
		):

			builded_json = Data.rebuild_json_(locals())


			self.json_obj = builded_json
			self.type = type,
			self.id = id,
			self.title = title,
			self.input_message_content = input_message_content,
			self.reply_markup = reply_markup,
			self.url = url,
			self.hide_url = hide_url,
			self.description = description,
			self.thumbnail_url = thumbnail_url,
			self.thumbnail_width = thumbnail_width,
			self.thumbnail_height = thumbnail_height


			def __repr__(self):
				return str(vars(self))

			def __str__(self):
				return str(vars(self))


	def article(
		self,
		id: str,
		title: str,
		input_message_content: InputMessageContent,
		type: str = 'article',
		reply_markup: InlineKeyboardMarkup = {},
		url: str = '',
		hide_url: bool = False,
		description: str = '',
		thumbnail_url: str = '',
		thumbnail_width: int = 0,
		thumbnail_height: int = 0
	):
	
		self.result_.append(
			InlineQueryResult.InlineQueryResultArticle(
				id = id,
				title = title,
				input_message_content = input_message_content.json_obj if input_message_content != {} else {},
				type = type,
				reply_markup = reply_markup.raw_keyboard if reply_markup != {} else reply_markup,
				url = url,
				hide_url = hide_url,
				description = description,
				thumbnail_url = thumbnail_url,
				thumbnail_width = thumbnail_width,
				thumbnail_height = thumbnail_height
			)
		)

