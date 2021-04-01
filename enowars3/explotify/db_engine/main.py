from eve import Eve
app = Eve(settings="settings.py")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)