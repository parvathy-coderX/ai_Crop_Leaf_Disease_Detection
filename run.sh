#!/usr/bin/env bash
set -e

echo "Starting SmartAgriAI backend and frontend"

cd backend
python app.py &
BACKEND_PID=$!

cd ../frontend
npm start

trap "kill $BACKEND_PID" EXIT
