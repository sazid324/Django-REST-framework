# Ensure the script exits on any error
set -e

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Define Docker image versions from environment variables
VERSION_API=${DOCKER_IMAGE_VERSION_API:-latest}
VERSION_DB=${DOCKER_IMAGE_VERSION_DB:-latest}

# pull docker images from registry
docker pull registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API
docker pull registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB

# tag pulled images
docker tag registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API tolhub-api:$VERSION_API
docker tag registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB mysql:$VERSION_DB

# remove pulled images
docker rmi registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API
docker rmi registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB

echo "Script completed."
