#from .uni_cfg import *
from ..Uni_cfg import asyncio, Namespace




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


async def check_filters_equal(handler_filters_, event, event_commands, event_type, content_types, lock_event_type, equal, commands, callback_filters, chat_types, event_chat_type):

	cur_filters_enable = [i[0] for i in handler_filters_.items() if i[1] != None and i[1] != []]
	pre_done_filters = []

	#нужно просканить совпадения по фильтрам и если все правильно то пропустить ивент

	for filter_ in cur_filters_enable:

		if filter_ == 'commands':
			print(commands, event_commands)
			if len(list(set(commands).intersection(event_commands))) > 0:
				pre_done_filters.append(filter_)

		elif filter_ == 'lock_event_type':
			if event_type in lock_event_type:
				pre_done_filters.append(filter_)

		elif filter_ == 'callback_filters':
			#print(callback_filters, event.data)
			try:
				if callback_filters[0] != 'all':
					if len([1 for cur_filter in callback_filters if str(cur_filter) in str(event.data)]) > 0:
						pre_done_filters.append(filter_)
				else:
					pre_done_filters.append(filter_)
			except Exception as e:
				pass

		elif filter_ == 'content_types':
			print(f'КОНТЕНТ ТАЙП:', event_type, content_types)
			if event_type in content_types:
				pre_done_filters.append(filter_)

		elif filter_ == 'equal':
			if await check_equal(event=event, event_type=event_type, equal=equal) == True:
				pre_done_filters.append(filter_)

		elif filter_ == 'chat_types':
			print(event_chat_type, chat_types)
			if event_chat_type in chat_types:
				pre_done_filters.append(filter_)


	print(cur_filters_enable)
	print(pre_done_filters)

	done_filters = [i for i in pre_done_filters if i in cur_filters_enable]

	if len(list(set(done_filters).intersection(cur_filters_enable))) == len(cur_filters_enable):
		return True
	else:
		return False