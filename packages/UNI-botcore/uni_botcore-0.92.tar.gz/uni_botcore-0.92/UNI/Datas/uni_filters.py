#from .uni_cfg import *
from ..Uni_cfg import asyncio, Namespace, Any, Dict, Set, List, Callable




async def check_equal(event: Namespace = None, event_type: str = '', equal: list = []) -> bool:

	if equal != []:

		if event_type == 'callback':
			if not event.data in equal:
				return False
			return True

		elif event_type == 'text':
			print(event_type, event.text, equal)
			if not event.text in equal:
				return False
			return True

	return True


# async def check_filters_equal(handler_filters_, event, event_commands, event_type, content_types, lock_event_type, equal, commands, callback_filters, chat_types, event_chat_type):

# 	cur_filters_enable = [i[0] for i in handler_filters_.items() if i[1] != None and i[1] != []]
# 	pre_done_filters = []

# 	#нужно просканить совпадения по фильтрам и если все правильно то пропустить ивент

# 	for filter_ in cur_filters_enable:

# 		if filter_ == 'commands':
# 			#print(commands, event_commands)
# 			if len(list(set(commands).intersection(event_commands))) > 0:
# 				pre_done_filters.append(filter_)

# 		elif filter_ == 'lock_event_type':
# 			if event_type in lock_event_type:
# 				pre_done_filters.append(filter_)

# 		elif filter_ == 'callback_filters':
# 			#print(callback_filters, event.data)
# 			try:
# 				if callback_filters[0] != 'all':
# 					if len([1 for cur_filter in callback_filters if str(cur_filter) in str(event.data)]) > 0:
# 						pre_done_filters.append(filter_)
# 				else:
# 					pre_done_filters.append(filter_)
# 			except Exception as e:
# 				pass

# 		elif filter_ == 'content_types':
# 			#print(f'КОНТЕНТ ТАЙП:', event_type, content_types)
# 			if event_type in content_types:
# 				pre_done_filters.append(filter_)

# 		elif filter_ == 'equal':
# 			if await check_equal(event=event, event_type=event_type, equal=equal) == True:
# 				pre_done_filters.append(filter_)

# 		elif filter_ == 'chat_types':
# 			#print(event_chat_type, chat_types)
# 			if event_chat_type in chat_types:
# 				pre_done_filters.append(filter_)


# 	#print(cur_filters_enable)
# 	#print(pre_done_filters)

# 	done_filters = [i for i in pre_done_filters if i in cur_filters_enable]

# 	if len(list(set(done_filters).intersection(cur_filters_enable))) == len(cur_filters_enable):
# 		return True
# 	else:
# 		return False

# async def check_filters_equal(handler_filters_, event, event_commands, event_type, content_types, lock_event_type, equal, commands, callback_filters, chat_types, event_chat_type):

# 	# Определяем включенные фильтры
# 	cur_filters_enable = {key for key, value in handler_filters_.items() if value}

# 	# Проверяем каждый фильтр по отдельности
# 	for filter_ in cur_filters_enable:

# 		if filter_ == 'commands':
# 			if set(commands).intersection(event_commands):
# 				continue

# 		elif filter_ == 'lock_event_type':
# 			if event_type in lock_event_type:
# 				continue

# 		elif filter_ == 'callback_filters':
# 			try:
# 				if 'all' in callback_filters or any(str(cur_filter) in str(event.data) for cur_filter in callback_filters):
# 					continue
# 			except Exception:
# 				pass

# 		elif filter_ == 'content_types':
# 			if event_type in content_types:
# 				continue

# 		elif filter_ == 'equal':
# 			if await check_equal(event=event, event_type=event_type, equal=equal):
# 				continue

# 		elif filter_ == 'chat_types':
# 			if event_chat_type in chat_types:
# 				continue

# 		# Если хотя бы один фильтр не проходит, возвращаем False
# 		return False

# 	# Если все фильтры пройдены, возвращаем True
# 	return True



async def check_filters_equal(
	handler_filters_: Dict[str, bool],
	event: Any,
	event_commands: List[str],
	event_type: str,
	content_types: Set[str],
	lock_event_type: Set[str],
	equal: Any,
	commands: Set[str],
	callback_filters: List[Any],
	chat_types: Set[str],
	event_chat_type: str
) -> bool:
	# Определяем включенные фильтры
	enabled_filters = {key for key, value in handler_filters_.items() if value}

	# Определяем функции проверки для каждого фильтра
	async def check_commands() -> bool:
		return bool(set(commands).intersection(event_commands))

	async def check_lock_event_type() -> bool:
		return event_type in lock_event_type

	async def check_callback_filters() -> bool:
		try:
			return 'all' in callback_filters or any(
				str(cf) in str(event.data) for cf in callback_filters
			)
		except Exception:
			return False

	async def check_content_types() -> bool:
		return event_type in content_types

	async def check_equal() -> bool:
		return await check_equal(event=event, event_type=event_type, equal=equal)

	async def check_chat_types() -> bool:
		return event_chat_type in chat_types

	# Словарь проверок
	filter_checks: Dict[str, Callable[[], bool]] = {
		'commands': check_commands,
		'lock_event_type': check_lock_event_type,
		'callback_filters': check_callback_filters,
		'content_types': check_content_types,
		'equal': check_equal,
		'chat_types': check_chat_types
	}

	# Проверяем каждый включенный фильтр
	for filter_ in enabled_filters:
		if filter_ in filter_checks and not await filter_checks[filter_]():
			return False

	return True