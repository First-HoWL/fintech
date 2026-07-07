import hashlib
import json

class Block:

    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = self.to_dict(with_hash=False)

        block_string = json.dumps(block_content)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self, with_hash=True):
        if with_hash:
            return {
                'index': self.index,
                'timestamp': self.timestamp,
                'data': self.data,
                'previous_hash': self.previous_hash,
                'nonce': self.nonce,
                'hash': self.hash,
            }
        else:
            return {
                'index': self.index,
                'timestamp': self.timestamp,
                'data': self.data,
                'previous_hash': self.previous_hash,
                'nonce': self.nonce,
            }

    def __repr__(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_dict(data):
        block = Block(data['index'], data['timestamp'], data['data'],
                      data['previous_hash'], data['nonce'])
        block.hash = data['hash']
        return block
 