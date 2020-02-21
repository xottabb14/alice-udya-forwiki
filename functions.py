import random
import config

generatestr="ABCDEFGHJIKLMNOPQRSTUVWXYZ1234567890abcdefghjklmnopqrstuvwxyz"
path_token="/tmp/t.token"
path_code="/tmp/c.code"
path_userid = "/tmp/user.id"
#запись строки в файл
def write_str(strcur,filename):
    f = open(filename, "w+", encoding = "utf-8")
    temp_string = f.write(strcur)
    f.close()

#читаем несколько строк из файла
def read_list(filename):
	f = open(filename, "r", encoding = "utf-8")
	temp_string = list(f)
	f.close()
	return temp_string

#читаем строку из файла
def read_str(filename):
	f = open(filename, "r", encoding = "utf-8")
	temp_string = f.read()
	f.close()
	return temp_string

def clean_text (text):
			if not isinstance(text, str):
				raise TypeError('Это не текст')
			for i in ['\n']:
				text = text.replace(i,'')
			return text	

#проверяем token
def token_get():
	try:
		tokenyandex = read_str(path_token)
	except:
		tokenyandex=""
		i=0
		while i != 30:
			tokenyandex=tokenyandex+generatestr[random.randint(0,(len(generatestr)-1))]
			i=i+1
		write_str(tokenyandex,path_token)
	return tokenyandex

#проверяем code
def code_get():
	try:
		codeyandex = read_str(path_code)
	except:
		codeyandex = ""
		i=0
		while i != 30:
			codeyandex=codeyandex+generatestr[random.randint(0,(len(generatestr)-1))]
			i=i+1
		write_str(codeyandex,path_code)
	return codeyandex

#проверяем userid
def userid_get():
	try:
		userid = read_str(path_userid)+"-"
	except:
		userid = config.userid
		i=0
		while i != 10:
			userid=userid+generatestr[random.randint(0,(len(generatestr)-1))]
			i=i+1
		write_str(userid,path_userid)
	return userid

#получаем request_id
def request_id_get():
	request_id = ""
	i=0
	while i != 40:
		request_id=request_id+generatestr[random.randint(0,(len(generatestr)-1))]
		i=i+1
	return request_id