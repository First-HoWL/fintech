from classes.block import Block
import time

class Blockchain:
    def __init__(self, difficulty = 2):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis_block(self):
        return Block(index=0, timestamp=time.time(), previous_hash='0' * 64, data='Genesis Block', nonce=0)

    def add_block(self, block):
        if block.previous_hash != self.last_block.hash:
            print(f'Відхилено блок #{block.index} через некоректний хеш попереднього блоку.')
            return False
        if block.hash != block.compute_hash():
            print(f'Відхилено блок #{block.index} через некоректний хеш.')
            return False
        
        if not block.hash.startswith('0' * self.difficulty):
            print(f'Відхилено блок #{block.index} через невіповідність умові складності.')
            return False

        self.chain.append(block)
        print(f'Блок #{block.index} прийнято у ланцюг.')
        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current, previous = self.chain[i], self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.hash != current.compute_hash():
                return False
        return True

    def to_dict(self):
        return {
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain]
        }

    def print_chain(self):
        for block in self.chain:
            print(block)