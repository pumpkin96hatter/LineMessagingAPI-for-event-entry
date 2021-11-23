import requests
import json
import traceback

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from django.views.decorators.csrf import csrf_exempt

import json
import re

from events.models import Event_Type, Entry, Application_Log, Application_Info


from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, PostbackAction
from linebot.exceptions import LineBotApiError

ACCESS_TOKEN = 'iXe8Mrhg4CsoWwiEoQHIhOhYIHebJ0VVVOMSGWYT5tS4R5iFofob0r0+njDR9ButbHKh++mV2xHsE6MACKg3TfovMbSmYTEndwZCLmgxVnj2ipWCbRS96xXYIGG7ed1waqeQDcqA1zxiYAaGIZWPhwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(ACCESS_TOKEN)

@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    sent_message = sent_json['events'][0]['message']['text']
    user_id = sent_json['events'][0]['source']['userId']
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
    user_name = json.loads(result.text)['displayName']
    reply_token = sent_json['events'][0]['replyToken']
    

    w = re.search('(参加|エントリー|完了|參加|報名|完成|確認)', sent_message)
    # if  w is not None:
    try:
        if w != None:
            if w.group() == 'エントリー' or w.group() == '報名':
                event_types = Event_Type.objects.all()
                columns = []
                for event_type in event_types:
                    actions = []
                    for entry in event_type.entry_set.all():
                        ma = MessageAction(
                            label = entry.name,
                            text = entry.name
                        )
                        actions.append(ma)
                    cm = CarouselColumn(
                            thumbnail_image_url='https://1.bp.blogspot.com/-quXPHEONkHA/Wj4ITFt6LYI/AAAAAAABJJg/5D37TjJ6rHsaIY9OxcIKiBI210A1Up50ACLcBGAs/s800/calender_man.png',
                            title=event_type.name,
                            text='description1',
                            actions=actions
                        )
                    columns.append(cm)
                
                message = TemplateSendMessage(
                    alt_text='Carousel template',
                    template=CarouselTemplate(
                        columns=columns
                    )
                )

            elif Entry.objects.filter(name = sent_message).first():
                entry = Entry.objects.filter(name=sent_message).first()
                application_info = Application_Info.objects.filter(participant=user_id, status=0).first()
                if not application_info:
                    application_info = Application_Info(participant=user_id)
                    application_info.save()
                application_log = Application_Log.objects.filter(application_info=application_info, entry=sent_message).first()
                if application_log:
                    application_log.amount = application_log.amount + 1
                else:
                    application_log = Application_Log(application_info=application_info, entry=entry, amount=1)
                application_log.save()
                    
                message = TextSendMessage(text='他にエントリーしたい交流会はありますか？複数ある場合は上記から追加で選択してください。\n無ければ「完了」と送信してください。') 
                
            elif Application_Info.objects.filter(participant=user_id, status=0).first()\
                and w.group() == '完了':
                application_info = Application_Info.objects.filter(participant=user_id, status=0).first()
                if not application_info:
                    # 新しいオーダーを作る
                    application_info = application_info(participant=user_id)
                    application_info.save()

                application_logs = application_info.application_log_set.all()
                message = TextSendMessage(text=f'{application_info.applied_at:%Y年%m月%d日 %H時%M分}にエントリーを受け付けました。\n\n{output_application_logs(application_logs)}\nエントリー済みの交流会日程を確認したい場合は「確認」と送信してください。')
                # 注文完了
                application_info.status = 1
                application_info.save()
                
            elif Application_Info.objects.filter(participant=user_id, status=1).first()\
                and w.group() == '確認':
                application_info = Application_Info.objects.filter(participant=user_id, status=1).all()
                application_log = Application_Log.objects.filter(application_info=application_info).all()
                application_logs = application_info.application_log_set.all()
                message = TextSendMessage(text=f'{user_name}さんのエントリー情報は以下の通りです。\n\n{output_application_log_confirmation(application_logs)}')

        else:

            message = TextSendMessage(text=f'{user_name}さん こんにちは。\n「エントリー」と送信すると、申し込みを開始できます。\n「日程表」と送信すると、スケジュールの確認が出来ます。')
    
    except Exception:
            message = TextSendMessage(text=f'{user_name}さん こんにちは。\n「エントリー」と送信すると、申し込みを開始できます。\n「日程表」と送信すると、スケジュールの確認が出来ます。')
    
            traceback.print_exc()
            
    line_bot_api.reply_message(reply_token, message)
    
    return HttpResponse('')

def output_application_logs(application_logs):
    result = ''
    for application_log in application_logs:
        result += f'{application_log.entry.name}\n' 
    return result

# def output_application_log_confirmation(output_application_log_confirmation):
#      result = ''
#      for application_log in application_logs:
#          result += f'{application_log.entry.name}\n' 
#      return result



urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', callback),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
