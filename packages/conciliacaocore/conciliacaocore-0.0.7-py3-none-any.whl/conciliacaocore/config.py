class Config:
    DB_HOST = None
    DB_NAME = None
    DB_USER = None
    DB_PASSWORD = None

    @classmethod
    def init_config(cls, db_host, db_name, db_user, db_password):
        cls.DB_HOST = db_host
        cls.DB_NAME = db_name
        cls.DB_USER = db_user
        cls.DB_PASSWORD = db_password
