# Ticketing System Preview

The app demonstrates a preview of how the ticketing application may work 

## Database Format
One database with two tables.

Database : aadb

Table 1 : auth


| Field         | Type         | Null | Key | Default | Extra          |
|---------------|--------------|------|-----|---------|----------------|
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| username      | varchar(32)  | YES  |     | NULL    |                |
| password_hash | varchar(128) | YES  |     | NULL    |                |



Table 2 : Sales

|     Field     | Type        | Null | Key | Default | Extra |
|---------------|-------------|------|-----|---------|-------|
| id            | int(3)      | YES  |     | NULL    |       |
| name          | varchar(30) | YES  |     | NULL    |       |
| reg_no        | varchar(20) | YES  |     | NULL    |       |
| mail_id       | varchar(30) | YES  |     | NULL    |       |
| mobile_no     | varchar(10) | YES  |     | NULL    |       |
| college       | varchar(30) | YES  |     | NULL    |       |
| pay_mode      | varchar(6)  | YES  |     | NULL    |       |
| location_sale | varchar(15) | YES  |     | NULL    |       |
| type          | varchar(15) | YES  |     | NULL    |       |
| pch_name      | varchar(20) | YES  |     | NULL    |       |


