from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.config import TG_ID_SUPPORT_CHAT


class ChatTypeFilter(BaseFilter):
	def __init__(self, chat_type: Union[str, list]):
		self.chat_type = chat_type

	async def __call__(self, message: Message) -> bool:
		if isinstance(self.chat_type, str):
			if self.chat_type == 'support':
				return message.chat.id == TG_ID_SUPPORT_CHAT

			return message.chat.type == self.chat_type
		else:
			return message.chat.type in self.chat_type
