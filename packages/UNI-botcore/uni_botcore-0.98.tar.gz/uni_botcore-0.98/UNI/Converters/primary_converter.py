from ..Uni_cfg import asyncio, Namespace, traceback, time, UNI_Handlers
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



async def classificate_update_type(update: Namespace, full_info: bool = False, event_data_path: str = ''):

	try:

		check_js = await update.to_dict() #await wrap_namespace(update)
		keys_l = list(check_js.keys())
		pre_type_key = keys_l[1]
		pre_type_key = pre_type_key.replace('_query', '').replace('message_', '')
		type_key = pre_type_key

		predict_event = Events_.events_templates[pre_type_key]
		for i in predict_event['event_choose_types']:
			if i:
				if i[0] in list(check_js[pre_type_key].keys()):
					type_key = i[1]


		return type_key
		
	except Exception as e:
		traceback.print_exc() 
		#скорее всего такого ивента просто не существует
		pass

	return None



async def get_update_primary_type(update: Namespace):

	#print(vars(update))
	update = await wrap_namespace(update)
	print(update)
	update_keys = list(vars(update).keys())
	return update_keys[1]



async def process_update(update: Namespace, bot_object: Namespace):

	#asyncio.create_task(methods.save_req_(update))


	primary_type = await get_update_primary_type(update=update)
	final_update_type = await classificate_update_type(update=update)
	print(time.time())

	# print(primary_type)
	print(final_update_type)
	# print(UNI_Handlers.keys())

	if final_update_type != None:

		print(UNI_Handlers.keys(), final_update_type)
		update_quick_name = Events_.events_templates[final_update_type]['quick_name']
		event_data_path = Events_.events_templates[final_update_type]['event_data_path']

		if update_quick_name in UNI_Handlers.keys():
			#print('da')
			for handler_ in UNI_Handlers[update_quick_name]:

				handler_link = handler_['handler_link']
				handler_args = handler_['handler_args']
				handler_simulator_link = handler_['simulate_handler_link']
				prepared_update = None

				try:
					prepared_update = getattr(update, primary_type)
				except Exception as e:
					update = await wrap_namespace(update)
					update_refreshed_dict = await replace_dict_keyname(d=update[primary_type], old_keyname='from', new_keyname='from_user')
					prepared_update = await wrap_dict(update_refreshed_dict)

				res = await handler_simulator_link(event=prepared_update, event_data_path=event_data_path, bot_object=bot_object, update_type_=final_update_type)
				print(f'симуляция')
				if res == True:
					print(f'{final_update_type} handler called')
					asyncio.create_task(handler_link(event=prepared_update, event_data_path=event_data_path, bot_object=bot_object, update_type_=final_update_type))
					return


		# if 'events' in UNI_Handlers.keys():

		# 	for handler_ in UNI_Handlers['events']:

		# 		handler_link = handler_['handler_link']
		# 		handler_args = handler_['handler_args'],
		# 		handler_simulator_link = handler_['simulate_handler_link']
		# 		prepared_update = None

		# 		try:
		# 			# print('-----------')
		# 			# print(update)
		# 			# print(primary_type)
		# 			# print('-----------')
		# 			prepared_update = getattr(update, primary_type)
		# 		except Exception as e:
		# 			#traceback.print_exc()
		# 			try:
		# 				update_refreshed_dict = await replace_dict_keyname(d=update[primary_type], old_keyname='user', new_keyname='from_user')
		# 				prepared_update = await wrap_dict(update_refreshed_dict)
		# 			except Exception as e:
		# 				#traceback.print_exc()
		# 				try:
		# 					update_refreshed_dict = await replace_dict_keyname(d=update[primary_type], old_keyname='from', new_keyname='from_user')
		# 					prepared_update = await wrap_dict(update_refreshed_dict)
		# 				except Exception as e:
		# 					#traceback.print_exc()
		# 					pass


		# 		#print(prepared_update)
		# 		if prepared_update != None:
		# 			res = await handler_simulator_link(event=prepared_update, bot_object=bot_object)
		# 			if res == True:
		# 				print(f'{final_update_type} handler called')
		# 				asyncio.create_task(handler_link(event=prepared_update, bot_object=bot_object))
		# 				return

		return False

	else:

		#тут вызывает ребут бота
		pass