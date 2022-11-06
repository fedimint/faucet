import os
import requests
import random
import json

from flask_qrcode import QRcode
from flask import Flask, render_template, request
from lightning import LightningRpc

rpc = LightningRpc(os.environ['RPC_SOCKET'])
connect_str = os.environ['CONNECT_STRING']
app = Flask(__name__)
QRcode(app)

BITCOIND_URL = "http://127.0.0.1:18443"
BITCOIND_USER = "bitcoin"
BITCOIND_PASSWORD = "bitcoin"

def rpc(method, params=[]):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": "minebet",
        "method": method,
        "params": params
    })
    return requests.post(BITCOIND_URL, auth=(BITCOIND_USER, BITCOIND_PASSWORD), data=payload).json()

def block_height():
    return rpc("getblockchaininfo")["result"]["blocks"]

def new_address():
    return rpc("getnewaddress")["result"]

def mine_blocks(num_blocks):
    address = new_address()
    return rpc("generatetoaddress", params=[num_blocks, address])

@app.route('/', methods=['GET', 'POST'])
def index():
    invoice = None
    pay_result = None

    if request.method == 'POST':
        # create invoice
        if 'amount' in request.form:
            # convert to sats
            amount = int(request.form['amount']) * 1000
            invoice = rpc.invoice(amount, str(random.random()), 'test')['bolt11']

        # pay invoice
        if 'invoice' in request.form:
            pay_result = str(rpc.pay(request.form['invoice']))

        # mint blocks
        if 'blocks' in request.form:
            print("mining", type(request.form["blocks"]))
            result = mine_blocks(int(request.form["blocks"]))
            print(result)

    height = block_height()
             
    return render_template('index.html', name='justin', 
        invoice=invoice, pay_result=pay_result, connect_str=connect_str, height=height)

