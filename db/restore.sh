#!/bin/bash
# Script to backup production database to JSON files.

. ./common.sh

for collection in ${Collections[@]}; do
    echo "Restoring $collection"
    $IMP --db=$DB --collection $collection --drop --file $BKUP_DIR/$collection.json
done