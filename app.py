from website import create_app

# Dev Mode
dev = True

app = create_app()

if __name__ == '__main__':
    app.run(debug=dev)
