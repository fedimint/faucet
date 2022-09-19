#!/usr/bin/env python

import os
import random
import json

from flask_qrcode import QRcode
from flask import Flask, render_template, request
from lightning import LightningRpc

rpc = LightningRpc(os.environ['RPC_SOCKET'])
connect_str = os.environ['CONNECT_STRING']
app = Flask(__name__)
QRcode(app)

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
            try:
                pay_result = str(rpc.pay(request.form['invoice']))
            except Exception as e:
                pay_result = str(e)
             
    return render_template('index.html', name='justin', 
        invoice=invoice, pay_result=pay_result, connect_str=connect_str)


if __name__ == "__main__":
    app.run(port = 3000)