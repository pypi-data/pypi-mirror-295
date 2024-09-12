from ..Uni_cfg import asyncio, Namespace
from .Custom_Event_Methods import Message_Event_Methods, Command_Event_Methods, Callback_Event_Methods, Inline_Event_Methods



# class Event_Core_Methods():

# 	def __init__(self, event, bot_object, **kwargs):
# 		self.__dict__['_fields'] = {}
# 		self.__dict__['event'] = event
# 		for key, value in kwargs.items():
# 			self._fields[key] = value

# 		self.bot_object=bot_object

# 	def __getattr__(self, attr):
# 		try:
# 			return self._fields[attr]
# 		except KeyError:
# 			return getattr(self.event, attr)

# 	def __setattr__(self, key, value):
# 		if key in ('event', '_fields'):
# 			self.__dict__[key] = value
# 		else:
# 			self._fields[key] = value

# 	def __delattr__(self, item):
# 		if item in self._fields:
# 			del self._fields[item]
# 		elif item in ('event', '_fields'):
# 			self.__dict__.pop(item, None)
# 		else:
# 			delattr(self.event, item)

# 	def __str__(self):
# 		fields = [(key, value) for key, value in self._fields.items()]
# 		fields_str = ', '.join([f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in fields])
# 		return f"{str(self.event)[:-1]}, {fields_str}" + '}'




class Messages_Event(Message_Event_Methods):
	def __init__(self, event, bot_object, **kwargs):
		self.__dict__['_fields'] = {}
		self.__dict__['event'] = event
		for key, value in kwargs.items():
			self._fields[key] = value

		self.bot_object=bot_object

	def __getattr__(self, attr):
		try:
			return self._fields[attr]
		except KeyError:
			return getattr(self.event, attr)

	def __setattr__(self, key, value):
		if key in ('event', '_fields'):
			self.__dict__[key] = value
		else:
			self._fields[key] = value

	def __delattr__(self, item):
		if item in self._fields:
			del self._fields[item]
		elif item in ('event', '_fields'):
			self.__dict__.pop(item, None)
		else:
			delattr(self.event, item)

	def __str__(self):
		fields = [(key, value) for key, value in self._fields.items()]
		fields_str = ', '.join([f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in fields])
		return f"{str(self.event)[:-1]}, {fields_str}" + '}'


class Commands_Event(Command_Event_Methods):
	def __init__(self, event, bot_object, **kwargs):
		self.__dict__['_fields'] = {}
		self.__dict__['event'] = event
		for key, value in kwargs.items():
			self._fields[key] = value

		self.bot_object=bot_object

	def __getattr__(self, attr):
		try:
			return self._fields[attr]
		except KeyError:
			return getattr(self.event, attr)

	def __setattr__(self, key, value):
		if key in ('event', '_fields'):
			self.__dict__[key] = value
		else:
			self._fields[key] = value

	def __delattr__(self, item):
		if item in self._fields:
			del self._fields[item]
		elif item in ('event', '_fields'):
			self.__dict__.pop(item, None)
		else:
			delattr(self.event, item)

	def __str__(self):
		fields = [(key, value) for key, value in self._fields.items()]
		fields_str = ', '.join([f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in fields])
		return f"{str(self.event)[:-1]}, {fields_str}" + '}'


class Callbacks_Event(Callback_Event_Methods):
	def __init__(self, event, bot_object, **kwargs):
		self.__dict__['_fields'] = {}
		self.__dict__['event'] = event
		for key, value in kwargs.items():
			self._fields[key] = value

		self.bot_object=bot_object

	def __getattr__(self, attr):
		try:
			return self._fields[attr]
		except KeyError:
			return getattr(self.event, attr)

	def __setattr__(self, key, value):
		if key in ('event', '_fields'):
			self.__dict__[key] = value
		else:
			self._fields[key] = value

	def __delattr__(self, item):
		if item in self._fields:
			del self._fields[item]
		elif item in ('event', '_fields'):
			self.__dict__.pop(item, None)
		else:
			delattr(self.event, item)

	def __str__(self):
		fields = [(key, value) for key, value in self._fields.items()]
		fields_str = ', '.join([f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in fields])
		return f"{str(self.event)[:-1]}, {fields_str}" + '}'


class Inlines_Event(Inline_Event_Methods):
	def __init__(self, event, bot_object, **kwargs):
		self.__dict__['_fields'] = {}
		self.__dict__['event'] = event
		for key, value in kwargs.items():
			self._fields[key] = value

		self.bot_object=bot_object

	def __getattr__(self, attr):
		try:
			return self._fields[attr]
		except KeyError:
			return getattr(self.event, attr)

	def __setattr__(self, key, value):
		if key in ('event', '_fields'):
			self.__dict__[key] = value
		else:
			self._fields[key] = value

	def __delattr__(self, item):
		if item in self._fields:
			del self._fields[item]
		elif item in ('event', '_fields'):
			self.__dict__.pop(item, None)
		else:
			delattr(self.event, item)

	def __str__(self):
		fields = [(key, value) for key, value in self._fields.items()]
		fields_str = ', '.join([f"'{key}': '{value}'" if isinstance(value, str) else f"'{key}': {value}" for key, value in fields])
		return f"{str(self.event)[:-1]}, {fields_str}" + '}'