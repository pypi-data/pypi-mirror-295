#from .uni_cfg import *
from ..Uni_cfg import asyncio, Namespace, textwrap, randint, time
from ..Datas.Data import get_namespace_of_path
from ..Types.Events_ import events_templates
import types 

# async def get_keyboards(bot_object, user):
	

# 	#print(f'получаем клавиатуру : {time.time()}')
# 	#print(bot_object.BAG)
# 	keybs = Namespace(**{name: getattr(bot_object.BAG.keyboards, name) for name in dir(bot_object.BAG.keyboards) if not name.startswith('__')})
	
# 	for name, method in vars(keybs).items():
# 		if callable(method):
# 			setattr(keybs, name, types.MethodType(method, user))
# 	#print(f'собрали клавиатуру : {time.time()}')
# 	return keybs


# async def get_texts(bot_object, user):
# 	#import types

# 	#print(f'получаем тексты : {time.time()}')
# 	text = Namespace(**{name: getattr(bot_object.BAG.texts, name) for name in dir(bot_object.BAG.texts) if not name.startswith('__')})
	
# 	for name, method in vars(text).items():
# 		if callable(method):
# 			setattr(text, name, types.MethodType(method, user))
# 	#print(f'собрали тексты : {time.time()}')
# 	return text






# async def get_keyboards(bot_object, user):

# 	if not isinstance(bot_object.BAG.keyboards, Namespace):

# 		keyboards = {
# 			name: getattr(bot_object.BAG.keyboards, name)
# 			for name in dir(bot_object.BAG.keyboards) 
# 			if not name.startswith('__')
# 		}
		
# 		keybs = Namespace(**keyboards)

# 		for name, method in keyboards.items():
# 			if callable(method):
# 				setattr(keybs, name, types.MethodType(method, user))

# 		bot_object.BAG.keyboards = keybs

# 	else:
# 		keybs = bot_object.BAG.keyboards

# 	return keybs


# async def get_texts(bot_object, user):

# 	if not isinstance(bot_object.BAG.texts, Namespace):
# 		texts = {
# 			name: getattr(bot_object.BAG.texts, name)
# 			for name in dir(bot_object.BAG.texts)
# 			if not name.startswith('__')
# 		}

# 		text = Namespace(**texts)

# 		for name, method in texts.items():
# 			if callable(method):
# 				setattr(text, name, types.MethodType(method, user))

# 		bot_object.BAG.texts = text

# 	else:
# 		text = bot_object.BAG.texts

# 	return text
	




def initialize_namespace(obj, user):
    items = {
        name: getattr(obj, name)
        for name in dir(obj)
        if not name.startswith('__')
    }

    namespace = Namespace(**items)

    for name, method in items.items():
        if callable(method):
            setattr(namespace, name, types.MethodType(method, user))

    return namespace

async def get_keyboards(bot_object, user):
	if not isinstance(bot_object.BAG.keyboards, Namespace):
		bot_object.BAG.keyboards = initialize_namespace(bot_object.BAG.keyboards, user)
	return bot_object.BAG.keyboards

async def get_texts(bot_object, user):
	if not isinstance(bot_object.BAG.texts, Namespace):
		bot_object.BAG.texts = initialize_namespace(bot_object.BAG.texts, user)
	return bot_object.BAG.texts



async def _get_user(bot_object, *args, **kwargs):
	try:
		event = args[0]

		# Параллельное выполнение асинхронных функций
		user = await bot_object.BAG.Custom_Packs.pack_user(event)
		keyboards_task = None
		texts_task = None

		if not isinstance(bot_object.BAG.keyboards, Namespace):
			keyboards_task = get_keyboards(bot_object, user)
		if not isinstance(bot_object.BAG.texts, Namespace):
			texts_task = get_texts(bot_object, user)
		
		# Ожидание завершения всех задач
		if keyboards_task != None and texts_task != None:
			keyboards, texts = await asyncio.gather(keyboards_task, texts_task)
		else:
			keyboards, texts = bot_object.BAG.keyboards, bot_object.BAG.texts

		return user, keyboards, texts

	except Exception as e:
		# Логирование ошибки и возврат None в случае ошибки
		traceback.print_exc()
		return None, None, None



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


	#print(f'CHAT TYPE: {chat_type}')
	#print(f'CHAT: {chat_inst}')
	# print('----')
	return chat_type

# async def _get_event_chat_type(event, event_type):
# 	chat_type = 'none'

# 	chat_path = events_templates[event_type]['chat_path']

# 	# Получаем chat_inst, перебирая вложенные атрибуты, если они существуют
# 	chat_inst = event
# 	for attr in chat_path.split('.'):
# 		chat_inst = getattr(chat_inst, attr, None)
# 		if chat_inst is None:
# 			break

# 	if not chat_inst:
# 		return chat_type  # Если chat_inst не найден, возвращаем 'none'

# 	# Определяем тип чата по наличию ключей
# 	chat_inst_dict_keys = vars(chat_inst).get('_values', vars(chat_inst)).keys()

# 	if 'first_name' in chat_inst_dict_keys:
# 		chat_type = 'user_chat'
# 	elif 'title' in chat_inst_dict_keys:
# 		chat_type = 'public_chat' if 'username' in chat_inst_dict_keys else 'private_chat'

# 	return chat_type
