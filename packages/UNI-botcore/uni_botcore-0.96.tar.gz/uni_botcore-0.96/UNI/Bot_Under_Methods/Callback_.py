from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query

from ..Types.Keyboards_ import InlineKeyboardMarkup



class Callback_Methods():

	async def callback_answer(
		self,
		callback_query_id: str,
		text: str = '',
		show_alert: bool = False,
		url: str = '',
		cache_time: int = 0
		):

		json_ = await Data.rebuild_json(locals())
			
		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='answerCallbackQuery')