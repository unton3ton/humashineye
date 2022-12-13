from hashlib import sha256

file = open("norma1_1.png", "rb") 
hash1 = sha256(file.read()).hexdigest() 
file.close()

file = open("speckled_1.png", "rb") 
hash2 = sha256(file.read()).hexdigest() 
file.close()

print(f"The hashs of my files is: {hash1} and {hash2}")

file = open("result_1.png", "rb") 
hash3 = sha256(file.read()).hexdigest() 
file.close()

print(f"The hash of result (dif-img) is: {hash3}")