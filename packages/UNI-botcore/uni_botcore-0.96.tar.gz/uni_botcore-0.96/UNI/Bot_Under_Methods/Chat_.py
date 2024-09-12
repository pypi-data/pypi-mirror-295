from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query

from ..Types.Keyboards_ import InlineKeyboardMarkup



class Chat_Methods():

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))

	async def get_chat_member(
		self,
		chat_id: int,
		user_id: int
		):

		json_ = await Data.rebuild_json(locals())
			
		#print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='getChatMember')


	async def create_forum_topic(
		self,
		chat_id: int,
		name: str,
		icon_color: int = None,
		icon_custom_emoji_id: int = None
	):

		json_ = await Data.rebuild_json(locals())

		#print(f'BUILD MESSAGE: {json_}')
		return await send_query(bot_object=self, data=json_, method='createForumTopic')
		

	async def send_chat_action(
		self,
		chat_id: int,
		action: str, # typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
		business_connection_id: str = '',
		message_thread_id: int = 0
	):

		json_ = await Data.rebuild_json(locals())

		#print(f'BUILD MESSAGE: {json_}')
		return await send_query(bot_object=self, data=json_, method='sendChatAction')