from .Datas.process_data import process_output
from methods import texts
from .Uni_cfg import Optional, List, inspect, basename, splitext, wraps, traceback, time, Optional, Callable, Dict, Any, List
from .Communicate import handl
from .Converters.primary_converter import classificate_update_type
from .Types import Events_, Pack_Events
from .Datas.uni_filters import check_filters_equal
from .Datas.get_data import _get_event_chat_type, _get_user
from .Datas.Data import wrap_namespace, wrap_dict, replace_dict_keyname
from .Datas.process_data import process_callback_data, _process_callback_data_decorator


from .Types.Entities_ import Chat




def decorate_all_functions(decorator):
	def decorate(cls):
		for key, val in cls.__dict__.items():
			if callable(val) and inspect.iscoroutinefunction(val):
				setattr(cls, key, decorator(val))
		return cls
	return decorate


texts = decorate_all_functions(process_output)(texts)





async def toFixed(numObj, digits=0):

	return f"{numObj:.{digits}f}"



async def gen_uid(tablename: str = '', uid_type='int', lenght=6, column_name='uid'):

	while True:

		uid = None

		if uid_type == 'int':

			uid = int(''.join([str(randint(0, 9)) for _ in range(lenght)]))

		elif uid_type == 'str':

			characters = string.ascii_letters + string.digits + string.punctuation
			uid = ''.join(random.choice(characters) for i in range(lenght))

		result_uid = await db.execute('SELECT * FROM '+tablename+' WHERE '+column_name+' = $1', (uid, ))

		if not result_uid:

			return uid




@staticmethod
def uni_handler(
	commands: Optional[List[str]] = [], 
	callback_filters: Optional[str] = ['all'],
	content_types: Optional[List[str]] = list(Events_.events_templates.keys()), #['text', 'photo', 'video', 'document', 'sticker', 'animation', 'callback', 'inline_query', 'chat_member', 'my_chat_member', 'message_reaction'],
	chat_types: Optional[str] = [],#types.ChatType.PRIVATE,
	equal: Optional[List[str]] = [],
	lock_event_type: Optional[List[str]] = [],
	event=None, user=None, keyboards=None, texts=None):

	handler_filters_ = locals()

	def decorator(func):

		file_path = inspect.getfile(func)
		type_ = str(splitext(basename(file_path))[0]).split('_')[0] if not 'messages' in str(splitext(basename(file_path))[0]).split('_')[1] else  f"{str(splitext(basename(file_path))[0]).split('_')[0]}_messages" #получаем каждый декоратор из отдельного файла и исходя из названия файла присваиваем ему тип хендлера

		# @wraps(func)
		# async def wrapped_event_handler(event, event_data_path, bot_object, update_type_, *args):

		# 	try:
				
		# 		#print(f'достаем ивентайпы в юнике: {time.time()}')
		# 		event_type = update_type_#await classificate_update_type(update=event, event_data_path=event_data_path)
		# 		event_chat_type = await _get_event_chat_type(event=event, event_type=event_type)

		# 		#print(f'забрали ивентайпы в юнике: {time.time()}')

		# 		#print(f'определяем и собираем ивент в юнике: {time.time()}')
		# 		event = await event.to_dict() 
		# 		update_refreshed_dict = None

		# 		if 'from' in list(event.keys()):
		# 			update_refreshed_dict = await replace_dict_keyname(d=event, old_keyname='from', new_keyname='from_user')
		# 		elif 'user' in list(event.keys()):
		# 			update_refreshed_dict = await replace_dict_keyname(d=event, old_keyname='user', new_keyname='from_user')

		# 		event = await wrap_dict(update_refreshed_dict)


		# 		if hasattr(event, 'chat'):
		# 			event.chat = Chat(
		# 				bot_object, 
		# 				event.chat.id,
		# 				event.chat
		# 				)

		# 		if hasattr(event, 'from_user'):
		# 			#print(f'FROM US: {event.from_user}')
		# 			event.from_user = Chat(
		# 				bot_object, 
		# 				event.from_user.id,
		# 				event.from_user
		# 				)




		# 		fdata = None
		# 		args = []
		# 		event_commands = []


		# 		if event_type == 'callback':
		# 			fdata = await _process_callback_data_decorator(event)

		# 		#if event_type in ['text', 'business_message']:
		# 		if Events_.events_templates[event_type]['enable_commands'] == True:
		# 			try:
		# 				args = event.text.split()[1:]
		# 			except Exception as e:
		# 				#traceback.print_exc()
		# 				args = []
				
		# 			try:
		# 				#print(f'EVENT TEXT: {event.text}')
		# 				if '/' in event.text:
		# 					event_commands = event.text.split("/")
		# 					event_commands = [command.split(' ')[0] for command in event_commands if command]
		# 			except Exception as e:
		# 				traceback.print_exc()
		# 				event_commands = []


		# 		event_quick_name = Events_.events_templates[event_type]['quick_name']
		# 		custom_shell_path = getattr(Pack_Events, f'{event_quick_name.title()}_Event')

		# 		custom_event = custom_shell_path(event=event, fdata=fdata, bot_object=bot_object)
		# 		custom_event.fdata = fdata
		# 		custom_event.args = args
		# 		custom_event.event_type = event_type
		# 		custom_event.commands = event_commands
		# 		custom_event.chat_type = event_chat_type

		# 		#print(f'собрали ивент в юнике: {time.time()}')

		# 		equal_filters = await check_filters_equal(handler_filters_, event, event_commands, event_type, content_types, lock_event_type, equal, commands, callback_filters, chat_types, event_chat_type)
				
		# 		#print(f'прошли фильтры в юнике: {time.time()}')

		# 		if equal_filters == True:

		# 			#print(f'собираем данные клавиатуры и юзера в юнике: {time.time()}')
		# 			user, keyboards, texts = await _get_user(bot_object, event)

		# 			#print(f'данные собраны, отправка на хендлер : {time.time()}')
		# 			#print(f'KB: {keyboards}')
		# 			#print(f'вызываем функцию в юнике: {time.time()}')
		# 			await func(custom_event, user, keyboards, texts)
		# 			#print(f'функция отработала в юнике: {time.time()}')
		# 			return True

		# 	except Exception as e:
		# 		traceback.print_exc()
		# 		pass


		@wraps(func)
		async def wrapped_event_handler(
			event: Any,
			event_data_path: str,
			bot_object: Any,
			update_type_: str,
			*args: Any
		) -> Optional[bool]:
			try:

				print(f'определяем тип чата: {time.time()}')
				# Определяем тип события
				event_type = update_type_
				event_chat_type = await _get_event_chat_type(event=event, event_type=event_type)

				print(f'собираем ивент в словарь: {time.time()}')
				# Преобразование события в словарь и обновление ключей
				event_dict = await event.to_dict()  # Используйте `await` если это асинхронная операция


				print(f'заменяем ключи в собранном словаре: {time.time()}')
				# Замена ключей 'from' или 'user' на 'from_user'
				if 'from' in event_dict:
					event_dict = await replace_dict_keyname(d=event_dict, old_keyname='from', new_keyname='from_user')
				elif 'user' in event_dict:
					event_dict = await replace_dict_keyname(d=event_dict, old_keyname='user', new_keyname='from_user')

				# Создание объекта события

				print(f'оборачиваем ивент: {time.time()}')
				event = await wrap_dict(event_dict)

				# Обновление атрибутов чата и пользователя
				if hasattr(event, 'chat'):
					event.chat = Chat(bot_object, event.chat.id, event.chat)

				if hasattr(event, 'from_user'):
					event.from_user = Chat(bot_object, event.from_user.id, event.from_user)

				# Обработка данных события
				fdata: Optional[Any] = None
				parsed_args: List[str] = []
				event_commands: List[str] = []

				if event_type == 'callback':
					fdata = await _process_callback_data_decorator(event)

				if Events_.events_templates[event_type].get('enable_commands', False):
					text = getattr(event, 'text', '')
					parsed_args = text.split()[1:] if text else []

					if '/' in text:
						event_commands = [cmd.split(' ')[0] for cmd in text.split('/') if cmd]


				print(f'создаем кастомное событие: {time.time()}')
				# Создание кастомного события
				event_quick_name = Events_.events_templates[event_type]['quick_name']
				custom_shell_path = getattr(Pack_Events, f'{event_quick_name.title()}_Event')
				custom_event = custom_shell_path(event=event, fdata=fdata, bot_object=bot_object)
				custom_event.fdata = fdata
				custom_event.args = parsed_args
				custom_event.event_type = event_type
				custom_event.commands = event_commands
				custom_event.chat_type = event_chat_type


				print(f'проверяем фильтры: {time.time()}')
				equal_filters = await check_filters_equal(
					handler_filters_,
					event,
					event_commands,
					event_type,
					content_types,
					lock_event_type,
					equal,
					commands,
					callback_filters,
					chat_types,
					event_chat_type
				)

				#equal_filters = True

				if equal_filters:

					print(f'собираем юзера и клавиатуру с текстом: {time.time()}')
					user, keyboards, texts = await _get_user(bot_object, event)
					print(f'запускаем хендлер: {time.time()}')
					await func(custom_event, user, keyboards, texts)
					return True

			except Exception:
				traceback.print_exc()
				return None  # Возвращаем None в случае ошибки


		# @wraps(func)
		# async def simulate_event_handler(event, event_data_path, bot_object, update_type_, *args):

		# 	try:

		# 		#print(f'EVENT_: {event}')
		# 		#event_type = await classificate_update_type(update=event, event_data_path=event_data_path)
		# 		event_type = update_type_
		# 		#print(f'EVENT TYPE: {event_type}')
		# 		event_chat_type = await _get_event_chat_type(event=event, event_type=event_type)
		# 		#print(event_type, event_chat_type)
		# 		fdata = None
		# 		args = []
		# 		event_commands = []


		# 		if event_type == 'callback':
		# 			fdata = await _process_callback_data_decorator(event)

		# 		#if event_type in ['text', 'business_message']:
		# 		if Events_.events_templates[event_type]['enable_commands'] == True:
		# 			try:
		# 				args = event.text.split()[1:]
		# 			except Exception as e:
		# 				#traceback.print_exc()
		# 				args = []
				
		# 			try:
		# 				#print(f'EVENT TEXT: {event.text}')
		# 				if '/' in event.text:
		# 					event_commands = event.text.split("/")
		# 					event_commands = [command.split(' ')[0] for command in event_commands if command]
		# 			except Exception as e:
		# 				traceback.print_exc()
		# 				event_commands = []


		# 		event_quick_name = Events_.events_templates[event_type]['quick_name']
		# 		custom_shell_path = getattr(Pack_Events, f'{event_quick_name.title()}_Event')

		# 		custom_event = custom_shell_path(event=event, fdata=fdata, bot_object=bot_object)
		# 		custom_event.fdata = fdata
		# 		custom_event.args = args
		# 		custom_event.event_type = event_type
		# 		custom_event.commands = event_commands
		# 		custom_event.chat_type = event_chat_type


		# 		equal_filters = await check_filters_equal(handler_filters_, event, event_commands, event_type, content_types, lock_event_type, equal, commands, callback_filters, chat_types, event_chat_type)
		# 		#print(equal_filters)
		# 		return equal_filters

		# 	except Exception as e:
		# 		traceback.print_exc()
		# 		pass



		@wraps(func)
		async def simulate_event_handler(event: Any, event_data_path: str, bot_object: Any, update_type_: str, *args: Any) -> Optional[bool]:
			try:
				# Определяем тип события
				event_type = update_type_

				# Получаем тип чата
				event_chat_type = await _get_event_chat_type(event=event, event_type=event_type)
				
				fdata: Optional[Any] = None
				parsed_args: List[str] = []
				event_commands: List[str] = []

				# Обработка callback-событий
				if event_type == 'callback':
					fdata = await _process_callback_data_decorator(event)

				# Обработка текстовых команд, если они разрешены
				if Events_.events_templates[event_type].get('enable_commands', False):
					text = getattr(event, 'text', '')
					parsed_args = text.split()[1:] if text else []
					
					if '/' in text:
						event_commands = [cmd.split(' ')[0] for cmd in text.split('/') if cmd]

				# Создаем кастомное событие
				event_quick_name = Events_.events_templates[event_type]['quick_name']
				custom_shell_path = getattr(Pack_Events, f'{event_quick_name.title()}_Event')
				custom_event = custom_shell_path(event=event, fdata=fdata, bot_object=bot_object)
				custom_event.fdata = fdata
				custom_event.args = parsed_args
				custom_event.event_type = event_type
				custom_event.commands = event_commands
				custom_event.chat_type = event_chat_type

				# Проверяем фильтры
				equal_filters = await check_filters_equal(
					handler_filters_,
					event,
					event_commands,
					event_type,
					content_types,
					lock_event_type,
					equal,
					commands,
					callback_filters,
					chat_types,
					event_chat_type
				)
				
				return equal_filters

			except Exception:
				traceback.print_exc()
				return None  # Возвращаем None, если возникла ошибка

		#print(type_)
		if type_ == 'events':
			if lock_event_type != []:
				handl.register_handler(handler=wrapped_event_handler, handler_type=type_, handler_simulator=simulate_event_handler)
		else:
			handl.register_handler(handler=wrapped_event_handler, handler_type=type_, handler_simulator=simulate_event_handler)

		return func

	return decorator