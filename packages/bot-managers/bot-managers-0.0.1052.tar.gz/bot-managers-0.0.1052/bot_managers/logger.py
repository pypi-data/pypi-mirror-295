from tg_logger import BaseLogger


class ResponsibleLogger(BaseLogger):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = number
        self.thread_str = f'. Thread={self.number}'

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            return super().__getattr__(name)
        return lambda *args, **kwargs: self.log_message(
            name, *args, **kwargs, thread_str=self.thread_str
        )

    def create_telegram_client(self, log_level, tgbot):
        msg = f'Started client for bot id={tgbot.tgbot_id}' + self.thread_str
        self.log_message('get_or_create_bot_log', log_level, msg)

    def answer_chats(self, log_level, tgbot, chat_id):
        msg = (
            f'Bot id={tgbot.tgbot_id} started answering for chat={chat_id}'
            + self.thread_str
        )
        self.log_message('answer_chats', log_level, msg)

    def get_input_message_data(self, log_level):
        msg = 'Got the data for input message' + self.thread_str
        self.log_message('get_input_message_data', log_level, msg)

    def end_user_balance(self, log_level, user):
        msg = f'User id={user.tg_id} has zero balance' + self.thread_str
        self.log_message('get_or_create_bot_log', log_level, msg)

    def cancel_chat_task(self, log_level, tgbot_id, chat_id):
        msg = f'Cancel task: chatting_{tgbot_id}_{chat_id}' + self.thread_str
        self.log_message('cancel_chat_task', log_level, msg)

    def start_tasks(self, log_level):
        msg = 'Started asyncio tasks' + self.thread_str
        self.log_message('start_tasks', log_level, msg)