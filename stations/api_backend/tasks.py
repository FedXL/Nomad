from celery import shared_task, chain, signature

from api_backend.handlers.crm_handlers.client_handler import create_user
from crm.tasks import parse_file, my_task_logger, add_exists_clients, add_exist_client


@shared_task
def create_user_in_crm(phone_number, username):
    result = create_user(phone_number, username)
    if result:
        data = {'list': [result.get('client')]}
        group_chain = chain(
            parse_file.s(data),  # Возвращает какой-то результат
            signature("crm.tasks.add_exist_client", kwargs={"phone": phone_number})  # Передаём phone через kwargs
        )
        group_chain.apply_async()
    return 'completed'