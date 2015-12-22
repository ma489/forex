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
    } else if (event.data.indexOf("PriceUpdate") > -1) { //order partially filled
        updatePrices(event);
    }
};

function displayBuyOrder(event) {
    var messages = document.getElementsByTagName('ul')[0];
    var buyOrdersTable = document.getElementById('buyOrders');
    var row = buyOrdersTable.insertRow(-1);
    var cell1 = row.insertCell(0); //order ID
    orderId = event.data.split(" ")[13].slice(0,-2);
    row.setAttribute("id", orderId);
    cell1.innerHTML = orderId;
    orderSize = event.data.split(" ")[6];
    total = orderSize.slice(0, -2);
    var cell2 = row.insertCell(1); //order conditions
    order_cond = event.data.split(" ")[11].slice(0,-2);
    cell2.innerHTML = order_cond;
    var cell3 = row.insertCell(2); //order price
    ord_price = event.data.split(" ")[4].slice(0,-2);
    cell3.innerHTML = ord_price;
    var cell4 = row.insertCell(3); //order size
    cell4.innerHTML = numberWithCommas(total);
    var cell5 = row.insertCell(4); //progress bar
    prog_bar_html = '<div class="progress"><div id="'+ orderId + '-prog" class="progress-bar progress-bar-striped" role="progressbar"';
    prog_bar_html += ' aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"';
    prog_bar_html += ' style="width:0%;">0/' + total + '</div></div>';
    cell5.innerHTML = prog_bar_html;
}

function displaySellOrder(event) {
    var messages = document.getElementsByTagName('ul')[1];
    orderId = event.data.split(" ")[10];
    var sellOrders = document.getElementById('sellOrders');
    var row = sellOrders.insertRow(-1);
    var cell1 = row.insertCell(0);  //order ID
    orderId = event.data.split(" ")[13].slice(0,-2);
    row.setAttribute("id", orderId);
    cell1.innerHTML = orderId;
    orderSize = event.data.split(" ")[6];
    total = orderSize.slice(0, -2);
    var cell2 = row.insertCell(1); //order conditions
    order_cond = event.data.split(" ")[11].slice(0,-2);
    cell2.innerHTML = order_cond;
    var cell3 = row.insertCell(2); //order price
    ord_price = event.data.split(" ")[4].slice(0,-2);
    cell3.innerHTML = ord_price;
    var cell4 = row.insertCell(3); //order size
    cell4.innerHTML = numberWithCommas(total);
    var cell5 = row.insertCell(4); //progress bar
    prog_bar_html = '<div class="progress"><div id="'+ orderId + '-prog" class="progress-bar progress-bar-striped" role="progressbar"';
    prog_bar_html += ' aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"';
    prog_bar_html += ' style="width:0%;">0/' + total + '</div></div>';
    cell5.innerHTML = prog_bar_html;
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
    orderSize = event.data.split(" ")[2];
    var orderEntry = document.getElementById(orderId);
    $(function() {
         prog_id = "#" + orderId + "-prog";
         $(prog_id).delay(1000).animate({"width": "100%"}, 1000);
         $(prog_id).switchClass("progress-bar-striped","progress-bar-success",500);
         $(prog_id).html(orderSize + "/" + orderSize);
    });
    $("#" + orderId).delay(8000).fadeOut(3000);
}

function displayMatchedOrders(event) {
//TODO use same colour if part of same order filling?
    colour = getRandomColour();
    orderId1 = event.data.split(" ")[2];
    orderId2 = event.data.split(" ")[4];
    $("#" + orderId1).delay(1000).css("outline","solid " + colour);
    $("#" + orderId2).delay(1000).css("outline","solid " + colour);
    //TODO shorten outline time?
    $("#" + orderId1).animate({outlineColor: "none"}, 2000);
    $("#" + orderId2).animate({outlineColor: "none"}, 2000);
}

function getRandomColour() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function updatePrices(event) {
    //PriceUpdate#Bid: %f,Ask: %f,Last: %f
    priceInfo = event.data.split("#")[1].split(",");
    bidPriceInfo = priceInfo[0];
    bidPrice = bidPriceInfo.split(" ")[1];
    askPriceInfo = priceInfo[1];
    askPrice = askPriceInfo.split(" ")[1];
    lastPriceInfo = priceInfo[2];
    lastPrice = lastPriceInfo.split(" ")[1];
    var priceInfoPanelBid = document.getElementById('price-info-panel-bid');
    priceInfoPanelBid.innerHTML = "Bid: " + bidPrice;
    var priceInfoPanelAsk = document.getElementById('price-info-panel-ask');
    priceInfoPanelAsk.innerHTML = "Ask: " + askPrice;
    var priceInfoPanelLast = document.getElementById('price-info-panel-last');
    priceInfoPanelLast.innerHTML = "Last: " + lastPrice;
}
