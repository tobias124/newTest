from website import create_app

# Dev Mode
dev = True

app = create_app()

if __name__ == '__main__':
    if(dev):
        app.run(host="0.0.0.0", port=5000, debug=dev)
    else:
        app.run(debug=dev)
