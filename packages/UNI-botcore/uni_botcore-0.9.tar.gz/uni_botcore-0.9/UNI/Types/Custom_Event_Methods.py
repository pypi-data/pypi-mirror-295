from ..Uni_cfg import asyncio, Namespace, Bot_Object, inspect
from ..Datas import Data

from ..Types.Keyboards_ import InlineKeyboardMarkup
from ..Types.Reply_ import ReplyParameters



class Message_Event_Methods():

	async def reply(
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
		reply_parameters: ReplyParameters = {},
		reply_markup: InlineKeyboardMarkup = {}
	):

		reply_param = ReplyParameters(message_id=self.id, chat_id=self.chat.id)

		return await self.bot_object.send_message(
			chat_id=self.chat.id,
			text=text,
			business_connection_id=business_connection_id,
			message_thread_id=message_thread_id,
			parse_mode=parse_mode,
			entities=entities,
			link_preview_options=link_preview_options,
			disable_notification=disable_notification,
			protect_content=protect_content,
			message_effect_id=message_effect_id,
			reply_parameters=reply_param.json_obj,
			reply_markup=reply_markup
		)

		return res


	async def edit(
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

		return await self.bot_object.edit_message_text(
			text=text,
			chat_id=self.chat.id,
			message_id=self.message_id,
			business_connection_id = '',
			inline_message_id = 0,
			parse_mode = 'HTML',
			entities = [],
			link_preview_options = {},
			reply_markup = {}
		)


	async def delete(
		self,
		chat_id: int = 0,
		message_id: int = 0
	):


		await self.bot_object.delete_message(
			chat_id=self.chat.id,
			message_id=self.message_id
		)


	async def forward(
		self,
		chat_id: int,
		message_thread_id: int = 0
	):

		await self.bot_object.forward_message(
			chat_id=chat_id,
			message_id=self.message_id,
			from_chat_id=self.chat.id,
			message_thread_id=int(message_thread_id)
		)

	async def set_reaction(
		self,
		reaction: list
	):

		return await self.bot_object.set_message_reaction(
			chat_id=self.chat.id,
			message_id=self.message_id,
			reaction=reaction
		)



class Command_Event_Methods():

	async def reply(
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
		reply_parameters: ReplyParameters = {},
		reply_markup: InlineKeyboardMarkup = {}
	):

		reply_param = ReplyParameters(message_id=self.message_id, chat_id=self.chat.id)

		return await self.bot_object.send_message(
			chat_id=self.chat.id,
			text=text,
			business_connection_id=business_connection_id,
			message_thread_id=message_thread_id,
			parse_mode=parse_mode,
			entities=entities,
			link_preview_options=link_preview_options,
			disable_notification=disable_notification,
			protect_content=protect_content,
			message_effect_id=message_effect_id,
			reply_parameters=reply_param.json_obj,
			reply_markup=reply_markup
		)

		return res


	async def edit(
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

		return await self.bot_object.edit_message_text(
			text=text,
			chat_id=self.chat.id,
			message_id=self.message_id,
			business_connection_id = '',
			inline_message_id = 0,
			parse_mode = 'HTML',
			entities = [],
			link_preview_options = {},
			reply_markup = {}
		)


	async def delete(
		self,
		chat_id: int = 0,
		message_id: int = 0
	):


		await self.bot_object.delete_message(
			chat_id=self.chat.id,
			message_id=self.message_id
		)


	async def forward(
		self,
		chat_id: int,
		message_thread_id: int = 0
	):

		await self.bot_object.forward_message(
			chat_id=chat_id,
			message_id=self.message_id,
			from_chat_id=self.chat.id,
			message_thread_id=int(message_thread_id)
		)



class Callback_Event_Methods():

	async def answer(
		self,
		text: str = '',
		show_alert: bool = False,
		url: str = '',
		cache_time: int = 0
	):

		return await self.bot_object.callback_answer(
			callback_query_id=self.id,
			text=text,
			show_alert=show_alert,
			url=url,
			cache_time=cache_time
		)


	async def edit(
		self,
		text: str,
		business_connection_id: str = '',
		inline_message_id: int = 0,
		parse_mode: str = 'HTML',
		entities: list = [],
		link_preview_options: dict = {},
		reply_markup: InlineKeyboardMarkup = {}
	):

		return await self.bot_object.edit_message_text(
			text=text,
			chat_id=self.message.chat.id,
			message_id=self.message.message_id,
			business_connection_id = '',
			inline_message_id = inline_message_id,
			parse_mode = parse_mode,
			entities = entities,
			link_preview_options = link_preview_options,
			reply_markup = reply_markup
		)


	async def delete(
		self,
		chat_id: int = 0,
		message_id: int = 0
	):


		await self.bot_object.delete_message(
			chat_id=self.message.chat.id,
			message_id=self.message.message_id
		)


	async def pattern_edit(self, pattern: Namespace, args_: tuple = None, msg_id: int = 0):

		user = await self.bot_object.BAG.Custom_Packs.pack_user(user_id=self.event.from_user.id)
		args_ = (user,) + (args_ if args_ is not None else ())

		# if self.event_type == 'callback':

		# 	chat_id = self.event.message.chat.id
		# 	message_id = self.event.message.message_id

		# 	text = getattr(texts, pattern)
		# 	signature = inspect.signature(text)

		# 	keyboard = getattr(keyboards, pattern)

		# 	#------------
		# 	arg_names = list(signature.parameters.keys())
		# 	args_dict = {arg: args_[index] for index, arg in enumerate(arg_names)}
			
		# 	msg = await botToken.edit_message_text(
		# 		chat_id=chat_id, 
		# 		message_id=message_id, 
		# 		text=await text(**args_dict), 
		# 		reply_markup=await keyboard(**args_dict), 
		# 		parse_mode='HTML',
		# 		disable_web_page_preview=True
		# 	)

		# 	return msg

		#elif self.event_type == 'text':

		print(f'сработал паттерн едит', msg_id)

		chat_id = self.event.message.chat.id
		message_id = msg_id if msg_id != 0 else self.event.message.message_id

		text = getattr(self.bot_object.BAG.texts, pattern)
		signature = inspect.signature(text)

		keyboard = getattr(self.bot_object.BAG.keyboards, pattern)

		#------------
		arg_names = list(signature.parameters.keys())
		args_dict = {arg: args_[index] for index, arg in enumerate(arg_names)}
		
		print(f'редачим паттерн эдитом')

		try:

			msg = await self.bot_object.edit_message_text(
				chat_id=int(chat_id), 
				message_id=int(message_id), 
				text=await text(**args_dict), 
				reply_markup=await keyboard(**args_dict), 
				parse_mode='HTML'
			)

		except Exception as e:
			print(f'ОШИБКА ПАТТЕРН ЭДИТА:\n\nARGS: {args_dict}')
			pass

		return msg



class Inline_Event_Methods():

	async def answer(
		self,
		results: list = [],
		cache_time: int = 0,
		is_personal: bool = True,
		next_offset: str = '',
		button: dict = {}
	):

		#print(locals())

		return await self.bot_object.inline_answer(
			inline_query_id=self.id,
			results=results,
			cache_time=cache_time,
			is_personal=is_personal,
			next_offset=next_offset,
			button=button
		)