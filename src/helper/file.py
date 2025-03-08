import json
import os
import csv
import configparser

# DOSYAYI SİLER
def remove_file(path):
	try:
		if os.path.exists(path):
			os.remove(path)
	except:
		pass

# DOSYANIN İÇERİĞİNİ OKUR
def read_file(path):
	with open(path, "r", encoding="utf-8") as file:
		content = file.read()
	return content

# DOSYAYA YAZAR
def write_file(path, content):
	with open(path, "w", encoding="utf-8") as file:
		file.write(content)

# İKİLİ DOSYAYI OKUR
def read_binary_file(path):
	with open(path, "rb") as file:
		content = file.read()
	return content.decode("utf-8")

# İKİLİ DOSYAYA YAZAR
def write_binary_file(path, content):
	with open(path, "wb") as file:
		file.write(content)

# JSON DOSYASINI OKUR
def read_json_file(path):
	with open(path, "r", encoding="utf-8") as file:
		content = json.load(file)
	return content

# JSON DATA'YI JSON DOSYASINA YAZAR
def write_json_file(path, json_data):
	with open(path, "w", encoding="utf-8") as file:
		file.write(json.dumps(json_data, indent=4))

# CONF DOSYASINI OKUR
def read_conf_file(path):
	config = configparser.ConfigParser()
	config.optionxform = str
	config.read(path)
	return config

# TSV DOSYASINI OKUR
def read_tsv_file(path):
	with open(path, mode='r', newline='', encoding='utf-8') as file:
		reader = csv.DictReader(file, delimiter='\t')
		for row in reader:
			yield row

# LST DOSYASINI OKUR
def read_lst_file(path):
	with open(path, "r") as file:
		return file.read().splitlines()

# LST DOSYASINI YAZAR
def write_lst_file(path, lst_data):
	with open(path, "w") as file:
		for row in lst_data:
			file.write(row + "\n")

# LST DOSYASINI EKLER
def append_lst_file(path, lst_data):
	with open(path, "a") as file:
		for row in lst_data:
			file.write(row + "\n")
