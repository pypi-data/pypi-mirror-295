from ..Uni_cfg import asyncio, Namespace
from ..Datas import Data


class InputMessageContent():

	class InputTextMessageContent():

		def __init__(
			self,
			message_text: str,
			parse_mode: str = 'HTML',
			entities: dict = {},
			link_preview_options: dict = {}
		):

			builded_json = Data.rebuild_json_(locals())


			self.json_obj = builded_json
			self.message_text = message_text,
			self.parse_mode = parse_mode,
			self.entities = entities,
			self.link_preview_options = link_preview_options

			#return self