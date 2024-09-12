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