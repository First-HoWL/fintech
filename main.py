from classes.blockchain import Blockchain
from classes.block import Block
from classes.miner import Miner
import time

def main():
    difficulty = 5
    blockchain = Blockchain(difficulty)
    miner = Miner(name='miner_001')
    

    for i in range(1, 4):
        new_block = Block(
            index=i,
            timestamp=time.time(),
            data=f'Дані блоку #{i}',
            previous_hash=blockchain.last_block.hash,
        )
        mined_block = miner.mine_block(new_block, difficulty)
        blockchain.add_block(mined_block)

    blockchain.print_chain()
    print('Ланцюг валідний:', blockchain.is_chain_valid())

if __name__ == '__main__':
    main()