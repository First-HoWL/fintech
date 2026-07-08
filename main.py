from classes.blockchain import Blockchain
from classes.block import Block
from classes.miner import Miner
from classes.node import Node
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
import json

app = Flask(__name__)
CORS(app)

config = {}

with open("data/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

difficulty = 4
node = Node(name=config.get("name", "node_1"), apis=config.get("apis", []), difficulty=difficulty)

port=config.get("port")
delay = config.get("delay") # ms

def task():
    miner = Miner(name='miner_001')
        
    for i in range(1, 4):
        new_block = Block(
            index=i,
            timestamp=time.time(),
            data=f'Дані блоку #{i}',
            previous_hash=node.blockchain.last_block.hash,
        )
        mined_block = miner.mine_block(new_block, difficulty)
        node.post_block(mined_block)
    while True:
        for api in node.apis:
            try:
                node.request_chain(api)
            except Exception as e:
                print(f"Помилка при запиті до API {api}: {e}")
            
            try:
                node.request_apis(api)
            except Exception as e:
                print(f"Помилка при запиті до API {api}: {e}")
                
        time.sleep(delay)

@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/api/get_apis")
def get_apis():
    return {
        "success": True,
        "apis": node.get_apis()
        }

@app.route("/api/chain", methods=["GET"])
def get_chain():
    return jsonify({'chain': node.blockchain})

def main():
    app.run(debug=True, host="0.0.0.0", port=port)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=task, daemon=True)
    flask_thread.start()
    main()