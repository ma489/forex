// request the data
d3.json("/historic/GBPUSD",
    function(error, ticks) {
        first = ticks[0];
        display(first);
    }
);

function display(tick) {
    document.write(tick);
}