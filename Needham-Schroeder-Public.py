"""Needham-Schroedr Public Key Protocol"""
import RSA
import random
# Generate Public/Private keys for Alice/Bob/Server (pub, pr, n) 
# Dict of 'certificates', alice and bob
NoncesUsed = set()

AliceInfo = RSA.key_generation()
Alice = dict()
Alice['pubKeyString'] = str(AliceInfo[0]) + "," + str(AliceInfo[1])
Alice['privKeyString'] = str(AliceInfo[2]) + "," + str(AliceInfo[1])
Alice['pubKey'] = (AliceInfo[0], AliceInfo[1])
Alice['privKey'] = (AliceInfo[2], AliceInfo[1])

BobInfo = RSA.key_generation()
Bob = dict()
Bob['pubKeyString'] = str(BobInfo[0]) + "," + str(BobInfo[1])
Bob['privKeyString'] = str(BobInfo[2]) + "," + str(BobInfo[1])
Bob['pubKey'] = (BobInfo[0], BobInfo[1])
Bob['privKey'] = (BobInfo[2], BobInfo[1])

ServerInfo = RSA.key_generation()
Server = dict()
Server['pubKeyString'] = str(ServerInfo[0]) + "," + str(ServerInfo[1])
Server['privKeyString'] = str(ServerInfo[2]) + "," + str(ServerInfo[1])
Server['pubKey'] = (ServerInfo[0], ServerInfo[1])
Server['privKey'] = (ServerInfo[2], ServerInfo[1])

ServerRecords = dict()
ServerRecords['Alice'] = Alice['pubKey']
ServerRecords['Bob'] = Bob['pubKey']


# Alice messages server for bob pub key using Spub

print("Alice -> Server: I need to message Bob")

# Server encrypts Bob's Public Key using Server Private Key
BobSignedFromServer = []
for char in Bob['pubKeyString']:
    BobSignedFromServer.append(RSA.encrypt(ord(char), Server['privKey'][0], Server['privKey'][1]))
for char in ',Bob':
    BobSignedFromServer.append(RSA.encrypt(ord(char), Server['privKey'][0], Server['privKey'][1]))
print("Server: Let me encrypt his public key and send it to you")

# Server sends to alice using Spr key

print("Server: Here is Bob's public key, encrypted with my private key:", BobSignedFromServer)

print("Alice: Thanks. I'll decrypt it to verify it came from the server, then use it to message Bob")

BobDecrypted = ''
for char in BobSignedFromServer:
    BobDecrypted += chr(RSA.decrypt(char, Server['pubKey'][0], Server['pubKey'][1]))
# print(BobDecrypted)
BobDecryptedKey = BobDecrypted.split(",")
# print(BobDecryptedKey)

print("Alice: Now that I have Bob's public key, I need a nonce to message him")

# Alice creates nonce
AliceNonce = random.randint(1, 1000000)
# print(AliceNonce)
# Encrypts and sends to Bob using Bobpub
print("Alice: I will encrypt my nonce and name to send to Bob now using his public key from the server")
AliceBobMessage = str(AliceNonce) + "Alice"
AliceBobMessageEncrypted = []
for char in AliceBobMessage:
    AliceBobMessageEncrypted.append(RSA.encrypt(ord(char), int(BobDecryptedKey[0]), int(BobDecryptedKey[1])))

# Bob gets Alicepub from Server
print("Bob: I'm getting a message from someone claiming to be Alice. Let me ask the server for Alice's public key to respond")
AliceBobMessageDecrypted = ""

for char in AliceBobMessageEncrypted:
    AliceBobMessageDecrypted += chr(RSA.decrypt(char, Bob['privKey'][0], Bob['privKey'][1]))

AliceDecryptedNonce = AliceBobMessageDecrypted.split("Alice")
# print(AliceBobMessageDecrypted)
# print(AliceDecryptedNonce)

print("Bob -> Server: I need to message Alice")

# Server encrypts Alice's Public Key using Server Private Key
AliceSignedFromServer = []
for char in Alice['pubKeyString']:
    AliceSignedFromServer.append(RSA.encrypt(ord(char), Server['privKey'][0], Server['privKey'][1]))
for char in ',Alice':
    AliceSignedFromServer.append(RSA.encrypt(ord(char), Server['privKey'][0], Server['privKey'][1]))
print("Server: Let me encrypt her public key and send it to you")

print("Server: Here is Alice's public key, encrypted with my private key:", AliceSignedFromServer)

print("Bob: Thanks. I'll decrypt it to verify it came from the server, then use it to message Alice")

AliceDecrypted = ''
for char in AliceSignedFromServer:
    AliceDecrypted += chr(RSA.decrypt(char, Server['pubKey'][0], Server['pubKey'][1]))
# print(BobDecrypted)
AliceDecryptedKey = AliceDecrypted.split(",")
# print(AliceDecryptedKey)

print("Bob: Now that I have Alice's public key, I need a nonce to message start the double handshake")
BobNonce = random.randint(1, 1000000)
BobAliceMessage = str(AliceDecryptedNonce[0]) + "," + str(BobNonce)

# sends Alice nonce and Bobs nonce (Encrypted) to Alice using Alicepub

BobAliceMessageEncrypted = []
for char in BobAliceMessage:
    BobAliceMessageEncrypted.append(RSA.encrypt(ord(char), int(AliceDecryptedKey[0]), int(AliceDecryptedKey[1])))

# Alice verifies her nonce was decrypted properly
print("Alice: I'm getting a message from someone claiming to be Bob. Let me check if he decrypted my nonce properly and then deccrypt his")
BobAliceMessageDecrypted = ""
for char in BobAliceMessageEncrypted:
    BobAliceMessageDecrypted += chr(RSA.decrypt(char, Alice['privKey'][0], Alice['privKey'][1]))
BobAliceMessageDecrypted = BobAliceMessageDecrypted.split(",")
# print(AliceNonce)
# print(BobAliceMessageDecrypted)
if int(BobAliceMessageDecrypted[0]) == AliceNonce:
    print("Alice: It's Bob, He successfully decrypted my nonce! I'll send his back so he knows its me!")
else:
    print("Alice: This isn't my nonce, so this may not be Bob")

# Alice sends Bob his decrypted nonce using Bobpub
AliceBobMessage2 = BobAliceMessageDecrypted[1]
AliceBobMessage2Encrypted = []
for char in AliceBobMessage2:
    AliceBobMessage2Encrypted.append(RSA.encrypt(ord(char), int(BobDecryptedKey[0]), int(BobDecryptedKey[1])))

# Bob verifies nonce his decrypted properly
AliceBobMessage2Decrypted = ""
for char in AliceBobMessage2Encrypted:
    AliceBobMessage2Decrypted += chr(RSA.decrypt(char, Bob['privKey'][0], Bob['privKey'][1]))
AliceBobMessage2Decrypted = AliceBobMessage2Decrypted.split(",")
if int(AliceBobMessage2Decrypted[0]) == BobNonce:
    print("Bob: It's Alice, she successfully decrypted my nonce! We have secure communications!")
else:
    print("Bob: This isn't my nonce, so this may not be Alice")

# Finished
