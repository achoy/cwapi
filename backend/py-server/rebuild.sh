#! /bin/bash
export FLASK_APP=pyserver/pyserver.py
export FLASK_DEBUG=true
export FLASK_INFO=~/.py-server/pyserver.cfg
flask initdb
flask update
