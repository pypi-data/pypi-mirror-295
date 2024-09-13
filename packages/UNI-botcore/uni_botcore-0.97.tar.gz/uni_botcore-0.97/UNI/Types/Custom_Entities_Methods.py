from ..Uni_cfg import asyncio, Namespace, Bot_Object
from ..Datas import Data
from ..Types.Keyboards_ import InlineKeyboardMarkup



class Chat_Methods():

	async def send_message(
		self,
		text: str,
		business_connection_id: str = '',
		message_thread_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: dict = {},
		disable_notification: bool = False,
		protect_content: bool = False,
		message_effect_id: str = '',
		reply_parameters: dict = {},
		reply_markup: InlineKeyboardMarkup = {}
	):

		return await self.bot_object.send_message(
			chat_id=self.id,
			text=text,
			business_connection_id=business_connection_id,
			message_thread_id=message_thread_id,
			parse_mode=parse_mode,
			entities=entities,
			link_preview_options=link_preview_options,
			disable_notification=disable_notification,
			protect_content=protect_content,
			message_effect_id=message_effect_id,
			reply_parameters=reply_parameters,
			reply_markup=reply_markup
		)
