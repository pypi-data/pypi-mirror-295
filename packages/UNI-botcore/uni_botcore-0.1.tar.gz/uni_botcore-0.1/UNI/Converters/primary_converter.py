from ..Uni_cfg import asyncio, Namespace, traceback, time, UNI_Handlers, Optional, Callable, Dict
from ..Types import Events_
from ..Datas.Data import wrap_namespace, wrap_dict, replace_dict_keyname



# async def compare_json(template, check, gap, reverse_):
	
# 	template_keys = set(template.keys())
# 	check_keys = set(check.keys())

# 	#needs_ = len(check) + sum(len(value) for value in check.values() if isinstance(value, dict))
# 	#needs_ = []

# 	needs_ = set()
# 	try:
# 		for key1 in template.keys():
# 			needs_.add(key1)
# 			if isinstance(template[key1], dict):
# 				for key2 in template[key1].keys():
# 					if not f"{key1}.{key2}" in gap:
# 						needs_.add(f"{key1}.{key2}")
# 			#else:
# 				#needs_.add(key1)
# 	except Exception as e:
# 		traceback.print_exc()


# 	equals_ = set()
# 	try:
# 		for key1 in check.keys():
# 			equals_.add(key1)
# 			if isinstance(check[key1], dict):
# 				for key2 in check[key1].keys():
# 					if not f"{key1}.{key2}" in gap:
# 						equals_.add(f"{key1}.{key2}")
# 			#else:
# 				#equals_.add(key1)
# 	except Exception as e:
# 		traceback.print_exc()

	
# 	# for key, value in check.items():
# 	# 	print(key, value)
# 	# 	print('==============')
# 	# 	#needs_.append(key)
# 	# 	if type(value) == dict:
# 	# 		for key_, value_ in check[key].items():
# 	# 			print(key_, value_)
# 	# 			print('------')
# 	# 			needs_ += 1

# 	# 	print('+++++++++++++++++++++++++++++')

# 	# equals_ = len(template_keys.intersection(check_keys)) + sum(
# 	# 	len(set(check[key].keys()).intersection(template[key].keys()))
# 	# 	for key in check_keys if isinstance(check[key], dict) and key in template_keys
# 	# )

# 	# print('==============')
# 	# print(template)
# 	# print(check)
# 	# print(f'NEEDS: {needs_} | EQUALS: {equals_}')
# 	# print('==============')

# 	# if needs_ == equals_:
# 	# 	return True

# 	# if gap != []:
# 	# for i in gap:
# 	# 	if reverse_ == False:
# 	# 		if not i in equals_:
# 	# 			equals_.add(i)
# 	# 	else:
# 	# 		if not i in needs_:
# 	# 			needs_.add(i)

# 	print(f'=====================')
# 	print(f'NEEDS: {needs_}')
# 	print(f'EQUALS: {equals_}')
# 	print(f'+++++++++++++++++++++')

# 	# if prd == True:
# 	# 	if type_ == 'command':
# 	# 		print('****************')
# 	# 		print(type_)
# 	# 		print(template)
# 	# 		print(check)

# 	# 		print(f'NEEDS: {needs_}')
# 	# 		print(f'EQUALS: {equals_}')
# 	# 		print('****************')

# 	if needs_ == equals_:

# 		# print(f'=====================')
# 		# print(f'NEEDS: {needs_}')
# 		# print(f'EQUALS: {equals_}')
# 		# print(f'+++++++++++++++++++++')
# 		return True

# 	return False



# async def classificate_update_type(update: Namespace, full_info: bool = False, event_data_path: str = ''):

# 	try:

# 		check_js = await update.to_dict()
# 		keys_l = list(check_js.keys())
# 		pre_type_key = keys_l[1]
# 		pre_type_key = pre_type_key.replace('_query', '').replace('message_', '')
# 		type_key = pre_type_key

# 		predict_event = Events_.events_templates[pre_type_key]
# 		for i in predict_event['event_choose_types']:
# 			if i:
# 				if i[0] in list(check_js[pre_type_key].keys()):
# 					type_key = i[1]

# 		return type_key
		
# 	except Exception as e:
# 		traceback.print_exc() 
# 		#скорее всего такого ивента просто не существует
# 		pass

# 	return None






async def classificate_update_type(update: Namespace, full_info: bool = False, event_data_path: str = '') -> str | None:

	try:
		check_js = await update.to_dict()

		# Если pre_type_key всегда второй ключ, доступ можно сделать более прямым
		keys = list(check_js)
		pre_type_key = keys[1].replace('_query', '').replace('message_', '')

		predict_event = Events_.events_templates.get(pre_type_key)
		if predict_event:
			for key, value in predict_event.get('event_choose_types', []):
				if key in check_js.get(pre_type_key, {}):
					return value

		return pre_type_key

	except Exception as e:
		# Обрабатываем только ошибки, которые мы ожидаем (например, KeyError)
		traceback.print_exc() 

	return None



# async def classificate_update_type(update: Namespace, full_info: bool = False, event_data_path: str = '') -> Optional[str]:
# 	try:
# 		# Получаем все атрибуты из update, игнорируя встроенные
# 		attributes = dir(update)
# 		filtered_attributes = [attr for attr in attributes if not attr.startswith('__')]

# 		attributes_ = dir(update)
# 		filtered_attributes_ = [attr for attr in attributes_ if not attr.startswith('__')]
# 		primary_type = filtered_attributes_[2] if len(filtered_attributes_) > 2 else None

# 		# Если в update меньше двух атрибутов, возвращаем None
# 		if len(filtered_attributes) < 2:
# 			return None
		
# 		# Предполагаем, что pre_type_key - это второй атрибут
# 		pre_type_key = filtered_attributes[2].replace('_query', '').replace('message_', '')

# 		# Получаем значение по ключу
# 		if hasattr(update, pre_type_key):
# 			check_js = getattr(update, pre_type_key)
# 		else:
# 			return None, None

# 		# Предположим, что Events_.events_templates доступен в текущем контексте
# 		predict_event = Events_.events_templates.get(pre_type_key)
# 		if predict_event:
# 			for key, value in predict_event.get('event_choose_types', []):
# 				# Проверяем наличие ключа в check_js
# 				if hasattr(check_js, key):
# 					return value, primary_type

# 		#print(f'КЛАСИФИЦИРОВАЛИ АЙПДЕЙТ', pre_type_key, primary_type)
# 		return pre_type_key, primary_type

# 	except Exception as e:
# 		# Обрабатываем только ошибки, которые мы ожидаем (например, KeyError)
# 		traceback.print_exc() 

# 	return None, None



async def get_update_primary_type(update: Namespace):

	#print(vars(update))
	
	update = await wrap_namespace(update)
	#print(update)
	update_keys = list(vars(update).keys())
	return update_keys[1]


# async def get_update_primary_type(update: Namespace):
# 	# Получаем атрибуты объекта Namespace
# 	attributes = dir(update)
	
# 	# Фильтруем атрибуты, чтобы оставить только те, которые не начинаются с '__'
# 	filtered_attributes = [attr for attr in attributes if not attr.startswith('__')]
	
# 	# Возвращаем второй атрибут, если он существует
# 	print(filtered_attributes)
# 	return filtered_attributes[2] if len(filtered_attributes) > 2 else None


# async def process_update(update: Namespace, bot_object: Namespace):

# 	primary_type = await get_update_primary_type(update=update)
# 	final_update_type = await classificate_update_type(update=update)

# 	print(final_update_type)

# 	if final_update_type != None:

# 		update_quick_name = Events_.events_templates[final_update_type]['quick_name']
# 		event_data_path = Events_.events_templates[final_update_type]['event_data_path']

# 		if update_quick_name in UNI_Handlers.keys():
# 			for handler_ in UNI_Handlers[update_quick_name]:

# 				handler_link = handler_['handler_link']
# 				handler_args = handler_['handler_args']
# 				handler_simulator_link = handler_['simulate_handler_link']
# 				prepared_update = None

# 				try:
# 					prepared_update = getattr(update, primary_type)
# 				except Exception as e:
# 					update = await wrap_namespace(update)
# 					update_refreshed_dict = await replace_dict_keyname(d=update[primary_type], old_keyname='from', new_keyname='from_user')
# 					prepared_update = await wrap_dict(update_refreshed_dict)
				
# 				res = await handler_simulator_link(event=prepared_update, event_data_path=event_data_path, bot_object=bot_object, update_type_=final_update_type)
# 				if res == True:
# 					asyncio.create_task(handler_link(event=prepared_update, event_data_path=event_data_path, bot_object=bot_object, update_type_=final_update_type))
# 					return


# 		return False

# 	else:

# 		#тут вызывает ребут бота
# 		pass










async def process_update(update: Namespace, bot_object: Namespace):

	print(f'собираем типы: {time.time()}')
	# получение первичного типа апдейта и его класификация - это вообще не трогать
	primary_type, final_update_type = await asyncio.gather(
		get_update_primary_type(update=update),
		classificate_update_type(update=update)
	)

	if final_update_type is not None:

		
		event_template = Events_.events_templates[final_update_type]
		update_quick_name = event_template['quick_name']
		event_data_path = event_template['event_data_path']

		if update_quick_name in UNI_Handlers.keys():
			for handler_ in UNI_Handlers[update_quick_name]:

				handler_link = handler_['handler_link']
				handler_args = handler_['handler_args']
				handler_simulator_link = handler_['simulate_handler_link']


				print(f'обрабатываем перед симуляцией: {time.time()}')

				if hasattr(update, primary_type):
					prepared_update = getattr(update, primary_type)
				else:
					update = await wrap_namespace(update)
					update_refreshed_dict = await replace_dict_keyname(d=update[primary_type], old_keyname='from', new_keyname='from_user')
					prepared_update = await wrap_dict(update_refreshed_dict)


				print(f'симуляция: {time.time()}')
				res = await handler_simulator_link(
					event=prepared_update,
					event_data_path=event_data_path,
					bot_object=bot_object,
					update_type_=final_update_type
				)

				
				if res:

					print(f'вызов хендлера: {time.time()}')
					asyncio.create_task(
						handler_link(
							event=prepared_update,
							event_data_path=event_data_path,
							bot_object=bot_object,
							update_type_=final_update_type
						)
					)
					return

		return False

	else:
		# Вызов ребута бота
		pass



# async def process_update(update: Namespace, bot_object: Namespace):
# 	# получение первичного типа апдейта и его класификация
# 	# primary_type, final_update_type = await asyncio.gather(
# 	# 	get_update_primary_type(update=update),
# 	# 	classificate_update_type(update=update)
# 	# )

# 	final_update_type, primary_type = await classificate_update_type(update=update)

# 	if final_update_type is not None:
# 		event_template = Events_.events_templates[final_update_type]
# 		update_quick_name = event_template['quick_name']
# 		event_data_path = event_template['event_data_path']

# 		if update_quick_name in UNI_Handlers.keys():
# 			for handler_ in UNI_Handlers[update_quick_name]:
# 				handler_link: Callable = handler_['handler_link']
# 				handler_args = handler_['handler_args']
# 				handler_simulator_link: Callable = handler_['simulate_handler_link']

# 				# Получаем атрибут из update
# 				if hasattr(update, primary_type):
# 					prepared_update = getattr(update, primary_type)
# 				else:
# 					# Если атрибут отсутствует, создаем его из доступных атрибутов
# 					# Пример простой логики для объединения доступных атрибутов
# 					available_attributes = {attr: getattr(update, attr, None) for attr in dir(update) if not attr.startswith('__')}
					
# 					# Проверяем, можем ли мы создать необходимое представление
# 					# Зависит от того, как вам нужно обрабатывать данные
# 					# В примере просто возвращаем None, если нужный атрибут не найден
# 					if primary_type in available_attributes:
# 						prepared_update = available_attributes[primary_type]
# 					else:
# 						# Если нужно, вы можете создать специфическую логику преобразования данных здесь
# 						return False

# 				# Применяем функцию-симулятор
# 				res = await handler_simulator_link(
# 					event=prepared_update,
# 					event_data_path=event_data_path,
# 					bot_object=bot_object,
# 					update_type_=final_update_type
# 				)

# 				if res:
# 					# Создаем задачу для асинхронного вызова обработчика
# 					asyncio.create_task(
# 						handler_link(
# 							event=prepared_update,
# 							event_data_path=event_data_path,
# 							bot_object=bot_object,
# 							update_type_=final_update_type
# 						)
# 					)
# 					return

# 		return False

# 	else:
# 		# Вызов ребута бота
# 		pass