from ..Uni_cfg import asyncio, Namespace, json, Decimal, inspect


async def wrap_dict(d):

	d = dict(d)
	for k, v in d.items():
		if isinstance(v, str):
			try:
				json_data = json.loads(v)
				if isinstance(json_data, dict):
					d[k] = await wrap_dict(json_data)
			except json.JSONDecodeError:
				pass
		elif isinstance(v, list):
			d[k] = [await wrap_dict(item) if isinstance(item, dict) else item for item in v]
		elif isinstance(v, dict):
			d[k] = await wrap_dict(v)
	return Namespace(**d)


def wrap_dict_(d):

	d = dict(d)
	for k, v in d.items():
		if isinstance(v, str):
			try:
				json_data = json.loads(v)
				if isinstance(json_data, dict):
					d[k] = wrap_dict_(json_data)
			except json.JSONDecodeError:
				pass
		elif isinstance(v, list):
			d[k] = [wrap_dict_(item) if isinstance(item, dict) else item for item in v]
		elif isinstance(v, dict):
			d[k] = wrap_dict_(v)
	return Namespace(**d)




async def wrap_namespace(namespace):
    if isinstance(namespace, Namespace):
        # Преобразовать атрибуты Namespace в словарь
        result = {}
        for key, value in namespace.__dict__.items():
            if isinstance(value, Namespace):
                # Если значение является также Namespace, рекурсивно вызвать функцию
                result[key] = await wrap_namespace(value)
            elif isinstance(value, list):
                # Обработка списков
                result[key] = [await wrap_namespace(item) for item in value]
            else:
                result[key] = value
        return result
    else:
        return namespace


def wrap_namespace_(namespace):
    if isinstance(namespace, Namespace):
        # Преобразовать атрибуты Namespace в словарь
        result = {}
        for key, value in namespace.__dict__.items():
            if isinstance(value, Namespace):
                # Если значение является также Namespace, рекурсивно вызвать функцию
                result[key] = wrap_namespace_(value)
            elif isinstance(value, list):
                # Обработка списков
                result[key] = [wrap_namespace_(item) for item in value]
            else:
                result[key] = value
        return result
    else:
        return namespace




async def replace_dict_keyname(d, old_keyname, new_keyname):
	#print(d)
	if old_keyname in d:
		d[new_keyname] = d.pop(old_keyname)
		for key, value in d.items():
			if isinstance(value, dict):
				await replace_dict_keyname(value, old_keyname, new_keyname)
			elif isinstance(value, list):
				for item in value:
					if isinstance(item, dict):
						await replace_dict_keyname(item, old_keyname, new_keyname)
	return d


async def get_namespace_of_path(ns, path):

	final_resp = None
	if '.' in path:
		components = str(path).split('.')
		final_resp = ns
		for c in components:
			final_resp = getattr(final_resp, c)
	else:
		final_resp = getattr(ns, path)

	return final_resp



async def rebuild_json(loc: Namespace = None):

	del loc['self']
	loc = {k: v for k, v in loc.items() if v not in [None, '', {}, [], (), 0]}
	return loc

def rebuild_json_(loc: Namespace = None):

	del loc['self']
	loc = {k: v for k, v in loc.items() if v not in [None, '', {}, [], (), 0]}
	return loc



class CustomNamespace():

	def __init__(self, data):
		self._set_attributes(data)
		self.dataspace = data

		if isinstance(self.dataspace, dict):
			self.dataspace = wrap_dict_(self.dataspace)

	def _set_attributes(self, data, prefix=""):
		if isinstance(data, dict):
			for key, value in data.items():
				attribute_name = prefix + key if prefix else key
				if isinstance(value, dict):
					setattr(self, attribute_name, CustomNamespace(value))  # Создаем вложенный объект
				elif isinstance(value, list):
					setattr(self, attribute_name, [CustomNamespace(item) if isinstance(item, dict) else item for item in value])
				else:
					setattr(self, attribute_name, value)


	async def to_dict(self):
		return await wrap_namespace(self.dataspace)

	def to_dict_(self):
		return wrap_namespace_(self.dataspace)