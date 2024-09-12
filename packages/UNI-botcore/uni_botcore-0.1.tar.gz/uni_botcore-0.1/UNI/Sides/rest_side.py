from ..Uni_cfg import aiohttp, asyncio, Namespace, time, httpx, traceback, urlparse
from ..Uni_cfg import json as json_


# Respone DataType
class Response(Namespace):
	async def update(self):
		
		path = getattr(Rest, self.type)
		return await path(url=self.url, headers=self.headers, data=self.data, json=self.json_data)


# Rest requests
class Rest():

	def __repr__(self):
		return str(vars(self))

	def __str__(self):
		return str(vars(self))

	async def __init__(self, response, text, json):
		self.response = response
		self.text = text
		self.json = json

	async def get(url: str, headers: dict = None, data: dict = None, json: dict = None):

		response_status = None
		response_text = None
		response_json = None

		# async with aiohttp.ClientSession(headers=headers) as session:
		# 	response = await session.get(url=url, json=json, data=data)

		# 	response_status = response.status

		# 	try:
		# 		response_text = await response.text(encoding='UTF-8')
		# 		response_json = await response.json()
		# 	except Exception as e:
		# 		#traceback.print_exc()
		# 		pass

		async with httpx.AsyncClient(headers=headers) as client:
			response = await client.get(url, params=json if json else data)
			
			response_status = int(response.status_code)

			try:
				response_text = None#response.text
				response_json = response.json()
			except Exception as e:
				traceback.print_exc()
				pass

		return Response(type='get', url=url, headers=headers, json_data=json, data=data, status=response_status, text=response_text, json=response_json)


	async def post(url: str, headers: dict = {}, data: dict = None, json: dict = None):

		response_status = None
		response_text = None
		response_json = None
		#connector = aiohttp.TCPConnector(limit=100)

		#print(f'открываем сессию на запрос: {time.time()}')

		# async with aiohttp.ClientSession(headers=headers, connector=connector) as session:

		# 	#print(f'отправляем запрос: {time.time()}')
		# 	if data != None:
		# 		response = await session.post(url=url, json=json, data=data, ssl=False, compress=True)
		# 	else:
		# 		response = await session.post(url=url, json=json, ssl=False, compress=True)

		# 	response_status = response.status

		# 	#print(f'обрабатываем ответ с запроса: {time.time()}')
		# 	try:
		# 		response_text = await response.text(encoding='UTF-8')
		# 		response_json = await response.json()
		# 	except Exception as e:
		# 		#traceback.print_exc()
		# 		pass





		# print(f'обрабатываем и направляем запрос с рестсайда: {time.time()}')

		# async with httpx.AsyncClient(headers=headers) as client:
		# 	response = await client.post(url=url, json=json, data=data)
			
		# 	response_status = int(response.status_code)

		# 	try:
		# 		response_text = None#response.text
		# 		response_json = response.json()
		# 	except Exception as e:
		# 		traceback.print_exc()
		# 		pass

		# print(f'отдаем ответ с рестсайда: {time.time()}')



		# print(f'обрабатываем и направляем запрос с рестсайда: {time.time()}')
		# parsed_url = urlparse(url)
		# host = parsed_url.hostname
		# port = parsed_url.port or 443  # HTTPS по умолчанию
		# path = parsed_url.path or '/'
		
		# reader, writer = await asyncio.open_connection(host, port, ssl=True)

		# # Формируем тело запроса
		# body = json if json else data
		# if body:
		# 	body = body if isinstance(body, str) else json_.dumps(body)
		# else:
		# 	body = ""

		# # Формируем заголовки
		# request_line = f"POST {path} HTTP/1.1\r\n"
		# headers_lines = (
		# 	f"Host: {host}\r\n"
		# 	"Content-Type: application/json\r\n"
		# 	f"Content-Length: {len(body)}\r\n"
		# 	"Connection: close\r\n"  # Закрыть соединение после завершения запроса
		# 	"\r\n"
		# )

		# # Полный HTTP-запрос
		# request = request_line + headers_lines + body

		# print(request)  # Отладочная информация

		# # Отправка запроса
		# writer.write(request.encode())
		# await writer.drain()

		# # Чтение ответа
		# response = await reader.read()
		# writer.close()
		# await writer.wait_closed()

		# # Обработка ответа
		# response_status = response.split(b'\r\n')[0].decode().split(' ')[1]
		# response_json = json_.loads(response.split(b'\r\n\r\n', 1)[1].decode())

		# print("Response status:", response_status)
		# print("Response body:", response_json)

		# print(f'отдаем ответ с рестсайда: {time.time()}')








		#print(f'обрабатываем и направляем запрос с рестсайда: {time.time()}')
		parsed_url = urlparse(url)
		host = parsed_url.hostname
		port = parsed_url.port or 443  # HTTPS по умолчанию
		path = parsed_url.path or '/'
		
		reader, writer = await asyncio.open_connection(host, port, ssl=True)

		# Формируем тело запроса
		if json is not None:
			body = json_.dumps(json)
		else:
			body = data or ""

		# Формируем заголовки
		headers_lines = (
			f"Host: {host}\r\n"
			"Content-Type: application/json\r\n"
			f"Content-Length: {len(body)}\r\n"
			"Connection: close\r\n"
			"\r\n"
		)

		# Полный HTTP-запрос
		request = f"POST {path} HTTP/1.1\r\n{headers_lines}{body}"

		#print(request)  # Отладочная информация

		# Отправка запроса
		writer.write(request.encode())
		await writer.drain()

		# Чтение ответа
		response = await reader.read()
		writer.close()
		await writer.wait_closed()

		# Обработка ответа
		header_end = response.find(b'\r\n\r\n')
		if header_end == -1:
			raise ValueError("Invalid response format")
		
		headers = response[:header_end].decode()
		body = response[header_end+4:]

		response_status = headers.split('\r\n')[0].split(' ')[1]
		response_json = json_.loads(body.decode())

		#print("Response status:", response_status)
		#print("Response body:", response_json)

		#print(f'отдаем ответ с рестсайда: {time.time()}')

		return Response(type='post', url=url, headers=headers, json_data=json, data=data, status=response_status, text=response_text, json=response_json)