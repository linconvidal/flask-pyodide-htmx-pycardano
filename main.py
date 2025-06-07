from flask import Flask, jsonify
from flask_cors import CORS
from pycardano import PaymentKeyPair, Address, Network
import random
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Hello, Flask on Pyodide!"

@app.route('/some_route')
def some_route():
    # Generate random dynamic data
    random_number = random.randint(1, 1000)
    random_float = round(random.uniform(0, 100), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
    <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
            <span class="font-medium text-blue-900">Random Integer:</span>
            <span class="text-xl font-bold text-blue-600">{random_number}</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
            <span class="font-medium text-green-900">Random Float:</span>
            <span class="text-xl font-bold text-green-600">{random_float}</span>
        </div>
        <div class="flex items-center justify-between p-3 bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg border border-purple-200">
            <span class="font-medium text-purple-900">Generated At:</span>
            <span class="text-sm font-mono text-purple-600">{timestamp}</span>
        </div>
        
        <details class="mt-4 group">
            <summary class="cursor-pointer flex items-center gap-2 text-sm font-medium text-zinc-700 hover:text-zinc-900 p-3 bg-zinc-100 hover:bg-zinc-50 rounded-t-lg border border-zinc-300 transition-colors duration-150 select-none hover:shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="details-icon transition-transform duration-300 ease-in-out group-open:rotate-90">
                    <path d="M6.375 7.125V4.658h1.78c.973 0 1.542.457 1.542 1.237 0 .802-.604 1.23-1.764 1.23H6.375zm0 3.762h1.898c1.184 0 1.81-.48 1.81-1.377 0-.885-.65-1.348-1.886-1.348H6.375v2.725z"/>
                    <path d="M4.002 0a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4h-8zm0 1h8a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-8a3 3 0 0 1-3-3V4a3 3 0 0 1 3-3z"/>
                </svg>
                <span>View Source Code</span>
            </summary>
            <div class="bg-[#282c34] rounded-b-lg border-x border-b border-zinc-300 overflow-hidden">
                <div class="flex items-center justify-between px-4 py-2 bg-[#21252b] text-xs text-zinc-400 border-b border-zinc-700">
                    <span>Python</span>
                    <span class="text-zinc-500">Flask Route</span>
                </div>
                <pre class="text-xs p-4 overflow-x-auto"><code class="language-python group-open:animate-fade-in-fast">@app.route('/some_route')
def some_route():
    # Generate random dynamic data
    random_number = random.randint(1, 1000)
    random_float = round(random.uniform(0, 100), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"..."  # HTML template with data</code></pre>
            </div>
        </details>
    </div>
    """

@app.route('/pycardano')
def pycardano_route():
    # Generate a new key pair
    payment_key_pair = PaymentKeyPair.generate()

    # Get the address for both mainnet and testnet
    testnet_address = Address(payment_key_pair.verification_key.hash(), network=Network.TESTNET)
    mainnet_address = Address(payment_key_pair.verification_key.hash(), network=Network.MAINNET)
    
    # Get key information
    verification_key_hex = payment_key_pair.verification_key.payload.hex()
    signing_key_hex = payment_key_pair.signing_key.payload.hex()
    verification_key_hash = payment_key_pair.verification_key.hash().payload.hex()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
    <div class="space-y-4">
        <div class="bg-gradient-to-r from-indigo-50 to-purple-50 p-4 rounded-lg border border-indigo-200">
            <h3 class="font-semibold text-indigo-900 mb-2">🏠 Addresses Generated</h3>
            <div class="space-y-2">
                <div>
                    <span class="text-xs font-medium text-indigo-700 uppercase tracking-wide">Testnet:</span>
                    <div class="font-mono text-sm text-indigo-800 break-all bg-white p-2 rounded mt-1">{str(testnet_address)}</div>
                </div>
                <div>
                    <span class="text-xs font-medium text-indigo-700 uppercase tracking-wide">Mainnet:</span>
                    <div class="font-mono text-sm text-indigo-800 break-all bg-white p-2 rounded mt-1">{str(mainnet_address)}</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gradient-to-r from-emerald-50 to-teal-50 p-4 rounded-lg border border-emerald-200">
            <h3 class="font-semibold text-emerald-900 mb-2">🔑 Key Information</h3>
            <div class="space-y-2 text-xs">
                <div>
                    <span class="font-medium text-emerald-700">Verification Key Hash:</span>
                    <div class="font-mono text-emerald-800 break-all bg-white p-2 rounded mt-1">{verification_key_hash}</div>
                </div>
                <div>
                    <span class="font-medium text-emerald-700">Verification Key:</span>
                    <div class="font-mono text-emerald-800 break-all bg-white p-2 rounded mt-1">{verification_key_hex}</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gradient-to-r from-amber-50 to-yellow-50 p-4 rounded-lg border border-amber-200">
            <h3 class="font-semibold text-amber-900 mb-2">📊 Generation Details</h3>
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span class="font-medium text-amber-700">Generated At:</span>
                    <div class="text-amber-800 font-mono">{timestamp}</div>
                </div>
                <div>
                    <span class="font-medium text-amber-700">Key Length:</span>
                    <div class="text-amber-800">{len(verification_key_hex)} hex chars</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gradient-to-r from-rose-50 to-pink-50 p-4 rounded-lg border border-rose-200">
            <h3 class="font-semibold text-rose-900 mb-2">⚠️ Security Notice</h3>
            <p class="text-sm text-rose-800">
                This is a demo key pair generated in the browser. 
                <strong>Never use these keys for real transactions!</strong>
            </p>
        </div>
        
        <details class="mt-4 group">
            <summary class="cursor-pointer flex items-center gap-2 text-sm font-medium text-zinc-700 hover:text-zinc-900 p-3 bg-zinc-100 hover:bg-zinc-50 rounded-t-lg border border-zinc-300 transition-colors duration-150 select-none hover:shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" class="details-icon transition-transform duration-300 ease-in-out group-open:rotate-90">
                    <path d="M6.375 7.125V4.658h1.78c.973 0 1.542.457 1.542 1.237 0 .802-.604 1.23-1.764 1.23H6.375zm0 3.762h1.898c1.184 0 1.81-.48 1.81-1.377 0-.885-.65-1.348-1.886-1.348H6.375v2.725z"/>
                    <path d="M4.002 0a4 4 0 0 0-4 4v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V4a4 4 0 0 0-4-4h-8zm0 1h8a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3h-8a3 3 0 0 1-3-3V4a3 3 0 0 1 3-3z"/>
                </svg>
                <span>View Source Code</span>
            </summary>
            <div class="bg-[#282c34] rounded-b-lg border-x border-b border-zinc-300 overflow-hidden">
                <div class="flex items-center justify-between px-4 py-2 bg-[#21252b] text-xs text-zinc-400 border-b border-zinc-700">
                    <span>Python</span>
                    <span class="text-zinc-500">PyCardano Route</span>
                </div>
                <pre class="text-xs p-4 overflow-x-auto"><code class="language-python group-open:animate-fade-in-fast">@app.route('/pycardano')
def pycardano_route():
    # Generate a new key pair
    payment_key_pair = PaymentKeyPair.generate()

    # Get the address for both mainnet and testnet
    testnet_address = Address(payment_key_pair.verification_key.hash(), 
                             network=Network.TESTNET)
    mainnet_address = Address(payment_key_pair.verification_key.hash(), 
                             network=Network.MAINNET)
    
    # Get key information
    verification_key_hex = payment_key_pair.verification_key.payload.hex()
    verification_key_hash = payment_key_pair.verification_key.hash().payload.hex()
    
    return f"..."  # HTML template with blockchain data</code></pre>
            </div>
        </details>
    </div>
    """

# Remove app.run() as it doesn't work in Pyodide
# Instead, we'll make the app callable through Pyodide's fetch mechanism 