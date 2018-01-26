from flask import Flask, render_template, request, url_for, jsonify
import logging

logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

