import requests
import json
import traceback

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

import json
import re

from events.models import Event_Type, Entry, Application_Info, Participant, Line_Name, Schedule


from linebot import LineBotApi
from linebot.models import TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, PostbackAction, ImageSendMessage
from linebot.exceptions import LineBotApiError

ACCESS_TOKEN = 'iXe8Mrhg4CsoWwiEoQHIhOhYIHebJ0VVVOMSGWYT5tS4R5iFofob0r0+njDR9ButbHKh++mV2xHsE6MACKg3TfovMbSmYTEndwZCLmgxVnj2ipWCbRS96xXYIGG7ed1waqeQDcqA1zxiYAaGIZWPhwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(ACCESS_TOKEN)

@csrf_exempt
def callback(request):
    sent_json = json.loads(request.body)
    try:
        sent_message = sent_json['events'][0]['message']['text']
    except KeyError:
        sent_message = "参加意思表明"
    
    try:
        pb_data = sent_json['events'][0]['postback']['data']
    except KeyError:
        pb_data = None
    
    
    user_id = sent_json['events'][0]['source']['userId']
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
    user_name = json.loads(result.text)['displayName']
    reply_token = sent_json['events'][0]['replyToken']
    
    w = re.search('(日程表|参加意思表明|エントリー|完了|考え中です|確認|キャンセル)', sent_message)
    # wは送ってきたメッセージ内の単語
    # y = re.search('(参加します|pb_process)', w.group())
    # yは参加しますは入っていますか
    try:
        if w != None:
            if w.group() == 'エントリー':
                # 中国語ver or w.group() == '報名':
                event_types = Event_Type.objects.all()
                entries = Entry.objects.all()
                columns = []
                for event_type in event_types:
                    actions = []
                    # for entry in entries:
                    pob = PostbackAction(
                        type="postback",
                        label="参加します",
                        display_text=f'{event_type.event_date:%m月%d日}{event_type.type_name}(台湾時間):参加します',
                        data=f'{event_type.event_date}'
                    )
                    actions.append(pob)

                    ma = MessageAction(
                        type="message",
                        label='考え中です',
                        text='考え中です',
                    )
                    actions.append(ma)
                    
                    cm = CarouselColumn(
                            thumbnail_image_url=f'{event_type.pic_url}',
                            title=event_type.type_name,
                            text=f'{event_type.event_date:%Y年%m月%d日 %H時%M分}(台湾時間)',
                            actions=actions
                        )
                    columns.append(cm)
                
                message = TemplateSendMessage(
                    alt_text='申し訳ありません、このLINEbotはPC未対応です。スマホアプリ版からご確認ください。\n何らかの理由でスマホ対応不可の場合は、運営LINEアカウント(手動)に直接ご相談ください。',
                    template=CarouselTemplate(
                        columns=columns
                    )
                )
                # pback_data = sent_json['events'][0]['postback']['data']
                
#               y = re.search('参加します', sent_message)
#               x = re.search(f'{event_types}', sent_message)
            elif w.group() == '参加意思表明':
                event_type = Event_Type.objects.filter(event_date=pb_data).first()
                entry = Entry.objects.filter(name= '参加します' ).first()
                if event_type:
                    participant = Participant.objects.filter(participant=user_id).first()
                    if not participant:
                        participant = Participant(participant=user_id)
                    participant.save()
                    application_info = Application_Info.objects.filter(Q(participant=participant), Q(event_type=event_type), Q(entry=entry), Q(status=0)|Q(participant=participant), Q(event_type=event_type), Q(entry=entry), Q(status=1)).first()
                    if not application_info:
                        application_info = Application_Info(participant=participant, event_type=event_type, entry=entry, status=0)
                        application_info.save()
                    application_info = Application_Info.objects.filter(participant=participant, event_type=event_type, entry=entry, status=1).first()
                    if application_info:
                        message = TextSendMessage(text=f'{event_type}はエントリー済みです')
                        line_bot_api.reply_message(reply_token, message)
                participant = Participant.objects.filter(participant=user_id).first()
                line_name = Line_Name.objects.filter(line_name=user_name, participant=participant).first()
                if not line_name:
                    line_name = Line_Name(line_name=user_name, participant=participant)
                    line_name.save()    
                message = TextSendMessage(text='他にエントリーしたい交流会はありますか？複数ある場合は上記から追加で選択してください。\n無ければ「完了」と送信してください。\n完了前に選択をキャンセルしたい場合は「キャンセル」と送信してください。')         
                        # 予約キャンセル作る時用
                        # application_log = application_log = Application_Log.objects.filter(event_type__type_name=event_type, entry__name=entry, application_info=application_info).first()
                        # if application_log:
                        #     application_log = Application_Log.objects.filter(event_type__type_name=event_type, entry__name=entry, application_info=application_info).first()
                        #     # amountに関していじる場合はここを追加　amount = 1
                        # else:
                        #     application_log = Application_Log(event_type__type_name=event_type, entry=entry, application_info=application_info).first()
                        # application_log.save()
            elif w.group() == '考え中です':

                message = TextSendMessage(text='他にエントリーしたい交流会はありますか？複数ある場合は上記から追加で選択してください。\n無ければ「完了」と送信してください。\n完了前に選択をキャンセルしたい場合は「キャンセル」と送信してください。') 


            elif w.group() == 'キャンセル':
                line_name = Line_Name.objects.filter(line_name=user_name).first()
                if Participant.objects.filter(participant=user_id, line_name=line_name).first():
                    participant = Participant.objects.filter(participant=user_id, line_name=line_name).first()
                    application_infos = Application_Info.objects.filter(participant=participant, status=0).all()
                    if application_infos:
                        for application_info in application_infos:
                            application_info.status = 2
                        application_info.save()
                message = TextSendMessage(text='申請の処理は途中でキャンセルされました。エントリーを希望される場合は、再度「エントリー」と送信してください。')
                

            elif w.group() == '完了':
                line_name = Line_Name.objects.filter(line_name=user_name).first()
                participant = Participant.objects.filter(participant=user_id, line_name=line_name).first()
                if Application_Info.objects.filter(participant=participant, status=0).first():
                    application_infos = Application_Info.objects.filter(participant=participant, status=0).all()
                    message = TextSendMessage(text=f'{user_name}さんのエントリーを受け付けました。\n\n{output_application_infos(application_infos)}\n※注意：台湾時間(日本-1)です\nエントリー済みの交流会日程を確認したい場合は「確認」と送信してください。\nエントリー完了後のキャンセルのお問い合わせは運営LINEまで別途お問い合わせ下さい。')
                    for application_info in application_infos:
                        application_info.status = 1
                        application_info.save()
                else:                    
                    message = TextSendMessage(text='エントリー申請完了時に新しい希望選択の記録が確認されませんでした。エントリーを希望される場合は、再度「エントリー」と送信し、やり直してください。')

                
            elif w.group() == '確認':
                participant = Participant.objects.filter(participant=user_id).first()
                if Application_Info.objects.filter(participant=participant, status=1).first():
                    application_infos = Application_Info.objects.filter(participant=participant, status=1).all()
                    message = TextSendMessage(text=f'{user_name}さんのエントリー情報は以下の通りです。\n\n{output_application_infos(application_infos)}\n※注意：台湾時間(日本-1)です\nキャンセルのお問い合わせは運営LINEまで別途お問い合わせ下さい。')
                else:
                    message = TextSendMessage(text=f'{user_name}さんが現在エントリーしている交流会はありません。\n興味のある交流会があれば、「エントリー」と送信して交流会にエントリーしましょう。')
                    
            elif w.group() == '日程表':
                message = TextSendMessage(text='今月の日程表はこちらです')
                schedule_pic= Schedule.objects.filter().first()
                image_message = ImageSendMessage(
                    original_content_url=f'{schedule_pic.schedule_url}', 
                    preview_image_url=f'{schedule_pic.schedule_url}'
                )
                line_bot_api.reply_message(reply_token, [message, image_message])

        else:

            message = TextSendMessage(text=f'{user_name}さん こんにちは。\n「エントリー」と送信すると、希望の交流会に申し込みを開始できます。\n「日程表」と送信すると、スケジュールの確認が出来ます。')
    
    except Exception:
            message = TextSendMessage(text=f'{user_name}さん こんにちは。\n「エントリー」と送信すると、希望の交流会に申し込みを開始できます。\n「日程表」と送信すると、スケジュールの確認が出来ます。')
    
            traceback.print_exc()
            
    line_bot_api.reply_message(reply_token, message)
        
    return HttpResponse('')


def output_application_infos(application_infos):
    result = ''
    for application_info in application_infos:
        result += ' 'f'{application_info.event_type.type_name}{application_info.event_type.event_date:%m月%d日%H時%M分}～\n''  :'f'{application_info.entry.name}\n' 
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
