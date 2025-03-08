import string
import random

# RASTGELE ID ÜRETİR
def generateId(length):
	characters = string.ascii_letters + string.digits
	result = ""
	for _ in range(length):
		result += random.choice(characters)
	return result

# BENZERSİZ ID ÜRETİR
# Açıklama: ids dizisinde olmayan bir id üretir
def generateUniqueId(length, ids):
	while True:
		id = generateId(length)
		if id not in ids:
			return id
