import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

from qcloudsms_py import SmsMultiSender,SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from django.conf import settings


def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :parm phone_num: 手机号
    :parm template_id: 腾讯云短信模板ID
    :parm template_param_list: 短信模板所需参数列表,例如：【验证码: {1},描述: {2}】
    : return:
    """
    appid = settings.TENCENT_SMS_APP_ID
    appkey = settings.TENCENT_SMS_APP_KEY
    sms_sign = settings.TENCENT_SMS_SIGN
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result':1000,'errmsg': "网络异常发送失败"}
    return response

def send_sms_multi(phone_num_list,template_id,param_list):
    """
    批量发送短信
    :paramphone_num_list：手机号列表
    :paramtemplate_id：腾讯云短信模板ID
    :paramparam_List：短信模板所需参数列表，例如：【验证码：[1}，描述：{2)】，则传递参
    :return:
    """
    appid = settings.TENCENT_SMS_APP_ID
    appkey = settings.TENCENT_SMS_APP_KEY
    sms_sign = settings.TENCENT_SMS_SIGN
    sender = SmsMultiSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num_list, template_id, param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result':1000,'errmsg':"网络异常发送失败"}
    return response