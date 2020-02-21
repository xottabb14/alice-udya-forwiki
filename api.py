# coding: utf-8
# Импортирует поддержку UTF-8.
#from __future__ import unicode_literals
import json
import logging
import flask
from flask_json import FlaskJSON, JsonError, json_response
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request, redirect
from flask import jsonify
import requests
import config
import functions
import devfunc


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
# Хранилище данных о сессиях.
sessionStorage = {}

#endpoint
@app.route("/v1.0", methods=['HEAD'])
def head_endpoint():
    resp.headers['Content-Type'] = 'text/html'
    return resp
#отвязка аккаунта
@app.route("/v1.0/user/unlink", methods=['POST'])
def unlink():
    resp.headers['Content-Type'] = 'text/html'
    return resp
#выдача токена яндексу
@app.route("/token", methods=['POST'])
def tokenn():
    tokenyandex = functions.token_get()
    return jsonify (access_token=tokenyandex,token_type="bearer",expires_in=2592000,refresh_token=tokenyandex)#2592000

#обновление токена яндексу
@app.route("/refresh", methods=['POST'])
def refresh():
    tokenyandex = functions.token_get()
    return jsonify (access_token=tokenyandex,token_type="bearer",expires_in=2592000,refresh_token=tokenyandex)

# OAuth
@app.route("/", methods=['GET'])
def main():
    client_id = str(request.args['client_id'])
    scope = str(request.args['scope'])#"read,home:lights"
    state = str(request.args['state'])
    code = functions.code_get()
    redirect_uri = str(request.args['redirect_uri'])
    url_par = redirect_uri+'?code='+code+'&state='+state+'&client_id='+client_id+'&scope='+scope
    return redirect(url_par)

#возвращаем список устройств
@app.route("/v1.0/user/devices", methods=['GET'])
def devices():
    tokenyandex = functions.token_get()
    test_token="Bearer "+tokenyandex
    device_list=devfunc.main_for_devs() #запрашиваем список устройств
    return device_list
 
 #Делаем действие и отправляем отчет
@app.route("/v1.0/user/devices/action", methods=['GET','POST'])
def action():
    req_save = request.json
    answ = devfunc.main_for_control(req_save)
    return answ
#Запрашиваем состояние устройств
@app.route("/v1.0/user/devices/query", methods=['GET','POST'])
def query():
    req_save = request.json
    answ = devfunc.main_status_dev(req_save)
    return answ
