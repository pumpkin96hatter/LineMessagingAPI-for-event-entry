line-messaging-api-django-for-application

こちらは1～200人以下程度のイベント参加申請を受け付けるline masseging apiです。
無料でシンプル、コードを一切書かない人でも管理できる、繰り返し使うことを意図しました。
サークル活動や定期小規模イベントを行う方におすすめです。

>以下私のようなマジ初学者向け
django adminにメンバーを追加することで、詳しくない人でも気軽に複数人で追加・編集・管理することができます。
ただし集計や記録に関してはエクスポートでcsvファイルを別途処理するようになっています。
excelやスプシで簡単に集計できるようにマクロ組む必要あり。
カルーセル上の内部で使う画像等は適当なあぷろだを利用して、admin内のイベントタイプのurlにコピペすればokです。(googleドライブ不可)

＞初心者が手探りで0から書いたので汚いですが、公式含め情報がflaskばっかなので公開してます。
蛇足ですが、cmd操作で一斉送信(ブロードキャストメッセージ)したい場合は以下でたたきます。"をポップアウトさせるのとか改行とか面倒だったのでコピペ用貼って置きます
これは画像用なのでまぁLINEでべろっぱーずでjsonの情報見ながらメッセージタイプなどは変更してください。無料版なのでメッセージ数制限に注意されたし。
https://developers.line.biz/ja/reference/messaging-api/#get-narrowcast-progress-status


curl.exe -v -X POST https://api.line.me/v2/bot/message/broadcast　^
     -H "Content-Type: application/json" ^
     -H "Authorization: Bearer {ACCESSトークン}" ^
    -d " { \"to\": \"botのアカウントID\", \"messages\": [ { \"type\": \"image\", \"originalContentUrl\": \"　URL \", \"previewImageUrl\": \" URL \"} ] }"
