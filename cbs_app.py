from CBS import create_app, db

cbs_app = create_app()

if __name__ == '__main__':
    with cbs_app.app_context():
        db.create_all()
    cbs_app.run(debug=True)
