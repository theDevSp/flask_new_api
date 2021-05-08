from application import init_app

app = init_app()

if __name__ == "__main__":
    
    app.run(port=5000, debug=True)