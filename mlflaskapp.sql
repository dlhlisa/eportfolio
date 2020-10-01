
CREATE TABLE blogs (
  id serial,
  title varchar(255) DEFAULT NULL,
  author varchar(100) DEFAULT NULL,
  body text,
  create_date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);

INSERT INTO blogs VALUES (2,'Article One','Lihua','1111','2020-09-17 16:24:49'),(3,'Article Two','Lihua','This is the example text for the first articles, you can edit or delete it later','2020-09-17 16:24:55'),(4,'Article 3','Lihua','This is the example text for the first articles, you can edit or delete it later','2020-09-17 16:24:57'),(5,'Article 4','Lihua','This is the example text for the first articles, you can edit or delete it later','2020-09-17 16:24:57'),(7,'Article One','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 22:23:47'),(8,'Article One','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 22:25:19'),(9,'Article One','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 22:26:37'),(10,'dddd','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 22:31:14'),(11,'11','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 22:53:55'),(12,'23','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 23:08:12'),(13,'cx','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 23:09:19'),(14,'An Example of a Google Bar Chart','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 23:18:57'),(15,'1An Example of a Google Bar Chart','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 23:20:56'),(16,'Article One jjj','Lihua','change ckeditor value and commit it back to mysql database','2020-09-18 23:23:07'),(18,'20150831','Lihua','接种吸附白喉破伤风联合疫苗及麻疹腮腺炎联合减毒活疫苗。','2020-09-19 23:08:35');


CREATE TABLE reviews (
  id serial,
  sentiment int DEFAULT NULL,
  date timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  review varchar(500) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  PRIMARY KEY (id)
);

INSERT INTO reviews VALUES (1,0,'2020-09-17 14:30:23','I don''t like this movie!',NULL),(2,0,'2020-09-17 14:30:37','I like this movie!',NULL),(3,0,'2020-09-17 14:37:55','this is another good movie.',NULL),(4,1,'2020-09-27 23:39:37','This is not related to the movie reviews',NULL),(5,0,'2020-09-27 23:45:19','Please enter your movie review',NULL),(6,1,'2020-09-30 20:17:49','I haven''t seen such a good movie for a long time.',NULL);


CREATE TABLE users (
  id serial,
  name varchar(45) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  username varchar(45) DEFAULT NULL,
  password varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users VALUES (1,'Lihua Deng','940429300@qq.com','Lihua','$5$rounds=535000$iH78mfvm.kC74FFG$5H2ohnhYOv8fi7LeBT4S79VRQar/hMS4KXI7mdM8.M3'),(2,'Lihua Deng','940429300@qq.com','Lihua','$5$rounds=535000$ohXMoA4VTZwqE4Mw$Yq4CpcBfuV7EJQwcP149/jRFFZDrdu6NBSf/7Vn6dg4'),(3,'Suxin Li','lisuxin38@163.com','Suxin Li','$5$rounds=535000$R6jP4yBrFOCjKiK2$19s2NVvmH4lmkLSAnW7/VH8JvjFfyPQ1YEqxOvYYGj6'),(4,'Yujiao Qu','quyujiao@outlook.com','Yujiao Qu','$5$rounds=535000$D9Ay/LIWLd8Lju/1$XNuJ7oFJ2oioIUKPs9HXBPXwDXsFnZRWgwnKN2DCIyB'),(5,'Jingzhen Ding','Jingzhen.ding@gmail.com','Jingzhen Ding','$5$rounds=535000$KL9K9wzdvSCtCoCe$e/XKBOLS06Iub1dcViTu9oCGkeOB4w9SuxROR8MI6zB'),(6,'Wanye Deng','745908989@qq.com','Wanye Deng','$5$rounds=535000$VZPV/pTAhNHvIB9g$kCBcRtD.7uzX6h7n.WIRT8zKNFg/UOzWGv7IoLuOEz6');
