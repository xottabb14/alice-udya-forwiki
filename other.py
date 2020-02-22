import functions
import config
import json
import requests
import string

ifttt_token = config.ifttt_token
blynk_serv = config.blynk_ip
llen = "devices.capabilities."



#вебхуки SEND
#дергаем вебхук IFTTT
def ifftt_send(hukname):
	url_get = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (hukname,ifttt_token)
	response = requests.request("GET", url_get)
#дергаем вебхук any
def any_send(url_any):
	response = requests.request("GET", url_any)
#дергаем вебхук any с параметром
def any_val_send(url_any,value_any):
	url_any = url_any.replace("--val--",value_any)
	response = requests.request("GET", url_any)
#дергаем вебхук blynk
def blynk_send(blynk_token,blynk_pin,blynk_value):
	url_get = "http://%s/%s/update/%s?value=%s" % (blynk_serv,blynk_token,blynk_pin,blynk_value)
	response = requests.request("GET", url_get)

#вебхуки GET
#any get all (получаем значение после запроса - строковое)
def any_get_all(url_any):
	response = requests.get(url_any)
	response.encoding = 'utf-8'
	val_brigh = response.text
	return val_brigh
#any get (получаем значение после запроса - строковое)
def any_get(url_any,indS,indE):
	response = requests.get(url_any)
	response.encoding = 'utf-8'
	val_brigh = response.text
	indSt = val_brigh.find(indS)+len(indS)
	indEn = val_brigh.find(indE)

	val_brigh = str(val_brigh[indSt:indEn])
	return val_brigh
#blynk get (получаем значение после запроса - строковое)
def blynk_get_val(blynk_token,blynk_pin):
	url_blynk = 'http://%s/%s/get/%s' % (blynk_serv,blynk_token,blynk_pin)
	response = requests.get(url_blynk)
	response.encoding = 'utf-8'
	val_blynk = response.text
	for i in ["\"","[","]"]:
		val_blynk = val_blynk.replace(i,"")
	return str(val_blynk)


#функция обработки умений из файла (описание устройства)
def other_dev_main(dev_param):
	first_part_str = '{"id":%s,"name":%s,"description":%s,"room":%s,"type":"devices.types.other","capabilities":[' % (str(dev_param[0]),str(dev_param[1]),str(dev_param[2]),str(dev_param[3]))
	file_capabil = str(dev_param[9].replace("\"",""))
	capabilities = functions.read_list(file_capabil)
	capabil_params =""
	for capab_str in capabilities:
		capab_str = functions.clean_text (capab_str)
		capab_list = capab_str.split(",")
		#тут проверяем умения
		if "on_off" in str(capab_list[0]):
			capabil_params = capabil_params+'{"type":"%son_off","retrievable":true},' % llen
		elif "toggle" in str(capab_list[0]):
			instance_str = str(capab_list[1])
			capabil_params = capabil_params+'{"type":"%stoggle","retrievable":true,"parameters":{"instance":%s}},' % (llen,instance_str)
		elif "range" in str(capab_list[0]):
			instance_str = str(capab_list[1])
			min_val = int(capab_list[2])
			max_val = int(capab_list[3])
			prec = int(capab_list[4])
			if "ifttt" in str(capab_list[5].replace("\"","")).lower():
				pass
			else:
				if "brightness" in instance_str or "open" in instance_str or "humidity" in instance_str:
					capabil_params = capabil_params+'{"type":"%srange","retrievable":true,"parameters":{"instance":%s,"random_access":true,"range":{"max":%s,"min":%s,"precision":%s},"unit":"unit.percent"}},' % (llen,instance_str,max_val,min_val,prec)
				elif "temperature" in instance_str:
					capabil_params = capabil_params+'{"type":"%srange","retrievable":true,"parameters":{"instance":%s,"random_access":true,"range":{"max":%s,"min":%s,"precision":%s},"unit":"unit.temperature.celsius"}},' % (llen,instance_str,max_val,min_val,prec)
				elif "channel" in instance_str or "volume" in instance_str:
					capabil_params = capabil_params+'{"type":"%srange","retrievable":true,"parameters":{"instance":%s,"random_access":true,"range":{"max":%s,"min":%s,"precision":%s}}},' % (llen,instance_str,max_val,min_val,prec)
				else:
					pass
		else:
			pass
	
	capabil_params = capabil_params[0:(len(capabil_params)-1)]
	third_path_str = '],"device_info":{"manufacturer":%s,"model":%s,"hw_version":%s,"sw_version":%s}}' % (str(dev_param[4]),str(dev_param[5]),str(dev_param[6]),str(dev_param[7]))
	
	all_str = first_part_str+capabil_params+third_path_str
	return all_str

#функция обработки статуса умений
def status_other(dev_param,dev_id,req_save):
	first_part_str = '{"devices":[{"id":"%s","capabilities": [' % dev_id
	file_capabil = str(dev_param[9].replace("\"",""))
	capabilities = functions.read_list(file_capabil)
	capabil_params =""

	for capab_str in capabilities: #для каждой строки в файле
		capab_str = functions.clean_text (capab_str)
		capab_list = capab_str.split(",")#разбиваем текущую строку на параметры

		if "on_off" in str(capab_list[0]):
			status_io = str(capab_list[4].replace("\"","")).lower() #статус или нет
			if "status" in status_io: #если статус
				if "blynk" in str(capab_list[1].replace("\"","")).lower():
					blynk_token = str(capab_list[3]).replace("\"","")
					blynk_pin = str(capab_list[2]).replace("\"","")
					current_val = blynk_get_val(blynk_token,blynk_pin)
					if "1" in current_val:
						st_value = "true"
					else:
						st_value = "false"
					
				else:#если ifttt или any
					url_any =  str(capab_list[5].replace("\"",""))
					current_val = any_get_all(url_any)
					str_for_search = str(capab_list[6].replace("\"",""))

					if str_for_search in current_val:
						st_value = "true"
					else:
						st_value = "false"
				capabil_params = capabil_params+'{"type":"%son_off","state":{"instance":"on","value":%s}},' % (llen,st_value)
			else:
				capabil_params = capabil_params+'{"type":"%son_off","state":{"instance":"on","value":false}},' % llen

		elif "toggle" in str(capab_list[0]):
			instance_str = str(capab_list[1])
			if "blynk" in str(capab_list[2].replace("\"","")).lower():
				status_io = str(capab_list[5].replace("\"","")).lower() #статус или нет
			else:
				status_io = str(capab_list[4].replace("\"","")).lower() #статус или нет
			if "status" in status_io: #если статус
				if "blynk" in str(capab_list[2].replace("\"","")).lower():
					blynk_token = str(capab_list[4]).replace("\"","")
					blynk_pin = str(capab_list[3]).replace("\"","")
					current_val = blynk_get_val(blynk_token,blynk_pin)
					if "1" in current_val:
						st_value = "true"
					else:
						st_value = "false"
					
				else:#если ifttt или any
					url_any =  str(capab_list[5].replace("\"",""))
					current_val = any_get_all(url_any)
					str_for_search = str(capab_list[6].replace("\"",""))
					if str_for_search in current_val:
						st_value = "true"
					else:
						st_value = "false" 
				capabil_params = capabil_params+'{"type":"%stoggle","state":{"instance":%s,"value":%s}},' % (llen,instance_str,st_value)
			else:
				capabil_params = capabil_params+'{"type":"%stoggle","state":{"instance":%s,"value":false}},' % (llen,instance_str)
		elif "range" in str(capab_list[0]):
			instance_str = str(capab_list[1])
			if "blynk" in str(capab_list[5].replace("\"","")).lower():
				status_io = str(capab_list[8].replace("\"","")).lower() #статус или нет
			else:
				status_io = str(capab_list[7].replace("\"","")).lower() #статус или нет

			if "status" in status_io: #если статус
				if "ifttt" in str(capab_list[5].replace("\"","")).lower():
					pass #не поддерживается
				elif "blynk" in str(capab_list[5].replace("\"","")).lower():
					blynk_token = str(capab_list[7]).replace("\"","")
					blynk_pin = str(capab_list[6]).replace("\"","")
					current_val = blynk_get_val(blynk_token,blynk_pin)

					capabil_params = capabil_params+'{"type":"%srange","state":{"instance":%s,"value":%s}},' % (llen,instance_str,current_val)
				elif "any" in str(capab_list[5].replace("\"","")).lower():

					url_any =  str(capab_list[8].replace("\"",""))
					indS = str(capab_list[9])
					indE = str(capab_list[10])

					current_val = any_get(url_any,indS,indE)
					capabil_params = capabil_params+'{"type":"%srange","state":{"instance":%s,"value":%s}},' % (llen,instance_str,current_val)
				else:

					val_rang = 100
					capabil_params = capabil_params+'{"type":"%srange","state":{"instance":%s,"value":%s}},' % (llen,instance_str,val_rang)
			else:

				val_rang = 100
				capabil_params = capabil_params+'{"type":"%srange","state":{"instance":%s,"value":%s}},' % (llen,instance_str,val_rang)
		else:
			pass
	capabil_params = capabil_params[0:(len(capabil_params)-1)]
	third_path_str =']}]}}' 
	all_str = first_part_str+capabil_params+third_path_str
	return all_str


#функция управления
def control_other(dev_id,req_save,dev_param):
	file_capabil = str(dev_param[9].replace("\"","")) #файл с конфигом умений
	capabilities = functions.read_list(file_capabil) #список строк умений из файла
	#текущий интенс из запроса
	intence_cur = str(req_save['payload']['devices'][0]['capabilities'][0]['state']['instance'])#'"on"'
	#тип умения из запроса. Например: devices.capabilities.on_off
	type_capability = str(req_save['payload']['devices'][0]['capabilities'][0]['type'])
	#проверяем on_off и шлем хук
	if "devices.capabilities.on_off" in type_capability:
		#текущее значение интенса. Например - 50
		resp_val = str(req_save['payload']['devices'][0]['capabilities'][0]['state']['value'])
		for capabil in capabilities: #для каждой строки в файле

			capabil_list = functions.clean_text (str(capabil)).split(",")#чистим от энтеров и делим параметры на список
			test_capabil = "devices.capabilities."+str(capabil_list[0])
			test_capabil = test_capabil.replace("\"","")#строка для сравнения с полученным типом умения
			if type_capability in test_capabil: #если тип умнеия есть в текущей строке файла
				if "ifttt" in str(capabil_list[1].replace("\"","")).lower(): #если ifttt
					huk_on = str(capabil_list[2]).replace("\"","")
					huk_off = str(capabil_list[3]).replace("\"","")
					if "True" in str(resp_val):
						ifftt_send(huk_on)
					if "False" in str(resp_val):
						ifftt_send(huk_off)
					else:
						pass
				elif "blynk" in str(capabil_list[1].replace("\"","")).lower():
					blynk_token = str(capabil_list[3]).replace("\"","")
					blynk_pin = str(capabil_list[2]).replace("\"","")
					on_val = "1"
					off_val = "0"

					if "True" in str(resp_val):
						blynk_send(blynk_token,blynk_pin,on_val)
					if "False" in str(resp_val):
						blynk_send(blynk_token,blynk_pin,off_val)
					else:
						pass
				elif "any" in str(capabil_list[1].replace("\"","")).lower():
					url_any_on = str(capabil_list[2]).replace("\"","")
					url_any_off = str(capabil_list[3]).replace("\"","")
					if "True" in str(resp_val):
						any_send(url_any_on)
					if "False" in str(resp_val):
						any_send(url_any_off)
					else:
						pass	
				else:
					pass

			else:
				pass		
		all_str = '{"devices":[{"id":"%s","capabilities":[{"type":"devices.capabilities.on_off","state":{"instance":"%s","action_result": {"status": "DONE"}}}]}]}}' % (dev_id,intence_cur)
		
	if "devices.capabilities.toggle" in type_capability:
		for capabil in capabilities: #для каждой строки в файле
			capabil_list = functions.clean_text(str(capabil)).split(",")
			test_intance = str(capabil_list[1])
			test_intance = test_intance.replace("\"","")
			if test_intance in intence_cur: 
				if "ifttt" in str(capabil_list[2].replace("\"","")).lower():
					huk_on = str(capabil_list[3]).replace("\"","")
					ifftt_send(huk_on)
				elif "blynk" in str(capabil_list[2].replace("\"","")).lower():
					blynk_token = str(capabil_list[4]).replace("\"","")
					blynk_pin = str(capabil_list[3]).replace("\"","")
					on_val = "1"
					blynk_send(blynk_token,blynk_pin,on_val)
				elif "any" in str(capabil_list[2].replace("\"","")).lower():
					url_any_on = str(capabil_list[3]).replace("\"","")
					any_send(url_any_on)
				else:
					pass
		all_str = '{"devices":[{"id":"%s","capabilities":[{"type":"devices.capabilities.toggle","state":{"instance":"%s","action_result": {"status": "DONE"}}}]}]}}' % (dev_id,intence_cur)

	if "devices.capabilities.range" in type_capability:
		#текущее значение интенса. Например - 50.
		resp_val = str(req_save['payload']['devices'][0]['capabilities'][0]['state']['value'])
		for capabil in capabilities:#для каждой строки в файле
			capabil_list = functions.clean_text(str(capabil)).split(",")
			test_intance = str(capabil_list[1])
			test_intance = test_intance.replace("\"","")
			if test_intance in intence_cur: #если совпадают названия интенсов
				if "ifttt" in str(capabil_list[5].replace("\"","")).lower():
					pass
				elif "blynk" in str(capabil_list[5].replace("\"","")).lower():
					blynk_token = str(capabil_list[7]).replace("\"","")
					blynk_pin = str(capabil_list[6]).replace("\"","")
					on_val = str(resp_val)

					blynk_send(blynk_token,blynk_pin,on_val)
				elif "any" in str(capabil_list[5].replace("\"","")).lower():
					url_any_on = str(capabil_list[6]).replace("\"","")
					value_any = str(resp_val)

					any_val_send(url_any_on,value_any)
				else:
					pass
		all_str = '{"devices":[{"id":"%s","capabilities":[{"type":"devices.capabilities.range","state":{"instance":"%s","action_result": {"status": "DONE"}}}]}]}}' % (dev_id,intence_cur)
	else:
		pass
	return all_str
