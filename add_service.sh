NAME=$1
PORT=$2

TUNNEL_NAME="${TUNNEL_NAME:-arson-dev}"
DOMAIN="${DOMAIN:-arson.dev}"
CLOUDFLARED_CONFIG_FILE="${CLOUDFLARED_CONFIG_FILE:-/etc/cloudflared/config.yml}"

if [ -z "$NAME" ] || [ -z "$PORT" ]; then
  echo "Usage: $0 <service-name> <port>"
  exit 1
fi

cloudflared tunnel route dns $TUNNEL_NAME $NAME.$DOMAIN

echo "Creating tunnel for $NAME on port $PORT..."

cat <<EOF >>$CLOUDFLARED_CONFIG_FILE
  - hostname: $NAME.$DOMAIN
    service: http://localhost:$PORT
EOF
