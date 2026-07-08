from classes.blockchain import Blockchain
from classes.block import Block
from classes.miner import Miner
import requests as request

class Node:
    def __init__(self, name, apis, difficulty):
        self.name = name
        self.blockchain = Blockchain(difficulty=difficulty)
        self.apis = apis
    
    def get_chain(self):
        return self.blockchain
    
    def post_chain(self, chain):
        if len(self.blockchain.chain) >= len(chain.chain):
            pass
        elif not self.blockchain.is_chain_valid():
            print(f'{self.name} received an invalid chain')
            if chain.is_chain_valid():
                self.blockchain = chain
        else:
            if chain.is_chain_valid():
                self.blockchain = chain
                print(f'{self.name} received a valid chain (length: {chain.chain.__len__()} blocks)')
    
    def get_apis(self):
        return self.apis
    
    def post_apis(self, apis):
        for api in apis:
            if not self.apis.__contains__(api):
                self.apis.append(api)

    def request_chain(self, api):
        response = request.get(f'{api}/api/chain')
        if response.status_code != 200:
            print(f'Error requesting chain from {api}: {response.status_code}')
            return
        
        data = response.json()
        received_blockchein = Blockchain()
        received_blockchein.difficulty = data['chain']['difficulty']
        received_blockchein.chain = [Block.from_dict(d) for d in data['chain']['chain']]
        self.post_chain(received_blockchein)
    
    def request_apis(self, api):
        response = request.get(f'{api}/api/get_apis')
        if response.status_code != 200:
            print(f'Error requesting apis from {api}: {response.status_code}')
            return
        
        data = response.json()
        self.post_apis(data["apis"])

    def post_block(self, block_data):
        return self.blockchain.add_block(block_data)    