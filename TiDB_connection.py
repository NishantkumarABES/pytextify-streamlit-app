from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


username = "2Q8jvwVEw3JhUQc.root"
password = "3iCmIOx4j0NGJTQy"
host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
port = 4000  
database_name = "test"
connect_timeout=300 


engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}",
    connect_args={
        'ssl': {'ca': 'ssl_cert.pem'},
        'connect_timeout': 20 
    },
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True  # Checks connection health before each query
)


Session = sessionmaker(bind=engine)
session = Session()

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
update_both = """
UPDATE users 
SET name = :name, email = :email 
WHERE username = :username
"""

update_name = """
UPDATE users 
SET name = :name 
WHERE username = :username
"""

update_email = """
UPDATE users 
SET email = :email 
WHERE username = :username
"""

update_uploads = """
UPDATE users
SET uploads = COALESCE(uploads, 0) + 1
WHERE username = :username;
"""
