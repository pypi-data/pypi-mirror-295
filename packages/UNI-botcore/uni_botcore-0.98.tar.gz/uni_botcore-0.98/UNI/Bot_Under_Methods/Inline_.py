from ..Uni_cfg import asyncio, Namespace
from ..Sides import rest_side
from ..Datas import Data
from .Rest_Core import send_query

from ..Types.Keyboards_ import InlineKeyboardMarkup, InlineQueryResultsButton
from ..Types.Inline_Result import InlineQueryResult


class Inline_Methods():

	async def inline_answer(
		self,
		inline_query_id: str,
		results: InlineQueryResult = [],
		cache_time: int = 300,
		is_personal: bool = True,
		next_offset: str = '',
		button: InlineQueryResultsButton = {}
		):

		json_ = await Data.rebuild_json(locals())
		if results != []:

			rebuilded_results = []
			for i in results.result_:
				rebuilded_results.append(i.json_obj)

			json_['results'] = rebuilded_results
			

		print('----')
		print(f'BUILD MESSAGE: {json_}')

		return await send_query(bot_object=self, data=json_, method='answerInlineQuery')