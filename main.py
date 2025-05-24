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
from goosechat import entry, markup

app = Flask(__name__)

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
        user = request.cookies.get('username', 'guest')
        msg  = request.form.get('msg')
        print(f"Adding message {msg!r} from user {user!r}")
        entry.add_msg(msg, user)
        return redirect("/chat/"+name)
    else:
        return "NotImplemented"

if __name__ == '__main__':
    app.run('0.0.0.0', debug=__debug__, threaded=True)