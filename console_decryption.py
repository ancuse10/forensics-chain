#!/usr/bin/python3

import os
import datetime
import time
import requests
requests.packages.urllib3.disable_warnings()
import json
import base64

## Custom modules
from modules.blockchain.smart_contract import SmartContractCaller
import direcciones_proyecto
from validar_certificado import validate

## blockchain url and addresses
smart_contract_address = direcciones_proyecto.smart_contract_address
eth_blockchain_url = direcciones_proyecto.eth_blockchain_url
abi_filename = os.path.abspath(direcciones_proyecto.abi_filename)

print("Smart contract is loaded")
## Smart Contract Setup
smart_contract_instance = SmartContractCaller(smart_contract_address, eth_blockchain_url)

## Load the ABI file
smart_contract_instance.load_abi(abi_filename)

## Create a smart contract obj to use
smart_contract_instance.create_smartcontract_obj()

print()
print("Sequence of steps to retrieve data:")

try:
        certificado = validate()
        certId = certificado[0]
        certBytes = certificado[1]
        certOwner = certificado[2]

        # Obtener última evidencia de la cadena de bloques
        print("Obtain last evidence from blockchain")
        evidence = smart_contract_instance.getLatestEvidence(certId, certBytes)
        print("\nEvidence acquired by user with certificate: " + certOwner)
except KeyboardInterrupt:
        print("Program interrupted by user.")

except Exception as e:
        print(f"Error in program: {e}")
