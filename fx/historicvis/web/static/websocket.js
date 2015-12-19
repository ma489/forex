var ws = new WebSocket("ws://127.0.0.1:5678/"),
                buyOrders = document.createElement('ul');
                sellOrders = document.createElement('ul');
                matchedOrders = document.createElement('ul');

ws.onmessage = function (event) {
    if (event.data.indexOf("Buy") > -1) { //this is a buy order
        var messages = document.getElementsByTagName('ul')[0];
        var buyOrdersTable = document.getElementById('buyOrders');
        var row = buyOrdersTable.insertRow(-1);
        var cell1 = row.insertCell(0);
        orderId = event.data.split(" ")[10];
        row.setAttribute("id", orderId);
        cell1.innerHTML = orderId;
        orderSize = event.data.split(" ")[6];
        var cell2 = row.insertCell(1);
        cell2.innerHTML = orderSize.slice(0, -2);
    } else if (event.data.indexOf("Sell") > -1) {// this is a sell order
        var messages = document.getElementsByTagName('ul')[1];
        orderId = event.data.split(" ")[10];
        var sellOrders = document.getElementById('sellOrders');
        var row = sellOrders.insertRow(-1);
        var cell1 = row.insertCell(0);
        orderId = event.data.split(" ")[10];
        row.setAttribute("id", orderId);
        cell1.innerHTML = orderId;
        orderSize = event.data.split(" ")[6];
        var cell2 = row.insertCell(1);
        cell2.innerHTML = orderSize.slice(0, -2);
    } else if (event.data.indexOf("Matched") > -1) { //orders matched
        var messages = document.getElementsByTagName('ul')[2];
        orderId = event.data.split(" ")[10];
    } else if (event.data.indexOf("Filled") > -1) { //orders matched
        orderId = event.data.split(" ")[1];
        var orderEntry = document.getElementById(orderId);
        orderEntry.style.color = "red";
        orderEntry.style.textDecoration = "line-through";
    }
};