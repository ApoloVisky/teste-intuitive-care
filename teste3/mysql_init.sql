SET GLOBAL max_allowed_packet=1073741824;
SET GLOBAL innodb_buffer_pool_size=536870912;
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));