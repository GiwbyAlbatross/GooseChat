#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-module-docstring,missing-function-docstring
#
#  main.py
#  
#  Copyright 2025 GiwbyAlbatross
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR ANY PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details. If you can find one :)
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 

from flask import Flask, request, Response, redirect
from goosechat import entry, markup, auth

app = Flask(__name__)
HIDDEN_PASSWORDS = {'admin', 'root', 'giwby', 'herobrine'}

@app.route('/')
def index_page():
    return redirect('/chat/default')
@app.route('/style.css')
def get_stylesheet():
    return Response(markup.readfrom('static/style.css'), mimetype='text/css')
@app.route('/backend/time_conversion.js')
def get_timeconverter():
    return Response(markup.readfrom('static/time_conversion.js'), mimetype='text/javascript')

@app.route('/chat/<name>/', methods=['GET', 'POST'])
def chat_page(name):
    # TODO:
    # - implement different chats based on name
    # - ...
    if request.method == 'GET':
        # render chat
        entries = entry.get_entries()
        #print("Entries:", entries)
        return markup.render_basic_template('Chat: '+name,
                                            markup.render_chat(
                                                entries
                                                )
                                            )
        #"""
        return "NotImplemented<br><br><hr>Coming soon!"
    elif request.method == 'POST':
        # post to chat
        user  = request.cookies.get('username', 'guest').strip() # fixes a bug my sister found...
        legit = request.cookies.get('legit', 'False')
        msg   = request.form.get('msg')
        print(f"Adding message {msg!r} from user {user!r}. Cookies: {request.cookies!r}")
        entry.add_msg(msg, user, legit=legit)
        return redirect("/chat/"+name)
    else:
        return "NotImplemented"

@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return markup.render_basic_template('Log in to GooseChat', markup.readfrom('static/login.html'))
    elif request.method == 'POST':
        username = request.form.get('username').strip(' ')
        password = auth.encodepass(request.form.get('passwd'))
        if username not in HIDDEN_PASSWORDS:
            print(f"Loggin in with username: {username!r} password: {password!r}")
        #print("Received and encoded username and password")
        resp = Response('<script>location.pathname="/";</script>')
        legit = 'False'
        #resp.set_cookie('legit', 'False')
        #print("Checking password")
        if not auth.check_pass(username, password):
            #print("Password wrong")
            if auth.add_pass(username, password) == auth.EnumPasswdUpdateStatus.CHANGE:
                #print("Wrong password, impostor user")
                pass
            else:
                #print("Set new password")
                #resp.set_cookie('legit', 'True')
                legit = 'True'
        else:
            #print("Password correct")
            #resp.set_cookie('legit', 'True')
            legit = 'True'
        resp.set_cookie('legit', legit)
        resp.set_cookie('username', username)
        return resp

if __name__ == '__main__':
    app.run('0.0.0.0', debug=False, threaded=True)

###############
# GISLEBURTUS #
#  HOC FECIT  #
###############
