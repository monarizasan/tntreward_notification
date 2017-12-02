# tntreward_notification
TNTreward_notification_using_LINE_Notify

LINE Notifyを使ってTNTリワードの当落をLINEに通知します。ちなみにTelegram用にもっと高機能のもの（https://github.com/kevinrombach/TNTNodeMonitorBot ）がすでにありますので、よほどのことがない限りそちらの方がおすすめです。どうしてもLINEが使いたいという方だけご使用ください。

必要な準備

・Etherscan（https://etherscan.io/ ）にログインして（アカウントがなければ作成して）、API-KEYを作成します。

・LINE Notifyのトークンを作成します。参考になるサイト：https://qiita.com/takeshi_ok_desu/items/576a8226ba6584864d95

・サーバ（作者はこのプログラムをTNTノードが稼動しているサーバ上で一緒に動かしています。）

設定方法

1. サーバにログインしてとりあえずこのリポジトリをgit cloneする。

    `git clone https://github.com/monarizasan/tntreward_notification.git`
    
2. 作成されたtntreward_notificationディレクトリへ移動してnodelist.txtを開きます。

    `cd tntreward_notification`
    
    `nano nodelist.txt`
    
   リワードの当落を調べたいノードの情報を、ノード名=ノードアドレス のようにnodelist.txtに記載します。
   
   複数のノードを登録する際には、1行に1つずつノード情報を記載をノード名=ノードアドレス のように記載します。
   
3. 次にTNTreward_notification.pyを開き、8行目にEtherscanのAPI-KEYを、9行目にLINE Notifyのトークンを、13行目にnodelist.txtのフルパスを記載します。

4. TNTreward_notification.pyの10-12行目の部分では必要に応じて残高チェックの有無、通知パターン、LINEスタンプの有無が設定可能です（後述）が、ここではbalance_notify = 1、notify_pattern = 1、line_stamp = 1のままとりあえず次へ進みます。

5. 下記を実行し、TNTreward_notification.pyのオーナーと実行権限を変更します。

    `sudo chmod 700 TNTreward_notification.py`
    
    `sudo chown root:root TNTreward_notification.py`
    
6. cronを設定し、TNTreward_notification.pyが30分ごとに実行されるように設定します。

    `sudo crontab -u root -e`
    
   上記コマンドでcrontabが開くので（初めての場合には使用するエディタを聞かれるので好きなものを選びます）、下記を追記します。
   
    `1,31 * * * * export PATH=$PATH:/usr/bin/;python3 /home/[username]/TNTreward_notification/TNTreward_notification.py`
    
   [username]部分は該当するユーザー名に置き換えてください。
   
   追記したらcrontabを上書き保存すると、cronが30分ごとにTNTreward_notification.pyを実行します。
   
   以上で設定自体は終了です。通知を中止する場合には追記した行を消去してください。
   
   以降は残高チェックの有無、通知パターン、LINEスタンプの有無が設定についてです。
   
7. TNTreward_notification.pyの10行目、balance_notifyは

    0:リワード当選時にTNT残高は通知しない。
   
    1:リワード当選時に当選したアドレスのTNT残高も同時に通知する。
   
    2:リワード当選時に登録した全てのアドレスのTNT残高を同時に通知する。
   
   の中から設定が可能です。デフォルトではbalance_notify=1に設定されています。
   
8. TNTreward_notification.pyの11行目、notify_patternは

    0:リワードが当選した時だけ通知する。
    
    1:リワードの当選も落選も通知する。
    
   の中から設定が可能です。デフォルトではnotify_pattern=1に設定されています。
   
9. TNTreward_notification.pyの12行目、line_stampは

    0:通知の時にLINEスタンプは送られてこない。
   
    1:当選通知時には嬉しいっぽい感じのLINEスタンプがランダムで一緒に送られてきて、落選通知時には悲しいっぽい感じのLINEスタンプがランダムで一緒に送られてくる。
    
   の中から設定が可能です。デフォルトではline_stamp=1に設定されています。
   
以上で設定は終了です。何かありましたら作者のtwitterアカウント（https://twitter.com/dankepy ）までご連絡ください。
