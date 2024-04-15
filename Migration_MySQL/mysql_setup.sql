create database simplywealth_app;

CREATE USER 'python-backend'@'%' IDENTIFIED BY 'thisisthepassword';

GRANT ALL PRIVILEGES ON simplywealth_app.* TO 'python-backend'@'%';
