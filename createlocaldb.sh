#!/bin/bash

# Verify if Postgres is installed
if ! type "psql" > /dev/null; then
    echo "Postgres is not installed."
    printf "To install:\t sudo apt-get install postgresql (depends of distro)\n"
    echo "Then excute this script again"
fi

echo "Introduce your password..."
sudo echo "Password introduced."

echo "Configuring local data base..."

printf "\nDropping database if exists...\n"
sudo -u postgres psql << EOF
drop database if exists alumnusb_db; 
\q
EOF

printf "\nCreating data base user\n"
sudo -u postgres createuser alumnusb_admin
echo "User created: alumnusb_admin"

printf "\nCreating data base\n"
sudo -u postgres createdb alumnusb_db
echo "Created data base: alumnusb_db" 

printf "\nAssigning privileges in the data base\n"
sudo -u postgres psql << EOF
alter user alumnusb_admin with encrypted password 'qwerqwer'; 
grant all privileges on database alumnusb_db to alumnusb_admin;
\q
EOF
echo "Assigned privileges"
echo "¡Created data base!"
