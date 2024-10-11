from sqlalchemy import create_engine

username = "2Q8jvwVEw3JhUQc.root"
password = "3iCmIOx4j0NGJTQy"
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000  
database_name = "test"



engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}", 
                       connect_args={'ssl': {'ca': 'ssl_cert.pem'}})



user_table_query = """
CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) UNIQUE,
    `name` VARCHAR(255),
    `password` VARCHAR(255),
    `email` VARCHAR(255)
);
"""

insert_user_query = """
INSERT INTO users (username, name, password, email) VALUES (:username, :name, :password, :email)
"""
fetch_username_query = """
SELECT * FROM users WHERE username = :username
"""