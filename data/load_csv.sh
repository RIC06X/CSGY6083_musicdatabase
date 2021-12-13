USER_ID="hz2758"
USER_DB="hz2758_db"
files=(artist album song album_artist_map song_artist_map company artistowned _user artistsubscribed playlist playlistcreated playliststores rating ratingby)
for i in "${files[@]}"; do
    echo "$i"
    cat $PWD/$i.csv | psql -U $USER_ID -d $USER_DB -c "COPY $i from STDIN CSV HEADER"
done

