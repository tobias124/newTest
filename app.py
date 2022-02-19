from website import create_app

# Dev Mode
dev = False

app = create_app(dev)

if __name__ == '__main__':
    app.run(debug=dev)
