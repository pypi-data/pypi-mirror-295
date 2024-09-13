from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query

from ..Types.Keyboards_ import InlineKeyboardMarkup
from ..Types.Reply_ import ReplyParameters
from ..Types.Entities_ import LinkPreviewOptions



class Message_Methods():

	async def send_message(
		self,
		chat_id: int,
		text: str,
		business_connection_id: str = '',
		message_thread_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: LinkPreviewOptions = LinkPreviewOptions().json_obj,
		disable_notification: bool = False,
		protect_content: bool = False,
		message_effect_id: str = '',
		reply_parameters: ReplyParameters = {},
		reply_markup: InlineKeyboardMarkup = {}
		):

		json_ = await Data.rebuild_json(locals())

		if reply_markup != {}:
			json_['reply_markup'] = reply_markup.raw_keyboard
			
		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='sendMessage')


	async def delete_message(
		self,
		chat_id: int,
		message_id: int
		):

		json_ = await Data.rebuild_json(locals())

		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='deleteMessage')


	async def edit_message_text(
		self,
		text: str,
		chat_id: int,
		message_id: int,
		business_connection_id: str = '',
		inline_message_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: dict = {},
		reply_markup: InlineKeyboardMarkup = {}
		):


		json_ = await Data.rebuild_json(locals())

		if reply_markup != {}:
			json_['reply_markup'] = reply_markup.raw_keyboard

		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='editMessageText')