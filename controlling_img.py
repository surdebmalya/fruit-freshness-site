import os, requests, base64, random
import vars

def upload_img_to_server(local_img_name):
	try:
		## Host ticket on Imgbb
		with open(local_img_name, "rb") as file:
			payload = {
			"key": vars.API_KEY,
			"image": base64.b64encode(file.read()),
			}
			res = requests.post(vars.URL_API, payload)
			link_of_the_img = res.json()['data']['url']

			return 'DONE', link_of_the_img
	except:
		return 'ERROR', 'ERROR'

def remove_local_pic(local_img_full_path):
	try:
		os.remove(local_img_full_path)
	except:
		pass

def checking_existense_of_file(total_name_generated, base_path):
	base_dir_files = os.listdir(base_path)
	for each_file_name in base_dir_files:
		if each_file_name.lower() == total_name_generated:
			return False
	return True

def load_url_local(base_path, img_link): # img_link: URL
	try:
		FLAG = True
		while FLAG:
			name = random.randint(1, 1000000)
			total_name = str(name)+'.jpg'
			total_path = os.path.join(base_path, total_name)
			result = checking_existense_of_file(
				total_name, 
				base_path
			)
			if result:
				# not exsists
				FLAG = False
		f = open(total_path,'wb')
		f.write(requests.get(img_link).content)
		f.close()
		return 'Success', total_path
	except:
		return 'ERROR', 'ERROR'