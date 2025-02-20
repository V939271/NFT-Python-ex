import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, nft):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'nft': nft,
        })
        return self.last_block['index'] + 1
    
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
class NFT:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
    
    def __repr__(self):
        return f'NFT(name={self.name}, owner={self.owner})'
def mint_nft(blockchain, name, owner):
    nft = NFT(name, owner)
    blockchain.new_transaction(sender="0", recipient=owner, nft=nft)
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)
    return nft, block

# Initialize blockchain
blockchain = Blockchain()

# Mint a new NFT
nft, block = mint_nft(blockchain, "Cool Art", "Alice")

print(f"Newly minted NFT: {nft}")
print(f"Block containing the NFT: {block}")