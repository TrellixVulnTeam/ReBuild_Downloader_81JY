# Server startline arguments
CONTAINER_NAME="rebuild_downloader"

docker build -t $CONTAINER_NAME .
docker run -it --rm --name $CONTAINER_NAME $CONTAINER_NAME python app/main.py