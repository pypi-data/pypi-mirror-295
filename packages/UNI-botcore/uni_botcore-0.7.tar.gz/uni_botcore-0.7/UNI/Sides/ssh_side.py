from ..Uni_cfg import aiohttp, asyncio, Namespace, time, httpx, traceback, urlparse, paramiko
from ..Uni_cfg import json as json_



async def send_ssh_query(hostname: str, username: str, password: str, command: str):

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=hostname, username=username, password=password)

	# Выполнение команды
	stdin, stdout, stderr = ssh.exec_command(command)

	# Чтение вывода из stdout
	output = stdout.read().decode('utf-8')

	# Вывод лога в консоль
	#print(output)

	# Закрытие соединения
	ssh.close()
	return output