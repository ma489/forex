var ws = new WebSocket("ws://127.0.0.1:5678/"),
                buyOrders = document.createElement('ul');
                sellOrders = document.createElement('ul');
                matchedOrders = document.createElement('ul');

ws.onmessage = function (event) {
    if (event.data.indexOf("Buy") > -1) { //this is a buy order
        displayBuyOrder(event);
    } else if (event.data.indexOf("Sell") > -1) {// this is a sell order
        displaySellOrder(event);
    } else if (event.data.indexOf("Matched") > -1) { //orders matched ?
        displayMatchedOrders(event);
    } else if (event.data.indexOf("Filled") > -1) { //order filled
        displayTotalFill(event);
    } else if (event.data.indexOf("Partial") > -1) { //order partially filled
        displayPartialFill(event);
    }
};

function displayBuyOrder(event) {
    var messages = document.getElementsByTagName('ul')[0];
    var buyOrdersTable = document.getElementById('buyOrders');
    var row = buyOrdersTable.insertRow(-1);
    var cell1 = row.insertCell(0);
    orderId = event.data.split(" ")[10];
    row.setAttribute("id", orderId);
    cell1.innerHTML = orderId;
    orderSize = event.data.split(" ")[6];
    var cell2 = row.insertCell(1);
    total = orderSize.slice(0, -2);
    prog_bar_html = '<div class="progress"><div id="'+ orderId + '-prog" class="progress-bar progress-bar-striped" role="progressbar"';
    prog_bar_html += ' aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"';
    prog_bar_html += ' style="width:0%;">0/' + total + '</div></div>';
    cell2.innerHTML = prog_bar_html;
}

function displaySellOrder(event) {
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
    total = orderSize.slice(0, -2);
    prog_bar_html = '<div class="progress"><div id="'+ orderId + '-prog" class="progress-bar progress-bar-striped" role="progressbar"';
    prog_bar_html += ' aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"';
    prog_bar_html += ' style="width:0%;">0/' + total + '</div></div>';
    cell2.innerHTML = prog_bar_html;
}

function displayPartialFill(event) {
    orderId = event.data.split(",")[0].split(" ")[1];
    total = event.data.split(",")[1].split(" ")[1];
    current = event.data.split(",")[2].split(" ")[1];
    var orderEntry = document.getElementById(orderId);
    var cell2 = orderEntry.cells[1];
    percentage = Math.round((current/total) * 100);
    $(function() {
         prog_id = "#" + orderId + "-prog";
         percentage_string = percentage + "%"
         $(prog_id).animate({"width": percentage_string}, 2000);
         $(prog_id).html(current + "/" + total);
         //TODO aria-valuenow
    });
}

function displayTotalFill(event) {
    orderId = event.data.split(" ")[1];
    var orderEntry = document.getElementById(orderId);
    $(function() {
         prog_id = "#" + orderId + "-prog";
         $(prog_id).animate({"width": "100%"}, 1000);
         $(prog_id).switchClass("progress-bar-striped","progress-bar-success",500);
         $(prog_id).html("100%");
    });
    $("#" + orderId).delay(8000).fadeOut(3000);
}

function displayMatchedOrders(event) {
    var messages = document.getElementsByTagName('ul')[2];
    orderId = event.data.split(" ")[10];
    //HUH?
}
