from ..Uni_cfg import asyncio, Namespace
from .Custom_Entities_Methods import Chat_Methods
from ..Datas import Data



class Chat(Chat_Methods):

	def __init__(self, bot_object, id: int, data: Namespace):

		self.id = id
		self.bot_object=bot_object

		json_data_obj = Data.wrap_namespace_(data)

		for key, value in json_data_obj.items():
			setattr(self, key, value)
		print(f'CHAT OBJ: {json_data_obj}')

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))


class LinkPreviewOptions():

	def __init__(
		self,
		is_disabled: bool = True,
		url: str = '',
		prefer_small_media: bool = False,
		prefer_large_media: bool = False,
		show_above_text: bool  = False
	):

		cleaned_json = Data.rebuild_json_(locals())

		self.json_obj = cleaned_json
		self.is_disabled = is_disabled
		self.url = url
		self.prefer_small_media = prefer_small_media
		self.prefer_large_media = prefer_large_media
		self.show_above_text = show_above_text