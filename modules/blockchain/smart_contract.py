#!/usr/bin/python3

import time
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json
import datetime
import sys
sys.path.append("../../")
from direcciones_proyecto import smart_contract_address, eth_blockchain_url, abi_filename


class SmartContractCaller:
    def __init__(self, smart_contract_address, eth_blockchain_url):
        self.smart_contract_address = smart_contract_address
        self.eth_blockchain_url = eth_blockchain_url
        self.contract_events = None

 
    def load_abi(self, abi_filename):
        ## load the abi
        with open(abi_filename, "r") as abi_file:
            try:
                self.abi_ = json.load(abi_file)
            except:
                print('Failed to open the ABI')

    def create_smartcontract_obj(self):
        ## make a connection to the blockchain node
        self.w3 = Web3(HTTPProvider(self.eth_blockchain_url))

        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        ## Convert address to checksummed address
        self.checksum_smart_contract_address = Web3.toChecksumAddress(self.smart_contract_address)

        ## get address of the node
        self.executor_address = self.w3.eth.accounts[0]

        ## connect to the smart contract
        self.contract = self.w3.eth.contract(address=self.checksum_smart_contract_address, abi=self.abi_)

        self.contract_events = self.contract_events

    # Function to get current ID from blockchain
    def getID(self):
        id = self.contract.functions.getID().call({"from":self.executor_address})

    # Function to register certificate
    def registerCertificate(self, certificateId, certificate, cert_owner):
        tx_hash = self.contract.functions.registerCertificate(certificateId, certificate, cert_owner).transact({'from': self.executor_address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt['status'] == 1:
           print("Certificate registered successfully")
        else:
           print("Error registering certificate")

    # Function to store evidence
    def storeEvidence(self, file_hash, certificateId, certificate, certificateData):
        tx_hash = self.contract.functions.storeEvidence(file_hash, certificateId, certificate, certificateData).transact({'from': self.executor_address})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        if tx_receipt['status'] == 1:
            result = self.contract.events.setHashEvent().processReceipt(tx_receipt)
            print("Evidence stored successfully")
            return result[0]['args']
        else:
            print("Error storing evidence")
            
    # Function to retrieve latest evidence
    def getLatestEvidence(self, certificateId, certificate):
        #GANACHE
        #evidence_aux = self.contract.functions.getLatestEvidence(certificateId, certificate).call()
        
        #PoA
        evidence_aux = self.contract.functions.getLatestEvidence(certificateId, certificate).transact({'from': self.executor_address})
        
        event_filter = self.contract.events.deviceEvent.createFilter(fromBlock='latest')

        events = event_filter.get_all_entries()

        #evidence = self.contract.functions.getLatestEvidence().call()
        for event in events:
        	print("Event: ", event.args._message)
        	print("Sender: ", event.args._from)
        print("Evidence ID: ", evidence_aux[0])
        print("Evidence:", evidence_aux[1])
        print("Timestamp:", evidence_aux[2])
        print(evidence_aux[3])

