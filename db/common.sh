# Some common shell stuff.

echo "Importing from common.sh"

DB=restaurantDB
USER=jw6680
CONNECT_STR="mongodb+srv://food-finder.ltqe7ym.mongodb.net/"
if [ -z $DATA_DIR ]
then
    DATA_DIR=/Users/jialinweng/Food-Finder/db
fi
BKUP_DIR=$DATA_DIR/bkup
EXP=/opt/homebrew/bin/mongoexport
IMP=/opt/homebrew/bin/mongoimport

# if [ -z $MONGO_PASSWD ]
# then
#     echo "You must set MONGO_PASSWD in your env before running this script."
#     exit 1
# fi


declare -a Collections=("restaurants" "reservations" "menus" "ratings" "users")