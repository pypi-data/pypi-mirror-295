#from .uni_cfg import *
from ..Uni_cfg import asyncio, Namespace, textwrap, randint
from ..Datas.Data import get_namespace_of_path
from ..Types.Events_ import events_templates


async def get_keyboards(bot_object, user):
	import types 

	print(f'получаем клавиатуру')
	#print(bot_object.BAG)
	keybs = Namespace(**{name: getattr(bot_object.BAG.keyboards, name) for name in dir(bot_object.BAG.keyboards) if not name.startswith('__')})
	
	for name, method in vars(keybs).items():
		if callable(method):
			setattr(keybs, name, types.MethodType(method, user))

	return keybs


async def get_texts(bot_object, user):
	import types

	print(f'получаем тексты')
	text = Namespace(**{name: getattr(bot_object.BAG.texts, name) for name in dir(bot_object.BAG.texts) if not name.startswith('__')})
	
	for name, method in vars(text).items():
		if callable(method):
			setattr(text, name, types.MethodType(method, user))

	return text
	

async def _get_user(bot_object, *args, **kwargs):

	try:

		event = args[0]

		user = await bot_object.BAG.Custom_Packs.pack_user(event)
		return user, await get_keyboards(bot_object, user), await get_texts(bot_object, user)

	except Exception as e:
		traceback.print_exc()
		pass


async def _get_event_chat_type(event, event_type):#переписать на новый манер


	chat_type = 'none'
	chat_inst = None

	print(event_type)

	chat_path = events_templates[event_type]['chat_path']
	

	chat_inst = None
	if not '.' in chat_path:
		chat_inst = getattr(event, chat_path)
	else:
		chat_inst = event
		for i in str(chat_path).split('.'):
			chat_inst = getattr(chat_inst, i)



	chat_inst_dict_keys = {}
	try:
		chat_inst_dict_keys = vars(chat_inst)['_values'].keys()
	except Exception as e:
		chat_inst_dict_keys = vars(chat_inst).keys()

	if 'first_name' in chat_inst_dict_keys:
		chat_type = 'user_chat'

	elif 'title' in chat_inst_dict_keys:

		if 'username' in chat_inst_dict_keys:
			chat_type = 'public_chat'
		else:
			chat_type = 'private_chat'


	# print(f'CHAT TYPE: {chat_type}')
	# print(f'CHAT: {chat_inst}')
	# print('----')
	return chat_type