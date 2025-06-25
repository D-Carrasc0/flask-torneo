from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
import requests

login_bp = Blueprint('login', __name__)

API_BASE_URL = 'http://localhost:4000/api' 

@login_bp.route('/')
def formulario_login():
    return render_template('login.html')
