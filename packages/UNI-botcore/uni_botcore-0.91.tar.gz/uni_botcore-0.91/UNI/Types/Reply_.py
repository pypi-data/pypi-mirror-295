from ..Uni_cfg import asyncio, Namespace
from ..Datas import Data


class ReplyParameters():

	def __init__(
		self,
		message_id: int,
		chat_id: int,
		allow_sending_without_reply: bool = False,
		quote: str = '',
		quote_parse_mode: str = '',
		quote_entities: list = [],
		quote_position: int = 0
	):

		builded_json = Data.rebuild_json_(locals())

		self.json_obj = builded_json
		self.message_id = message_id
		self.chat_id = chat_id
		self.allow_sending_without_reply = allow_sending_without_reply
		self.quote = quote
		self.quote_parse_mode = quote_parse_mode
		self.quote_entities = quote_entities
		self.quote_position = quote_position