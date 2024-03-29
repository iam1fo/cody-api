from flask import Flask, jsonify
import random
import string

app = Flask(__name__)

# Function to generate a random premium code
def generate_premium_code():
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(4)) + '-' + \
           ''.join(random.choice(string.digits) for _ in range(4)) + '-' + \
           ''.join(random.choice(string.digits) for _ in range(4)) + '-' + \
           ''.join(random.choice(string.digits) for _ in range(4))

# Endpoint to create a premium code
@app.route('/create/premiumcode', methods=['GET'])
def create_premium_code():
    premium_code = generate_premium_code()
    with open('premium_codes.txt', 'a') as file:
        file.write(premium_code + '\n')
    return jsonify({"premium_code": premium_code})

# Endpoint to redeem a premium code
@app.route('/redeem/premiumcode/<premium_code>', methods=['GET'])
def redeem_premium_code(premium_code):
    # Check if the premium code is valid
    with open('premium_codes.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        found = False
        for line in lines:
            if line.strip() == premium_code:
                found = True
                continue
            file.write(line)
        file.truncate()
    
    if found:
        return jsonify({"message": "Premium code redeemed successfully"})
    else:
        return jsonify({"error": "Invalid premium code"}), 400
