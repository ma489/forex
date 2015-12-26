echo "Killing Exchange Simulation Server..."
exchangeProcId=$(pgrep -f Exchange.py)
echo "Process ID: $exchangeProcId"
if [ -z "$exchangeProcId" ]
  then
	echo "Exchange Simulation Server not running"
else
	kill $exchangeProcId
fi
echo "...Done"
echo "Killing Main web server..."
mainProcId=$(pgrep -f Main.py)
echo "Process ID: $mainProcId"
if [ -z "$mainProcId" ]
  then
	echo "Main web server not running"
else
	kill $mainProcId
fi
echo "Shutting down."
