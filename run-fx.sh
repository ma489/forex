echo "Starting Exchange Simulation Server..."
nohup python3 fx/exchangesim/exchange/Exchange.py &
echo "...Done"
echo "Starting Main web server..."
python3 fx/web/Main.py
echo "Shutting down."
