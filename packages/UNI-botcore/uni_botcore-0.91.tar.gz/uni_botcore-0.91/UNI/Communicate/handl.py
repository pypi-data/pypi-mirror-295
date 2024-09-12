from ..Uni_cfg import UNI_Handlers, Namespace


def register_handler(handler: Namespace, handler_type: str, commands: list = [], args: dict = {}, handler_simulator: Namespace = None):

	global UNI_Handlers

	if not handler_type in UNI_Handlers.keys():
		UNI_Handlers[handler_type] = []

	UNI_Handlers[handler_type].append({'handler_link': handler, 'simulate_handler_link': handler_simulator, 'handler_args': args})
	print(UNI_Handlers)