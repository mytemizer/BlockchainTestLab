# Create Module 1 - Create a Blockchain

import datetime
import hashlib
import json

from flask import Flask, jsonify


# Part 1 - Building a Blockchain

class Blockchain:

    
    def __init__(self):
        
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0') #SHA 256 get only string


    def createBlock(self, proof, previousHash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()), 
            'proof' : proof, 
            'previousHash' : previousHash
        }
        self.chain.append(block)
        return block
        
    def getPreviousBlock(self):
        return self.chain[-1]
        
    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        
        while checkProof is False:
            
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        
        return newProof
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
        
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        
        while blockIndex < len(chain):
            block = chain[blockIndex]
            if block['previousHash'] != self.hash(previousBlock):
                return False

            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()            
            
            if hashOperation[:4] != '0000':
                return False
            
            previousBlock = block
            blockIndex += 1
            
        return True
        
# Part 2 - Mining out Blockchain


# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new blcok
@app.route('/mineBlock', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    
    proof = blockchain.proofOfWork(previousProof)
    
    previousHash = blockchain.hash(previousBlock)

    block = blockchain.createBlock(proof, previousHash)
    
    response = {
        'message' : 'Congrutilations, you just mined a block!',
        'index' : block['index'],
        'timestamp' : block['timestamp'], 
        'proof' : block['proof'], 
        'previousHash' : block['previousHash']
    }
    
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/getChain', methods=['GET'])
def getBlockchain():
    response = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain)
    }
    
    return jsonify(response), 200

# Checking validity of the chain
@app.route('/checkValidity', methods=['GET'])
def checkValidity():
    isValid = blockchain.isChainValid(blockchain.chain)
    
    if isValid:
        message = "Everything is perfect!"
    else:
        message = "There are some problems!, Chain is not valid"
    
    response = {
        'isValid' : isValid,
        'message' : message
    }

    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)


