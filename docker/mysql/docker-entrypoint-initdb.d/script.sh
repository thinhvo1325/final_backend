echo "** Creating default DB"

mysql -u root -proot --execute \
"CREATE DATABASE IF NOT EXISTS photo_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "** Finished creating default DB"
