PORT=$1
NAME=$2

if [ -z "$NAME" ]; then
  NAME=$(basename "$PWD")
fi

echo "Building service"

npm i
npm run build

echo "Starting $NAME on port $PORT"

pm2 delete $NAME
pm2 start dist/index.js --name $NAME -- $PORT

echo "Service $NAME started on port $PORT"
