# Ensure the script exits on any error
set -e

# Load environment variables from .env file
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Define Docker image versions from environment variables
VERSION_API=${DOCKER_IMAGE_VERSION_API:-latest}
VERSION_DB=${DOCKER_IMAGE_VERSION_DB:-latest}

# tag already existing image with new tag
docker tag tolhub-api:$VERSION_API registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API
docker tag mysql:$VERSION_DB registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB

# push to registry
docker push registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API
docker push registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB

# remove tagged images
docker rmi registry.gitlab.com/sazid324/tolhub_backend/tolhub-api:$VERSION_API
docker rmi registry.gitlab.com/sazid324/tolhub_backend/mysql:$VERSION_DB

echo "Script completed."
