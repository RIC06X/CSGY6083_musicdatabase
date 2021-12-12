USER_ID="yanjiexu"
USER_DB="demo"
files=(artist album song album_artist_map song_artist_map company artistowned _user artistsubscribed playlist playlistcreated playliststores rating ratingby)
for i in "${files[@]}"; do
    echo "$i"
    cat $PWD/data/$i.csv | psql -U $USER_ID -d $USER_DB -c "COPY $i from STDIN CSV HEADER"
done

