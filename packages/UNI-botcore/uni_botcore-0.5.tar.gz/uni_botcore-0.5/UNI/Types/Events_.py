

events_templates = {

	'command': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'commands',
		'gap': ['chat.last_name', 'from.last_name'],

		'enable_commands': True
	},


	'message': { 
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'event_choose_types': [
			["entities", 'command']
		],

		'enable_commands': False
	},

	'sticker': {
		'json_': {
			'update_id': 207890162, 
			'message': {
				'message_id': 272, 
				'from': {
					'id': 1939628022, 
					'is_bot': False, 
					'first_name': 'ηє', 
					'last_name': 'νєямσяє', 
					'username': 'beware_the_dead', 
					'language_code': 'ru', 
					'is_premium': True
				}, 
				'chat': {
					'id': 1939628022, 
					'first_name': 'ηє', 
					'last_name': 'νєямσяє', 
					'username': 'beware_the_dead', 
					'type': 'private'
				}, 
				'date': 1722060803, 
				'sticker': {
					'width': 512, 
					'height': 512, 
					'emoji': '🕺', 
					'set_name': 'memesbynorufx_by_fStikBot', 
					'is_animated': False, 
					'is_video': True, 
					'type': 'regular', 
					'thumbnail': {
						'file_id': 'AAMCAgADGQEAAgEQZqSQA6wdolsBHGEMOK8yTZGox7sAAsQnAAKiMYFLweLX5TpV8YgBAAdtAAM1BA', 
						'file_unique_id': 'AQADxCcAAqIxgUty', 
						'file_size': 4674, 
						'width': 320, 
						'height': 320}, 
						'thumb': {
							'file_id': 'AAMCAgADGQEAAgEQZqSQA6wdolsBHGEMOK8yTZGox7sAAsQnAAKiMYFLweLX5TpV8YgBAAdtAAM1BA', 
							'file_unique_id': 
							'AQADxCcAAqIxgUty', 
							'file_size': 4674, 
							'width': 320, 
							'height': 320
						}, 
					'file_id': 'CAACAgIAAxkBAAIBEGakkAOsHaJbARxhDDivMk2RqMe7AALEJwACojGBS8Hi1-U6VfGINQQ', 
					'file_unique_id': 'AgADxCcAAqIxgUs', 
					'file_size': 161487
				}
			}
		},
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],

		'enable_commands': False

	},

	'gif': {
		'json_': [
			{
			    "update_id": 207890171,
			    "message": {
			        "message_id": 281,
			        "from": {
			            "id": 1939628022,
			            "is_bot": False,
			            "first_name": "\u03b7\u0454",
			            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
			            "username": "beware_the_dead",
			            "language_code": "ru",
			            "is_premium": True
			        },
			        "chat": {
			            "id": 1939628022,
			            "first_name": "\u03b7\u0454",
			            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
			            "username": "beware_the_dead",
			            "type": "private"
			        },
			        "date": 1722061501,
			        "animation": {
			            "file_name": "lethal-company-boogie-down.mp4",
			            "mime_type": "video/mp4",
			            "duration": 4,
			            "width": 180,
			            "height": 320,
			            "file_id": "CgACAgQAAxkBAAIBGWakkr3aUTWsm9jiGEuitO8bn0ziAAJGBQAC0j40USTC-zcdclUkNQQ",
			            "file_unique_id": "AgADRgUAAtI-NFE",
			            "file_size": 233408
			        },
			        "document": {
			            "file_name": "lethal-company-boogie-down.mp4",
			            "mime_type": "video/mp4",
			            "file_id": "CgACAgQAAxkBAAIBGWakkr3aUTWsm9jiGEuitO8bn0ziAAJGBQAC0j40USTC-zcdclUkNQQ",
			            "file_unique_id": "AgADRgUAAtI-NFE",
			            "file_size": 233408
			        }
			    }
			},
			{
			    "update_id": 207890380,
			    "message": {
			        "message_id": 370,
			        "from": {
			            "id": 1939628022,
			            "is_bot": False,
			            "first_name": "\u03b7\u0454",
			            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
			            "username": "beware_the_dead",
			            "language_code": "ru",
			            "is_premium": True
			        },
			        "chat": {
			            "id": 1939628022,
			            "first_name": "\u03b7\u0454",
			            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
			            "username": "beware_the_dead",
			            "type": "private"
			        },
			        "date": 1722131003,
			        "animation": {
			            "file_name": "Untitled.gif.mp4",
			            "mime_type": "video/mp4",
			            "duration": 7,
			            "width": 320,
			            "height": 240,
			            "thumbnail": {
			                "file_id": "AAMCBAADGQEAAgFyZqWiOyTYCYrnG7NynVXCTSnRUeYAAlkKAAKoFSBQxtEAAaN9oqz1AQAHbQADNQQ",
			                "file_unique_id": "AQADWQoAAqgVIFBy",
			                "file_size": 11122,
			                "width": 320,
			                "height": 240
			            },
			            "thumb": {
			                "file_id": "AAMCBAADGQEAAgFyZqWiOyTYCYrnG7NynVXCTSnRUeYAAlkKAAKoFSBQxtEAAaN9oqz1AQAHbQADNQQ",
			                "file_unique_id": "AQADWQoAAqgVIFBy",
			                "file_size": 11122,
			                "width": 320,
			                "height": 240
			            },
			            "file_id": "CgACAgQAAxkBAAIBcmalojsk2AmK5xuzcp1Vwk0p0VHmAAJZCgACqBUgUMbRAAGjfaKs9TUE",
			            "file_unique_id": "AgADWQoAAqgVIFA",
			            "file_size": 29092
			        },
			        "document": {
			            "file_name": "Untitled.gif.mp4",
			            "mime_type": "video/mp4",
			            "thumbnail": {
			                "file_id": "AAMCBAADGQEAAgFyZqWiOyTYCYrnG7NynVXCTSnRUeYAAlkKAAKoFSBQxtEAAaN9oqz1AQAHbQADNQQ",
			                "file_unique_id": "AQADWQoAAqgVIFBy",
			                "file_size": 11122,
			                "width": 320,
			                "height": 240
			            },
			            "thumb": {
			                "file_id": "AAMCBAADGQEAAgFyZqWiOyTYCYrnG7NynVXCTSnRUeYAAlkKAAKoFSBQxtEAAaN9oqz1AQAHbQADNQQ",
			                "file_unique_id": "AQADWQoAAqgVIFBy",
			                "file_size": 11122,
			                "width": 320,
			                "height": 240
			            },
			            "file_id": "CgACAgQAAxkBAAIBcmalojsk2AmK5xuzcp1Vwk0p0VHmAAJZCgACqBUgUMbRAAGjfaKs9TUE",
			            "file_unique_id": "AgADWQoAAqgVIFA",
			            "file_size": 29092
			        }
			    }
			}
		],
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],

		'enable_commands': False
	},

	'photo': {
		'json_': {
		    "update_id": 207890173,
		    "message": {
		        "message_id": 283,
		        "from": {
		            "id": 1939628022,
		            "is_bot": False,
		            "first_name": "\u03b7\u0454",
		            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
		            "username": "beware_the_dead",
		            "language_code": "ru",
		            "is_premium": True
		        },
		        "chat": {
		            "id": 1939628022,
		            "first_name": "\u03b7\u0454",
		            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
		            "username": "beware_the_dead",
		            "type": "private"
		        },
		        "date": 1722061641,
		        "photo": [
		            {
		                "file_id": "AgACAgIAAxkBAAIBG2akk0nZ3OV1i2Yn_PqwERhFNncoAAJ02DEbMk8pSQJxVBBd1Z2vAQADAgADbQADNQQ",
		                "file_unique_id": "AQADdNgxGzJPKUly",
		                "file_size": 923,
		                "width": 32,
		                "height": 32
		            }
		        ]
		    }
		},
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],

		'enable_commands': False
	},

	'document': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'geo': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'contact': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'audio': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'voice': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'video_note': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'my_chat_member': {
		'chat_path': 'chat',
		'event_data_path': 'my_chat_member',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'chat_member': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'topic_created': {
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'reaction': {
		'chat_path': 'chat',
		'event_data_path': 'message_reaction',
		'quick_name': 'messages',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	# 'forward': {
		
	# 	'chat_path': 'chat',
	# 	'event_data_path': 'message',
	# 	'quick_name': 'messages',
	# 	'gap': [],

	# 	'enable_commands': False
	# },


	'callback': {
		'chat_path': 'message.chat',
		'event_data_path': 'callback_query',
		'quick_name': 'callbacks',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'inline': {
		'chat_path': 'from',
		'event_data_path': 'inline_query',
		'quick_name': 'inlines',
		'gap': [],
		'event_choose_types': [
		],

		'enable_commands': False
	},


	'via_bot': {
		'json_': {
		    "update_id": 207890568,
		    "message": {
		        "message_id": 444,
		        "from": {
		            "id": 1939628022,
		            "is_bot": False,
		            "first_name": "\u03b7\u0454",
		            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
		            "username": "beware_the_dead",
		            "language_code": "ru",
		            "is_premium": True
		        },
		        "chat": {
		            "id": 1939628022,
		            "first_name": "\u03b7\u0454",
		            "last_name": "\u03bd\u0454\u044f\u043c\u03c3\u044f\u0454",
		            "username": "beware_the_dead",
		            "type": "private"
		        },
		        "date": 1722253007,
		        "text": "message text",
		        "reply_markup": {
		            "inline_keyboard": [
		                [
		                    {
		                        "text": "test",
		                        "url": "https://t.me/dev_nevermore"
		                    }
		                ]
		            ]
		        },
		        "via_bot": {
		            "id": 6342840221,
		            "is_bot": True,
		            "first_name": "TESTBOT 2",
		            "username": "redzonetest2_bot"
		        }
		    }
		},
		'chat_path': 'chat',
		'event_data_path': 'message',
		'quick_name': 'messages',
		'gap': [],

		'enable_commands': False
	}
}