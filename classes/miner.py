import hashlib
import json
import time
from classes.block import Block


class Miner:

    def __init__(self, name):
        self.name = name
        

    def mine_block(self, block, difficulty):
        nonce = 0
        while not block.hash.startswith('0' * difficulty):
            nonce += 1
            block.nonce = nonce
            block_content = block.to_dict(with_hash=False)

            block_string = json.dumps(block_content)
            block.hash = hashlib.sha256(block_string.encode()).hexdigest()
        
        return block
        
 