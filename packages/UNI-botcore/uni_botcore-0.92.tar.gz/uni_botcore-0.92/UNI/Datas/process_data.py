from ..Uni_cfg import asyncio, Namespace, functools, textwrap


async def process_callback_data(callback_data: str) -> dict:

	result = {}
	if ':' in str(callback_data) and ';' in str(callback_data):

		try:
			for segment in callback_data.split('_')[1].split(';'):

				if ':' in segment:
					key, value = segment.split(':', 1)
					result[key.strip()] = value.strip()

		except Exception as e:
			pass

	return Namespace(**result)



def process_callback_data_decorator(handler):

	@wraps(handler)
	async def wrapper(call, *args, **kwargs):

		f_data = await process_callback_data(call.data)
		return await handler(call, f_data, *args, **kwargs)

	return wrapper


async def _process_callback_data_decorator(call):

	f_data = await process_callback_data(call.data)
	return f_data


def process_output(func): #декоратор на текста, чтоб врапались и были ровными
	@functools.wraps(func)
	async def wrapper(*args, **kwargs):
		result = await func(*args, **kwargs)
		return textwrap.dedent(result)

	return wrapper