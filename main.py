from flask import Flask, jsonify
from flask_cors import CORS
from pycardano import PaymentKeyPair, Address, Network

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Hello, Flask on Pyodide!"

@app.route('/some_route')
def some_route():
    return "<p>Data loaded from Flask!</p>"

@app.route('/pycardano')
def pycardano_route():
    # Generate a new key pair
    payment_key_pair = PaymentKeyPair.generate()

    # Get the address
    address = Address(payment_key_pair.verification_key.hash(), network=Network.TESTNET)

    return jsonify({
        "address": str(address)
    })

# Remove app.run() as it doesn't work in Pyodide
# Instead, we'll make the app callable through Pyodide's fetch mechanism 