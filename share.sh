#!/bin/bash
cd ~/diwali-wishes && source venv/bin/activate
pkill -f "streamlit run" 2>/dev/null; pkill -f "cloudflared tunnel" 2>/dev/null
sleep 1
nohup streamlit run app.py --server.headless true --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false >/tmp/streamlit.log 2>&1 &
sleep 4
nohup cloudflared tunnel --url http://localhost:8501 >/tmp/cf.log 2>&1 &
for i in $(seq 1 30); do
  URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/cf.log | head -1)
  [ -n "$URL" ] && break
  sleep 1
done
echo "Link: ${URL:-not found, check /tmp/cf.log}"
