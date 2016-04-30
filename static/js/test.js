
d3.tsv("static/tsv/data.tsv", type, function(error, data) {
    console.log("hey");
    console.log(data);
});
$.get('/data', function(data){
    var object = data.object;
    console.log("hey2");
    console.log(object);
});
function type(d) {
  d.value = +d.value;
return d;
}

/* OLD EXAMPLE */
/*
$.get('/data', function(data){
var svg = d3.select("body")
            .append("svg")
            .attr("width", 300)
            .attr("height", 50*data.random.length);

    svg.selectAll(".bar")
       .data(data.random)
       .enter()
       .append("rect")
       .attr({
            class : "bar",
            width : function(d) {return d;},
            height: "40",
            y : function(d, i) {return i*50 + 10;},
            x : "10"
        });
});

*/

var margin = {top: 20, right: 30, bottom: 40, left: 30},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scale.linear()
    .range([0, width]);

var y = d3.scale.ordinal()
    .rangeRoundBands([0, height], 0.1);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickSize(0)
    .tickPadding(6);

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

$.get('/data', function(dataWrapper){
  var data = dataWrapper.object;
  x.domain(d3.extent(data, function(d) { return d.value; })).nice();
  y.domain(data.map(function(d) { return d.name; }));

  svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", function(d) { return "bar bar--" + (d.value < 0 ? "negative" : "positive"); })
      .attr("x", function(d) { return x(Math.min(0, d.value)); })
      .attr("y", function(d) { return y(d.name); })
      .attr("width", function(d) { return Math.abs(x(d.value) - x(0)); })
      .attr("height", y.rangeBand());

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + x(0) + ",0)")
      .call(yAxis);
});

function type(d) {
  d.value = +d.value;
  return d;
}
//onsole.log(data);
