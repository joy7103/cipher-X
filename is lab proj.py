import time

from PIL import Image
import Crypto
from Crypto.Cipher import DES3

from hashlib import md5


shorthand='$$$$#+++$$$$#'        #here shorthand has been used to seperate nonce and cipher text values which are encoded in steganography

print('\n\n Hi welcome to Xipher_base !\n\nlet us start the project!')
kin=input("\n\nEnter the key you will be using for 3DES(encryption/decryption)    \n")
k=md5(kin.encode('ascii')).digest()

key = DES3.adjust_key_parity(k)


def encrypt_des(msg):
    cipher = DES3.new(key, DES3.MODE_EAX)
    nonce = cipher.nonce
    ciphertext = cipher.encrypt(msg.encode('ascii'))
    return nonce, ciphertext

def decrypt_des(nonce, ciphertext):
    cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    #print("\n\n\n\n\n")
    #print(plaintext)
    return plaintext.decode('ascii')


def genData(data):

	
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):


        

		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

	
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):


		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1


def estag(message):
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = message
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	

	new_img_name = input("Enter the name of new image(with extension) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    
	print('\nOpening the new image with cipher encoded inside ........')

	time.sleep(3)

	im = Image.open(new_img_name) 
	im.show()


def dstag():
	img = input("Enter image name(with extension) : ")
	image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data
        
        
def decode():
    
    cip=dstag()
    
    print("\n printin cip val ",cip)
    m=len(shorthand)

    text=""
    nonce=""

    for i in range(0,len(cip)-m+1):
        if cip[i:i+m]==shorthand:
           text=cip[:i]
           nonce=cip[i+m:]
    
    
    print(text)
    print(nonce)
    
    lp=bytes(text, 'ISO-8859-1')
    mp=bytes(nonce, 'ISO-8859-1')
    
    print(lp)
    print(mp)
    
    plaintext=decrypt_des(mp,lp)
    return plaintext
    
    
    
    
def encode():
    
    nonce, ciphertext = encrypt_des(input('Enter a message: '))
    
    print("the cipher text ",ciphertext)
    print("\n nonce value is", nonce)
    
    message_text=str(ciphertext, 'ISO-8859-1')
    message_nonce=str(nonce, 'ISO-8859-1')
    
    print("\n converted cipher is ",message_text)
    #print("\n converted nonce is",message_nonce)
    
    message=message_text+shorthand+message_nonce
    print("\n final message is ",message)
    estag(message)
    
    
    


# Main Function
def main():
	a = int(input(":: What is your need ::\n\n"
						"1. Encode the message\n2. Decode the message\n\n"))
	if (a == 1):
		encode()
		print("\n\n\nmessage has been encoded inside image \nprogram terminated......")

	elif (a == 2):
		print("The decoded text is    :   " + decode())
	else:
		raise Exception("Enter correct input")

# Driver Code
if __name__ == '__main__' :

	# Calling main function
	main()