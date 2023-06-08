#!/usr/bin/python3

import os
import datetime
import time
import requests
import json
import base64

## Custom modules
from modules.blockchain.smart_contract import SmartContractCaller
import direcciones_proyecto
from acquisition import adquisicion
from validar_certificado import validate

## blockchain url and addresses
smart_contract_address = direcciones_proyecto.smart_contract_address
eth_blockchain_url = direcciones_proyecto.eth_blockchain_url
abi_filename = os.path.abspath(direcciones_proyecto.abi_filename)

## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

print("Smart Contract is Loaded")

certificado = validate()

certId = certificado[0]
certBytes = certificado[1]
certOwner = certificado[2]

archivo_log = adquisicion()

with open(archivo_log, 'r') as f:
	blockchain_store = f.read()

print()
print("Log file name: ", archivo_log)
print()
print("Store this payload to Ethereum Blockchain")
print(blockchain_store)

certOwner = "\nEvidence stored by user with certificate:  " + certOwner

smart_contract_instance.storeEvidence(blockchain_store,certId, certBytes, certOwner)
print()
print()
