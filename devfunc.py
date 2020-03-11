
#здесь выполняются функции устройств
import functions
import config
import json
import requests
import string
import other
import scene
path_devices = "devices.txt"
ifttt_token = config.ifttt_token
blynk_serv = config.blynk_ip

#Функция запроса списка устройств
def get_list_dev():
	list_dev = functions.read_list(path_devices)
	return (list_dev)


###############_РАЗДЕЛ ЗАПРОСА СПИСКА УСТРОЙСТВ_#############

#_____Блок обработки типов устройств ____Для списка устройств	
def return_capabilities(dev_type,dev_param,device_list_second):
	if dev_type == "выключатель":
		device_list_second = device_list_second+'{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.switch","capabilities":[{"type":"devices.capabilities.on_off","retrievable":true}],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]),str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
		device_list_second = device_list_second+','
	elif dev_type == "розетка":
		device_list_second = device_list_second+'{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.socket","capabilities":[{"type":"devices.capabilities.on_off","retrievable":true}],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]),str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
		device_list_second = device_list_second+','
	elif dev_type == "лампа":
		iftttornot=str(dev_param[9].replace("\"","")).lower()
		if iftttornot == "ifttt":
			device_list_second = device_list_second+'{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.light","capabilities":[{"type":"devices.capabilities.on_off","retrievable":true}],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]),str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
			device_list_second = device_list_second+','
		else:
			device_list_second = device_list_second+'{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.light","capabilities":[{"type": "devices.capabilities.range","retrievable": true,"parameters":{"instance":"brightness","random_access": true,"range":{"max": 100,"min": 1,"precision": 1},"unit": "unit.percent"}},{"type":"devices.capabilities.on_off","retrievable":true}],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]),str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
			device_list_second = device_list_second+','
	elif dev_type == "другое":
		device_list_second = device_list_second+other.other_dev_main(dev_param)
		device_list_second = device_list_second+','
	elif dev_type == "сцена":
		device_list_second = device_list_second+'{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.switch","capabilities":[{"type":"devices.capabilities.on_off","retrievable":true}],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]),str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
		device_list_second = device_list_second+','
	else:
		pass

	return device_list_second
#конец блока

#главная функция запроса списка устройств
def main_for_devs():
	list_dev = get_list_dev() #список строк из devices.txt
	tokenyandex = functions.token_get()
	request_id =functions.request_id_get()
	userid = functions.userid_get()
	test_token="Bearer "+tokenyandex
	device_list_first='{"request_id":"%s","payload":{"user_id":"%s","devices":[' % (request_id,userid)
	device_list_second = ""
	for str_dev in list_dev:
		str_lixt = functions.clean_text (str_dev)
		dev_param = str_lixt.split(",")
		dev_type = str(dev_param[8].replace("\"",""))
		dev_type = dev_type.lower()
		device_list_second = return_capabilities(dev_type,dev_param,device_list_second)
	device_list_second = device_list_second[0:(len(device_list_second)-1)] #убираем последнюю запятую
	dev_l_str = device_list_first+device_list_second+']}}'

	return dev_l_str

###############_КОНЕЦ РАЗДЕЛА ЗАПРОСА СПИСКА УСТРОЙСТВ_#############

###############_РАЗДЕЛ УПРАВЛЕНИЯ УСТРОЙСТВАМИ_#############

#функция выбора url (IFTTT, Blynk, Any) для лампы
def choise_but_url(dev_param,st_str):
	url_geton = "http://ya.ru"
	dev_ch_url = str(dev_param[9].replace("\"","")).lower()
	if dev_ch_url == "ifttt":#тут ок
		pass
	elif dev_ch_url == "blynk":#тут ок
		blynk_tok = str(dev_param[11].replace("\"",""))
		blynk_pin = str(dev_param[13].replace("\"",""))
		blynk_max = str(dev_param[14].replace("\"",""))
		val_br = str(st_str)
		val_br = str(round((blynk_max/100)*int(val_br)))
		url_geton = "http://%s/%s/update/%s?value=%s" % (blynk_serv,blynk_tok,blynk_pin,val_br)
	elif dev_ch_url == "any":
		stat_info = str(dev_param[12].replace("\"","")).lower()
		st_str_str = str(st_str)

		if stat_info == "status":
			any_max = str(dev_param[19].replace("\"",""))
			st_str_str = str(round((any_max/100)*int(st_str_str)))
			url_geton = str(dev_param[15]).replace("\"","").replace("--val--",st_str_str)
		else:
			any_max = str(dev_param[14].replace("\"",""))
			st_str_str = str(round((any_max/100)*int(st_str_str)))
			url_geton = str(dev_param[13]).replace("\"","").replace("--val--",st_str_str)
	else:
		pass
	return url_geton

#функция выбора url (IFTTT, Blynk, Any) для выключателя и розетки
def choise_url(dev_param):
	url_geton = "http://ya.ru"
	url_getoff = "http://ya.ru"
	dev_ch_url = str(dev_param[9].replace("\"","")).lower()
	if dev_ch_url == "ifttt":
		ifttt_huk_on = str(dev_param[10].replace("\"",""))
		ifttt_huk_off = str(dev_param[11].replace("\"",""))
		url_geton = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (ifttt_huk_on,ifttt_token)
		url_getoff = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (ifttt_huk_off,ifttt_token)
	elif dev_ch_url == "blynk":
		blynk_tok = str(dev_param[11].replace("\"",""))
		blynk_pin = str(dev_param[10].replace("\"",""))
		url_geton = "http://%s/%s/update/%s?value=1" % (blynk_serv,blynk_tok,blynk_pin)
		url_getoff = "http://%s/%s/update/%s?value=0" % (blynk_serv,blynk_tok,blynk_pin)
	elif dev_ch_url == "any":
		url_geton = str(dev_param[10]).replace("\"","")
		url_getoff = str(dev_param[11]).replace("\"","")
	else:
		pass
	return url_geton,url_getoff

#Функция выбора устройства
def test_dev_ctrl(dev_param,req_save,dev_id,num_dev):
	dev_type = str(dev_param[8].replace("\"","")).lower()
	if dev_type == "выключатель" or dev_type == "розетка":
		url_geton,url_getoff = choise_url(dev_param)
		st_str = str(req_save['payload']['devices'][num_dev]['capabilities'][0]['state']['value'])#request.json
		if "True" in str(st_str):
			response = requests.request("GET", url_geton)
		elif "False" in str(st_str):
			response = requests.request("GET", url_getoff)
		else:
			pass
		ctrl_second = '{"id": "%s","capabilities": [{"type": "devices.capabilities.on_off","state": {"instance": "on","action_result": {"status": "DONE"}}}]},' % dev_id
	elif dev_type == "лампа":
		url_geton,url_getoff = choise_url(dev_param)
		if "devices.capabilities.on_off" in str(req_save['payload']['devices']):
			st_str = str(req_save['payload']['devices'][num_dev]['capabilities'][0]['state']['value'])#request.json
			if "True" in str(st_str):
				response = requests.request("GET", url_geton)
			elif "False" in str(st_str):
				response = requests.request("GET", url_getoff)
			else:
				pass
			ctrl_second = '{"id": "%s","capabilities": [{"type": "devices.capabilities.on_off","state": {"instance": "on","action_result": {"status": "DONE"}}}]},' % dev_id
		else:
			st_str = int(req_save['payload']['devices'][num_dev]['capabilities'][0]['state']['value'])
			url_getonB = choise_but_url(dev_param,st_str)
			response = requests.request("GET", url_getonB)
			ctrl_second = '{"id": "%s","capabilities": [{"type": "devices.capabilities.range","state": {"instance": "brightness","action_result": {"status": "DONE"}}}]},' % (dev_id)
	elif dev_type == "другое":
		ctrl_second = other.control_other(dev_id,req_save,dev_param,num_dev)
	elif dev_type == "сцена":
		ctrl_second = scene.control_scene(dev_id,req_save,dev_param,num_dev)
	else:
		pass
	return ctrl_second


def main_for_control(req_save):
	list_dev = get_list_dev() #список строк из devices.txt
	request_id =functions.request_id_get()
	ctrl_list_first='{"request_id":"%s","payload":{"devices": [' % request_id
	ctrl_list_second = ""
	num_dev = 0
	for numstr in list_dev:
		for str_dev in list_dev:
			try:
				id_device = str(req_save['payload']['devices'][num_dev]['id'])
				dev_param = functions.clean_text (str_dev).split(",")
				dev_id = str(dev_param[0].replace("\"",""))
				if id_device == dev_id:
					ctrl_list_second_tmp = test_dev_ctrl(dev_param,req_save,dev_id,num_dev)
					ctrl_list_second = ctrl_list_second+ctrl_list_second_tmp
				else:
					pass
			except:
				pass
		num_dev = num_dev+1
	ctrl_list_second = ctrl_list_second[0:(len(ctrl_list_second)-1)]
	ctrl_str = ctrl_list_first+ctrl_list_second+']}}'
	print ("\nОтвет____ ",ctrl_str)

	return ctrl_str
	

###############_КОНЕЦ РАЗДЕЛА УПРАВЛЕНИЯ УСТРОЙСТВАМИ_#############

###############_РАЗДЕЛ ЗАПРОСА СОСТОЯНИЯ_#############
# функция проверки сервиса и запроса статуса (для выключателя)
def choise_status(dev_param,dev_id):
	url_stat = ""
	str_for_search = ""
	dev_ch_stat = str(dev_param[9].replace("\"","")).lower()
	if dev_ch_stat == "ifttt":
		url_stat = str(dev_param[13].replace("\"",""))
		str_for_search = str(dev_param[14].replace("\"",""))
	elif dev_ch_stat == "blynk":
		blynk_tok = str(dev_param[11].replace("\"",""))
		blynk_pin = str(dev_param[10].replace("\"",""))
		url_stat = 'http://%s/%s/get/%s' % (blynk_serv,blynk_tok,blynk_pin)
		str_for_search = "1"
	elif dev_ch_stat == "any":
		url_stat = str(dev_param[13].replace("\"",""))
		str_for_search = str(dev_param[14].replace("\"",""))
	else:
		pass
	response = requests.get(url_stat)
	response.encoding = 'utf-8'
	st_value = "false"
	if str_for_search in response.text:
		st_value = "true"
	else:
		st_value = "false"
	url_for_stat = '{"devices":[{"id":"%s","capabilities": [{"type": "devices.capabilities.on_off","state":{"instance": "on","value":%s}}]}]}}' % (dev_id,st_value)
	return url_for_stat

# функция проверки сервиса и запроса статуса (для лампы)
def choise_status_lamp(dev_param,dev_id):
	url_stat = ""
	str_for_search = ""
	dev_ch_stat = str(dev_param[9].replace("\"","")).lower()
	if dev_ch_stat == "ifttt":
		url_stat = str(dev_param[13].replace("\"",""))
		str_for_search = str(dev_param[14].replace("\"",""))
	elif dev_ch_stat == "blynk":
		blynk_tok = str(dev_param[11].replace("\"",""))
		blynk_pin = str(dev_param[10].replace("\"",""))
		url_stat = 'http://%s/%s/get/%s' % (blynk_serv,blynk_tok,blynk_pin)
		str_for_search = "1"
	elif dev_ch_stat == "any":
		url_stat = str(dev_param[13].replace("\"",""))
		str_for_search = str(dev_param[14].replace("\"",""))
	else:
		pass
	response = requests.get(url_stat)
	response.encoding = 'utf-8'
	st_value = "false"
	if str_for_search in response.text:
		st_value = "true"
	else:
		st_value = "false"
	#запрашиваем статус яркости
	if dev_ch_stat == "ifttt":
		val_brigh = 100
	elif dev_ch_stat == "blynk":
		blynk_tok = str(dev_param[11].replace("\"",""))
		pin_brigh = str(dev_param[13].replace("\"",""))
		blynk_max = str(dev_param[14].replace("\"",""))
		url_brigh = 'http://%s/%s/get/%s' % (blynk_serv,blynk_tok,pin_brigh)
		response = requests.get(url_brigh)
		response.encoding = 'utf-8'
		val_brigh = response.text
		for i in ["\"","[","]"]:
			val_brigh = val_brigh.replace(i,"")
		val_brigh = int(round((100/blynk_max)*int(val_brigh)))
	elif dev_ch_stat == "any":
		#тут ваяем проверку яркости с энидевайсом
		any_max = str(dev_param[19].replace("\"",""))
		url_brigh = str(dev_param[16].replace("\"",""))
		fst_str = str(dev_param[17])
		sec_str = str(dev_param[18])
		response = requests.get(url_brigh)
		response.encoding = 'utf-8'
		val_brigh = response.text
		indS = val_brigh.find(fst_str)+len(fst_str)
		indE = val_brigh.find(sec_str)
		val_brigh = int(val_brigh[indS:indE])
		val_brigh = int(round((100/any_max)*int(val_brigh)))
	else:
		pass
	url_for_stat = '{"devices":[{"id":"%s","capabilities": [{"type": "devices.capabilities.range","state": {"instance": "brightness","value": %s}},{"type": "devices.capabilities.on_off","state":{"instance": "on","value":%s}}]}]}}' % (dev_id,val_brigh,st_value)
	return url_for_stat

#функция проверки выбора устройства для статуса
def test_dev_stat(dev_param,req_save,dev_id):
	dev_type = str(dev_param[8].replace("\"","")).lower()
	if dev_type == "выключатель" or dev_type == "розетка":
		yesno = str(dev_param[12].replace("\"","")).lower()
		if yesno == "status":
			url_for_stat = choise_status(dev_param,dev_id)
		else:
			url_for_stat = '{"devices":[{"id":"%s","capabilities": [{"type": "devices.capabilities.on_off","state":{"instance": "on","value":false}}]}]}}' % dev_id
	elif dev_type == "лампа":
		yesno = str(dev_param[12].replace("\"","")).lower()
		if yesno == "status":
			url_for_stat = choise_status_lamp(dev_param,dev_id)
		else:
			url_for_stat = '{"devices":[{"id":"%s","capabilities": [{"type": "devices.capabilities.range","state": {"instance": "brightness","value": 100}},{"type": "devices.capabilities.on_off","state":{"instance": "on","value":false}}]}]}}' % dev_id
	elif dev_type == "другое":
		url_for_stat = other.status_other(dev_param,dev_id,req_save)
	elif dev_type == "сцена":
		url_for_stat = '{"devices":[{"id":"%s","capabilities": [{"type": "devices.capabilities.on_off","state":{"instance": "on","value":false}}]}]}}' % dev_id
	else:
		pass
	return url_for_stat


#главная функция запроса статуса устройства
def main_status_dev(req_save):
	request_id =functions.request_id_get()
	list_dev = get_list_dev()#список строк из devices.txt
	stat_list_first='{"request_id":"%s","payload":'% request_id
	stat_list_second = ""
	id_device = str(req_save['devices'][0]['id'])
	for str_dev in list_dev:
		dev_param = functions.clean_text (str_dev).split(",")
		dev_id = str(dev_param[0].replace("\"",""))
		if id_device == dev_id:
			stat_list_second = test_dev_stat(dev_param,req_save,dev_id)
		else:
			pass
	stat_str = stat_list_first+stat_list_second

	return stat_str

###############_КОНЕЦ РАЗДЕЛА ЗАПРОСА СОСТОЯНИЯ_#############

