# tntreward_notification
TNTreward_notification_using_LINE_Notify

![img_1617](https://user-images.githubusercontent.com/32188449/33521399-653bf124-d814-11e7-97d4-342e1174c26c.jpg)

上の画像のようにLINE Notifyを使ってTNTリワードの当落をLINEに通知します。ちなみにTelegram用にもっと高機能のもの（https://github.com/kevinrombach/TNTNodeMonitorBot ）がすでにありますので、よほどのことがない限りそちらの方がおすすめです。どうしてもLINEが使いたいという方だけご使用ください。

必要な準備

・Etherscan（https://etherscan.io/ ）にログインして（アカウントがなければ作成して）、API-KEYを作成します。

<img width="504" alt="etherscan1" src="https://user-images.githubusercontent.com/32188449/33521257-94a713a2-d810-11e7-9209-80c296906e60.png">

   上記の左側のAPI-KEYsをクリックして

<img width="515" alt="etherscan2" src="https://user-images.githubusercontent.com/32188449/33521265-bab08ccc-d810-11e7-9716-53775d864587.png">

   出てきた右側の青いCreate Api Keyというボタンを押してAPI-KEYを作成し、設定後に表示されたAPI-KEYを記録しておきます。

・LINE Notifyのトークンを作成して記録しておきます。参考になるサイト：https://qiita.com/takeshi_ok_desu/items/576a8226ba6584864d95

・サーバ（作者はこのプログラムをTNTノードが稼動しているサーバ上で一緒に動かしていますので、その方法であれば新たにサーバは必要ありません。）を稼働させます。

設定方法

1. サーバにログインしてとりあえずこのリポジトリ（https://github.com/monarizasan/tntreward_notification ）をgit cloneする。

    `git clone https://github.com/monarizasan/tntreward_notification.git`
    
2. 作成されたtntreward_notificationディレクトリへ移動してnodelist.txtを開きます。

    `cd tntreward_notification`
    
    `nano nodelist.txt`
    
   リワードの当落を調べたいノードの情報を、ノード名=ノードアドレス のようにnodelist.txtに記載します。
   
<img width="443" alt="nodelist" src="https://user-images.githubusercontent.com/32188449/33521285-700fef40-d811-11e7-8dd6-5b555383d50f.png">
   
   複数のノードを登録する際には、上の画像のように1行に1つずつノード情報を記載をノード名=ノードアドレス のように記載します。

3. 下記を実行し、TNTreward_notification.pyのオーナーと実行権限を変更します。

    `sudo chmod 700 TNTreward_notification.py`
    
    `sudo chown root:root TNTreward_notification.py`
    
4. cronを設定し、TNTreward_notification.pyが30分ごとに実行されるように設定します。

    `sudo crontab -u root -e`
    
   上記コマンドでcrontabが開くので（初めての場合には使用するエディタを聞かれるので好きなものを選びます）、下記のコマンドを追記します。(crontabに下記を1行で追記します)
   
    `3,33 * * * * export PATH=$PATH:/usr/bin/;python3 /home/[username]/tntreward_notification/TNTreward_notification.py --nodes /home/[username]/tntreward_notification/nodelist.txt --etherscan-token [etherscanトークン] --line-token [lineトークン] --balance-notify elected --notify-pattern winlose`
    
   [username]、[etherscanトークン]、[lineトークン]部分は該当する自分のものに置き換えてください。例えば下記のようになります。
   
   `3,33 * * * * export PATH=$PATH:/usr/bin/;python3 /home/monarisa/tntreward_notification/TNTreward_notification.py --nodes /home/monarisa/tntreward_notification/nodelist.txt --etherscan-token ABCR4IA9862D7V9W1777HHHZA3FRGGGGFQ --line-token LW699999ffffddddPJUSywDssssggggiiiiTgkAd --balance-notify elected --notify-pattern winlose`
   
   追記したらcrontabを上書き保存すると、cronが30分ごとにTNTreward_notification.pyを実行します。
   
   以上で設定自体は終了です。通知を中止する場合にはcrontabに追記した行を消去してください。
   
   以下の画像のようにリワードが当たったかどうかがLINEに通知されてきます。
   
   ![img_16162](https://user-images.githubusercontent.com/32188449/33521392-3c84c5f8-d814-11e7-9524-6f71e1e9b388.jpg)
   
   ![img_1616](https://user-images.githubusercontent.com/32188449/33521395-5fbc8934-d814-11e7-8be8-fead1553dcf8.jpg)

   ![img_1617](https://user-images.githubusercontent.com/32188449/33521399-653bf124-d814-11e7-97d4-342e1174c26c.jpg)

   以降は残高チェックの有無、通知パターン、LINEスタンプの有無の設定についてです。
   
5. TNTreward_notification.pyのbalance-notifyオプションでは

    no:リワード当選時にTNT残高は通知しない。
   
    elected:リワード当選時に当選したアドレスのTNT残高も同時に通知する。
   
    all:リワード当選時に登録した全てのアドレスのTNT残高を同時に通知する。
   
   の中から設定が可能です。上述のサンプルコマンドでは--balance-notify electedに設定されています。
   
6. TNTreward_notification.pyのnotify-patternオプションでは

    win:リワードが当選した時だけ通知する。
    
    winlose:リワードの当選も落選も通知する。
    
   の中から設定が可能です。上述のサンプルコマンドでは--notify-pattern winloseに設定されています。リワード当選時のみの通知にしたい場合には、--notify-pattern winに設定してください。
   
9. --without-line-stampオプションをつけると通知時にLINEスタンプが送られてこなくなります。

＊etherscanのapiを30分ごとにたたくスクリプトなので、そんなに負荷がかからない分リワードアドレス決定のタイミング次第でリワード当落通知が1回分(30分)遅れて通知されることがあるようです。現在解決策を考え中です。取り急ぎの回避策として、上のコマンドでは毎時3分と33分に通知となっています。
   
以上で設定は終了です。何かありましたら作者のtwitterアカウント（https://twitter.com/dankepy ）までご連絡ください。
