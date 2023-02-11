# cipher-X


The user inputted key is hashed using md5 hash algorithm and parity is adjusted.
The user inputted message is encypted and hidden inside a PNG image of choice using steganography(LSB technique).

In order to maintain the confidentiality of the data various approaches like cryptography and steganography may be used.
In this project we have encoded the text(location of the party) using 3DES encryption technique via Python’s Pycryptodome package.
Then to hide the ciphertext generated via 3DES, it is again encoded in an image using LSB based steganographic method for hiding the data 
by applying Least Significant Bit (LSB) algorithm for embedding the data into the images which is implemented through the Python pillow package

Whereas for decoding we take the encryption key used for 3DES from the user and convert it into bytes using md5 python package .
Then the byte converted key is made to go through DES parity checker .We extract cipher from image using LSB technique of image Steganography and decrypt
using the 3DES key.

The program also generates a nonce value mid encryption and concats it to message, which adds to data integrity as tampering can be identfied using nonce.

(note: the program supports only PNG images as an input whereas the out can be any desired format)
