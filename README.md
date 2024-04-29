# MATH367-Project
# Alex Murphy

# Authentication for Large Networks: Needham-Schroeder and Wide-Mouth Frog Protocols
This repository contains python files simulating the Needham-Schroeder Authentication Protocols using both symmetric key and public key encryption schemes, as well as the Wide-Mouth Frog Authentication Protocol.

There are 4 python files included in this repository:
- RSA.py: Contains all the required functions for RSA Encryption. The default is set ot use keys of 10 bits in length
- Needham-Schroeder-Symmetric.py: Simulates the Needham-Schroeder Authentication Protocol using symmetric key encryption and a Vignere cipher
- Needham-Schroeder-Public.py: Simulates the Needham-Schroeder Authentication Protocol using public keys and the RSA encryption scheme (implemented using the provided RSA.py file)
- Wide-Mouth-Example.py: Simulates the Wide-Mouth Frog Authentication Protocol using symmetric key encryption with a Vignere cipher

## Requirements:
- Python 3.8 or later

## Usage:
To run the simulate authentication protocols:
1. Navigate to the project directory
2. Run the command for the dedicated script:
    - For Needham-Schroeder Symmetric Key:
        python Needham-Schroeder-Example.py
    - For Needham-Schroeder Public Key:
        python Needham-Schroeder-Public.py
    - For Wide-Mouth Frog Authentication:
        python Wide-Mouth-Frog-Example.py