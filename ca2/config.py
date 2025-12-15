import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


'''class Config:
    SECRET_KEY = "supersecretkey"
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql://finance_user:StrongPassword123@localhost/finance_app"
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://finance_user:StrongPassword123@localhost/finance_app"
    )'''




class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Comment out MySQL:
    # SQLALCHEMY_DATABASE_URI = (
    #     "mysql+pymysql://finance_user:StrongPassword123@localhost/finance_app"
    # )

    # Use SQLite (file-based DB in your project folder)
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance_app.db"
