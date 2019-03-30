const ROLES = {
    GUEST: 'GUEST',
    ENGINEER: 'ENGINEER',
    ADMIN: 'ADMIN'
};

const FRAME = 10;
const FETCH_INTERVAL = 2 * 1000;


let step = 0;
let chart;
let currentSensor = 0;

function fetchData(){

    // Update data
    var newData = [Date.now(), 560 + Math.random() * 20 - 10];
    data[0].values.push(newData);   // Push data to our array

    // Update graph
    d3.select('#chart svg')
        .datum(data);
    chart.update();

    // Move the frame
    step++;
    if(step === FRAME){
        data[0].values = data[0].values.slice(FRAME);
        step = 0;
    }

    // Call again
    setTimeout(function(){
        fetchData();
    }, FETCH_INTERVAL);
}


var data = [{
        key: 'Датчик 1',
        values: [
            [Date.now() - 86400*10, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*8, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*7, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*5, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*4, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*3, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*2, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*2-7200, 560 + Math.random() * 20 - 10],
                [Date.now() - 86400*2-3600, 560 + Math.random() * 20 - 10],

        ],
    }
];

nv.addGraph(function() {
        chart = nv.models.linePlusBarChart()
            .margin({top: 30, right: 60, bottom: 50, left: 70})
            //We can set x data accessor to use index. Reason? So the bars all appear evenly spaced.
            .x(function(d,i) { return i })
            .y(function(d,i) {return d[1] }).showLegend(false);

        chart.xAxis.tickFormat(function(d) {
            var dx = data[0].values[d] && data[0].values[d][0] || 0;
            return d3.time.format('%I:%M')(new Date(dx))
        });

        chart.y1Axis
            .tickFormat(d3.format(',f'));

        chart.y2Axis
            .tickFormat(function(d) { return d3.format(',f')(d) + '°' });

        chart.bars.forceY([0]);

        d3.select('#chart svg')
            .datum(data)
            .transition()
            .duration(0)
            .call(chart);

        chart.update();

        // Check new data
        fetchData();

        nv.utils.windowResize(chart.update);
        return chart;
    }
);
