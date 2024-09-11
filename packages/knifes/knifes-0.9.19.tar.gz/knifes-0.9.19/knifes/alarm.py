from knifes import times
from django.conf import settings
import httpx
import threading
import logging
logger = logging.getLogger(__name__)


# 异步发送报警
def async_send_msg(msg):
    threading.Thread(target=send_feishu_msg(msg)).start()


def send_feishu_msg(msg):
    data = {
        'msg_type': 'text',
        'content': {
            'text': f'{msg} [{times.strftime()}]'
        }
    }
    try:
        httpx.post(settings.FEISHU_ALARM_API, json=data, verify=False)
    except: # noqa
        logger.exception(f'推送报警信息失败:{msg}')

