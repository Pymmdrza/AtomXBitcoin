# Programmer Mmdrza
# Atom X Bitcoin (CPU SAVER MOD) ~ Trial Version.
# Website : https://Mmdrza.Com
# Github : Github.com/PyMmdrza
# Telegram Channel : t.me/mPython3
# Telegram ID : t.me/PyMmdrza
# ------------------------------------------------

import random
from lxml import html
from rich.console import Console
import sys
from os import system
import time
import hashlib
import binascii
import multiprocessing
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
import threading
import base58
import ecdsa
import requests
import os
import subprocess
import base58
import ecdsa
import requests

console = Console()


def generate_private_key():
    return binascii.hexlify(os.urandom(32)).decode('utf-8')


def private_key_to_WIF(private_key):
    var80 = "80" + str(private_key)
    var = hashlib.sha256(binascii.unhexlify(hashlib.sha256(binascii.unhexlify(var80)).hexdigest())).hexdigest()
    return str(base58.b58encode(binascii.unhexlify(str(var80) + str(var[0:8]))), 'utf-8')


def private_key_to_public_key(private_key):
    sign = ecdsa.SigningKey.from_string(binascii.unhexlify(private_key), curve=ecdsa.SECP256k1)
    return ('04' + binascii.hexlify(sign.verifying_key.to_string()).decode('utf-8'))


def public_key_to_address(public_key):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    count = 0
    val = 0
    var = hashlib.new('ripemd160')
    var.update(hashlib.sha256(binascii.unhexlify(public_key.encode())).digest())
    doublehash = hashlib.sha256(
        hashlib.sha256(binascii.unhexlify(('00' + var.hexdigest()).encode())).digest()).hexdigest()
    address = '00' + var.hexdigest() + doublehash[0:8]
    for char in address:
        if (char != '0'):
            break
        count += 1
    count = count // 2
    n = int(address, 16)
    output = []
    while (n > 0):
        n, remainder = divmod(n, 58)
        output.append(alphabet[remainder])
    while (val < count):
        output.append(alphabet[0])
        val += 1
    return ''.join(output[::-1])


def data_export(queue):
    zi = 0
    wi = 0
    while True:
        zi += 1
        sys.stdout.write(f"\x1b]2;Total:{zi} Found:{wi}\x07")

        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        address = public_key_to_address(public_key)
        data = (private_key, address, wi, zi)
        queue.put(data, block=False)


def worker(queue):
    while True:
        if not queue.empty():
            data = queue.get(block=True)
            process(data)


def process(data):
    private_key = data[0]
    address = data[1]
    urlblock = "https://bitcoin.atomicwallet.io/address/" + str(address)
    respone_block = requests.get(urlblock)
    byte_string = respone_block.content
    source_code = html.fromstring(byte_string)
    xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
    treetxid = source_code.xpath(xpatch_txid)
    balance = str(treetxid[0].text_content())
    iffer = str('0 BTC')
    zi = data[3]
    wi = data[2]

    if str(balance) == str(iffer):
        console.print("[gold1]Total:[/gold1][cyan]" + str(zi * 8) + "[/cyan] : [green]Win:[/green][white]" + str(
            wi) + "[/white][red] ~ [/][gold1]" + str(address) + "[/gold1][red1] : [/red1][white]" + str(
            private_key) + "[/white] [red1]:[/red1] [cyan]" + str(
            balance) + "[/cyan]")
        zi += 1
    else:
        wi += 1
        with open("Winning.txt", "a", encoding="utf-8") as xf:
            xf.write(f"ADDRESS: {address}               BALANCE:{balance}\n"
                     f"PRIVATE KEY: {private_key}\n"
                     f"-----------------[ {time.thread_time()} ]------------------\n"
                     f"==================[ M M D R Z A . C o M ]==================\n")
            xf.close()


def thread(iterator):
    processes = []
    data = Queue()
    data_factory = Process(target=data_export, args=(data,))
    data_factory.daemon = True
    processes.append(data_factory)
    data_factory.start()
    work = Process(target=worker, args=(data,))
    work.daemon = True
    processes.append(work)
    work.start()
    data_factory.join()


if __name__ == '__main__':
    pool = ThreadPool(processes=multiprocessing.cpu_count())
    pool.map(thread, range(8))
    pool.close()
    exit()
