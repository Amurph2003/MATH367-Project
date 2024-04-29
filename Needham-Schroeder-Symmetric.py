
import random
import re
# Generate Public/Private keys for Alice/Bob/Server (pub, pr, n) 
# Dict of 'certificates', alice and bob
NoncesUsed = set()

def encrypt(key, message):
    key = key.upper()
    shifts = []
    for i in key:
        shifts.append(ord(i) - 65)

    key_index = 0
    message_index = 0
    encrypted = ""
    message = message.upper().replace(",", "")
    while (message_index < len(message)):
        if message[message_index].isdigit():
            pt_char = ord(message[message_index]) - 48
            encrypted_char = (pt_char + shifts[key_index]) % 10
            encrypted += chr(encrypted_char + 48)
        else:
            pt_char = ord(message[message_index]) - 65
            encrypted_char = (pt_char + shifts[key_index]) % 26
            encrypted += chr(encrypted_char + 65)

        message_index += 1
        key_index = (key_index + 1) % len(key)

    return encrypted

def decrypt(key, encrypted_message):
    shifts = []
    key = key.upper()
    for i in key:
        shifts.append(ord(i) - 65)

    key_index = 0
    ct_index = 0
    decrypted = ""
    ct = encrypted_message.upper()
    while (ct_index < len(ct)):
        if ct[ct_index].isdigit():
            ct_char = ord(ct[ct_index]) - 48
            pt_char = (ct_char - shifts[key_index]) % 10
            if pt_char < 0:
                pt_char += 10
            decrypted += chr(pt_char + 48)
        else:
            ct_char = ord(ct[ct_index]) - 65
            pt_char = (ct_char - shifts[key_index])
            if pt_char < 0:
                pt_char += 26
            decrypted += chr(pt_char + 65)

        ct_index += 1
        key_index = (key_index + 1) % len(key)

    return decrypted

def keyGeneration():
    length = 6
    key = ""
    for _ in range(length):
        key += chr(random.randint(0, 25) + 65)
    return key

AliceServerKey = keyGeneration()
BobServerKey = keyGeneration()

AliceNonce1 = random.randint(1, 1000000)

print("Alice: I want to message Bob. Let me talk to the server\n")
print("Alice -> Server: I want to talk to Bob, here's my nonce\n")

AliceServerMessage = "Alice,Bob,"+str(AliceNonce1)

print("Server: I received your message, Let me get the info\n")

ck = random.randint(1, 1000000)
BobEncrypt1 = encrypt(BobServerKey, str(ck)+"Alice")
ServerAliceMessage = str(AliceNonce1)+"Bob"+str(ck)+"ENC"+BobEncrypt1
# print(ServerAliceMessage)
ServerAliceMessageEncrypted = encrypt(AliceServerKey, ServerAliceMessage)
pServerAliceMesageEncrypted = re.split("ENC", ServerAliceMessage)
pServerAliceMesageEncrypted[0] = re.split("Bob", pServerAliceMesageEncrypted[0])

print(f"Server -> Alice: Here's the message for you using our key: {pServerAliceMesageEncrypted}\n")

print("Alice: Let me decrypt it and get the info\n")

ServerAliceMessageDecrypted = decrypt(AliceServerKey, ServerAliceMessageEncrypted)
ServerAliceMessageDecrypted = re.split("ENC", ServerAliceMessageDecrypted)
print(f"Alice: Here's the info I got from the server for Bob: {ServerAliceMessageDecrypted[1]}, I will send this to Bob\n")
AliceFoundCK = ServerAliceMessageDecrypted[0].split("BOB")[0]
# print(AliceFoundCK)

AliceBobMessage = ServerAliceMessageDecrypted[1]

print(f"Bob: I received this message: {AliceBobMessage}, I will try to decrypt it\n")

AliceBobMessageDecrypted = decrypt(BobServerKey, AliceBobMessage).split("(ALICE)")

print("Bob: Looks like Alice is trying to communicate with me, let me send a nonce to verify that this isn't a replay attack. I expect to receive my nonce - 1 since that is standard\n")
BNonce = random.randint(1, 1000000)
BobAliceMessageBNonce  = encrypt(AliceBobMessageDecrypted[0], str(BNonce))

print(f"Alice: Here's an encrypted nonce from Bob {BobAliceMessageBNonce}, let me decrypt it and subtraact 1, then send back to Bob so he knows its me\n")

AliceDecryptBNonce = int(decrypt(str(ck), BobAliceMessageBNonce))
AliceEncryptBNonce1 = encrypt(str(ck), str(AliceDecryptBNonce - 1))


print(f"Bob: I received this from Alice, let me check if its my nonce - 1 when I decrypt. If so, It is a secure key\n")

BobDecryptAliceBNonce1 = decrypt(AliceBobMessageDecrypted[0], AliceEncryptBNonce1)

if int(BobDecryptAliceBNonce1) == (BNonce - 1):
    print("Bob: Decrypted successfuly, so it is secure!\n")
else:
    print("Bob: Didn't match the expected result, so I assume it is not secure\n")



