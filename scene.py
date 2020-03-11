import functions
import config
import json
import requests
import string

llen = "devices.capabilities."

#вебхуки SEND
#дергаем вебхук any
def any_send(url_any):
	response = requests.request("GET", url_any)

#функция управления
def control_scene(dev_id,req_save,dev_param,num_dev):
	file_capabil = str(dev_param[9].replace("\"","")) #файл с конфигом сценария
	capabilities = functions.read_list(file_capabil) #список строк умений из файла
	#текущий интенс из запроса
	intence_cur = str(req_save['payload']['devices'][num_dev]['capabilities'][0]['state']['instance'])#'"on"'
	resp_val = str(req_save['payload']['devices'][num_dev]['capabilities'][0]['state']['value'])
	for capabil in capabilities: #для каждой строки в файле
		capabilstr = (functions.clean_text(str(capabil))).replace("\"","")#чистим от энтеров и кавычек
		url_any_on = str(capabilstr)
		if "True" in str(resp_val):
			any_send(url_any_on)
		else:
			pass	
	all_str = '{"id":"%s","capabilities":[{"type":"devices.capabilities.on_off","state":{"instance":"on","action_result": {"status": "DONE"}}}]},' % dev_id
	return all_str
