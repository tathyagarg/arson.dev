NAME=$1
PORT=$2
RESTART=$3

TUNNEL_NAME="${TUNNEL_NAME:-arson-dev}"
DOMAIN="${DOMAIN:-arson.dev}"
CLOUDFLARED_CONFIG_FILE="${CLOUDFLARED_CONFIG_FILE:-/etc/cloudflared/config.yml}"

if [ -z "$NAME" ] || [ -z "$PORT" ]; then
  echo "Usage: $0 <service-name> <port>"
  exit 1
fi

cloudflared tunnel route dns $TUNNEL_NAME $NAME.$DOMAIN

echo "Creating tunnel for $NAME on port $PORT..."

sed '$i\
  - hostname: '"$NAME.$DOMAIN"'\
    service: http://localhost:'"$PORT"'
' $CLOUDFLARED_CONFIG_FILE >temp && sudo mv temp $CLOUDFLARED_CONFIG_FILE

if [ "$RESTART" = "true" ]; then
  sudo docker-compose down
  sudo docker-compose up -d
else
  sudo docker-compose up -d $NAME
fi
sudo systemctl restart cloudflared
