#/usr/bin/python3

import requests
import random

#####################################################################################

etherscan_api = ''
linenotify_token = ''
balance_notify = 1  #{0:no TNT balance notify, 1:elected address only, 2:all address}
notify_pattern = 1  #{0:win only, 1:win and lose}
line_stamp = 1  #{0:no Line stamp, 1:Line stamp will be sent with notify}
filename = '/home/[username]/tntreward_notification/nodelist.txt'

#####################################################################################

tnt_balances = []
contact_address = '0x08f5a9235b08173b7569f83645d2c7fb55e8ccd8'
tntreword_address = '0xddfff2b78463ab1ca781e853bb888fdfd06083d3'

PREFIX = 'https://api.etherscan.io/api?'
MODULE = 'module='
ACTION = '&action='
CONTRACT_ADDRESS = '&contractaddress='
ADDRESS = '&address='
SORT = '&sort='
START_BLOCK = '&startblock='
END_BLOCK = '&endblock='
BLOCKNO = '&blockno='
TAG = '&tag='
API_KEY = '&apikey='

def get_nodelist(filename):

    """Get node addresses from txt file"""

    file = open(filename)
    nodelist = file.readlines() 
    file.close()

    nodenames = []
    nodeaddresses = []

    for i in nodelist:
        nodenames.append(i.split('=')[0])
        nodeaddresses.append(i.split('=')[1][0:42])

    return nodenames, nodeaddresses

def get_tnt_balance(etherscan_api, target_address, contact_address):

    """Get TNT balance from target address"""

    global tnt_balances

    api_url = PREFIX\
             +MODULE+'account'\
             +ACTION+'tokenbalance'\
             +CONTRACT_ADDRESS+contact_address\
             +ADDRESS+target_address\
             +TAG+'latest'\
             +API_KEY+etherscan_api

    r = requests.get(api_url)
    json = r.json()

    tnt_balances.append(int(json['result'])/100000000)

def get_elected_address(etherscan_api, tntreword_address):

    """Get an address which is a destination of last transaction of
    an address for sending TNT rewards"""

    api_url_tnt = PREFIX\
             +MODULE+'account'\
             +ACTION+'txlist'\
             +ADDRESS+tntreword_address\
             +START_BLOCK+'0'\
             +END_BLOCK+'99999999'\
             +SORT+'asc'\
             +API_KEY+etherscan_api

    def check_from(result):

        """Determine whether obtained transaction indicates paying from
        an address for sending TNT rewards"""

        if(result['from'] == tntreword_address):
            return 1
        else:
            return 0

    r_tnt = requests.get(api_url_tnt)
    json_tnt = r_tnt.json()
    last_tx_input = list(filter(check_from, json_tnt["result"]))[-1]['input']
    elected_address = last_tx_input[:2] + last_tx_input[34:74]

    return elected_address

def line_notify(elected_address, nodeaddresses):

    """Notify win or lose using LINE Notify"""

    url = "https://notify-api.line.me/api/notify"
    token = linenotify_token
    headers = {"Authorization" : "Bearer "+ token}

    if elected_address in nodeaddresses:

        elected_nodename = nodenames[nodeaddresses.index(elected_address)]

        if balance_notify == 0:
            message = elected_nodename + ' Winner!'

        elif balance_notify == 1:
            get_tnt_balance(etherscan_api, elected_address, contact_address)
            balance = tnt_balances[nodeaddresses.index(elected_address)]
            message = elected_nodename + ' Winner! Now ' + elected_nodename \
                      + ' has ' + str(balance) + ' TNT!'
                      
        else:
            balance = ['\n']
            for target_address in nodeaddresses:
                get_tnt_balance(etherscan_api, target_address, contact_address)

            for i in range(len(nodeaddresses)):
                balance.append(nodenames[i] + ' ' + str(tnt_balances[i]) + ' TNT' + '\n')

            message = elected_nodename + ' Winner!' + ''.join(balance) \
                      + 'total: ' + str(sum(tnt_balances)) + ' TNT'

        if line_stamp == 0:

            payload = {"message":message}

        else:

            stamp_num = [[1,2],[1,4],[1,5],[1,10],[1,13],[1,14],[1,106],[1,107],\
                         [1,114],[1,116],[1,125],[1,134],[1,137],[1,138],[1,139],\
                         [1,407],[2,22],[2,34],[2,144],[2,156],[2,167],[2,171],\
                         [2,172],[2,176],[2,179],[2,501],[2,513],[2,514],[2,516],\
                         [2,525]]

            stamp_num_win = random.choice(stamp_num)

            payload = {"message":message, 'stickerPackageId':stamp_num_win[0], 'stickerId':stamp_num_win[1]}

        r = requests.post(url ,headers=headers ,params=payload)

    else:

        message_lose = 'You lost this time...'

        if line_stamp == 0 and notify_pattern == 1:

            payload = {"message":message_lose}

            r = requests.post(url ,headers=headers ,params=payload)

        elif line_stamp == 1 and notify_pattern == 1:

            stamp_num = [[1,3],[1,7],[1,8],[1,9],[1,16],[1,17],[1,21],[1,102],\
                         [1,104],[1,105],[1,108],[1,111],[1,112],[1,113],[1,118],\
                         [1,121],[1,123],[1,127],[1,129],[1,131],[1,133],[1,135],\
                         [1,401],[1,403],[1,416],[1,417],[1,418],[1,419],[1,420],\
                         [1,421],[1,422],[1,423],[1,424],[2,18],[2,23],[2,24],\
                         [2,25],[2,32],[2,145],[2,152],[2,154],[2,168],[2,173],\
                         [2,174],[2,517],[2,519],[2,520],[2,523],[2,525]]

            stamp_num_lose = random.choice(stamp_num)

            payload = {"message":message_lose, 'stickerPackageId':stamp_num_lose[0], 'stickerId':stamp_num_lose[1]}

            r = requests.post(url ,headers=headers ,params=payload)


nodenames, nodeaddresses = get_nodelist(filename)
elected_address = get_elected_address(etherscan_api, tntreword_address)
line_notify(elected_address, nodeaddresses)

exit

