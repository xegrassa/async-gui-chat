from enum import Enum


class Notification(Enum):
    NEW_MESSAGE_IN_CHAT = 0
    MESSAGE_SENT = 1
    AUTHORIZATION_DONE = 2
    PROMPT_BEFORE_AUTH = 3
