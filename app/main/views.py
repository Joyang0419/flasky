from flask import render_template
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    """首頁"""
    return render_template('index.html')
