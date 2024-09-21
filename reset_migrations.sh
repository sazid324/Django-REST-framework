# Delete old migrations
rm -f authentication/migrations/0*
rm -f authorization/migrations/0*
rm -f filesystem/migrations/0*

# Make migrations
echo "Making migrations..."
python manage.py makemigrations

# Migrate database
echo "Migrating database..."
python manage.py migrate

echo "Reset completed."
