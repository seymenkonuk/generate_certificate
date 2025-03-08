import requests
from helper.file import write_binary_file

def createQR(qr_data, img_path):
	api_url = f'https://api.qrserver.com/v1/create-qr-code/?data={qr_data}'
	response = requests.get(api_url)
	write_binary_file(img_path, response.content)
