var graph_songs = document.getElementById("graph_songs").value.split(",");
console.log("graph_songs ", graph_songs)
var margin = {top: 10, right: 20, bottom: 10, left: 20};

    var width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;
      padding = 20;
      x_margin = margin.left;
      y_margin = margin.top;
var colorArray = [d3.schemeCategory10, d3.schemeAccent];
var colors = d3.scaleOrdinal(d3.schemeCategory10);
x =['danceability', 'energy', 'loudness','speechiness','acousticness','instrumentalness','liveness', 'valence','tempo', 'playcount','listeners']

d3.json(
    `http://127.0.0.1:5000/get_recommended_songs?graph_songs=${graph_songs}`,
    function (data) {
      return {
            name: data.name,
            id: data.id,
            type: data.type,

            value: data.value
      };
    }
  )
    .then(function (data) {

    var id_set= d3.set()

data.forEach(function(d){
id_set.add(d.id)
})

d3.select("#selectButton")
      .selectAll('myOptions')
     	.data(x)
      .enter()
    	.append('option')
      .text(function (d) { return d; }) // text showed in the menu
      .attr("value", function (d) { return d; })

        var svg = d3.select("body").append("svg").attr("id","svg-a")
           .attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom);

           svg.append("text")
          .attr("id","title-a")
          .attr("transform", "translate(" + (width / 2) + "," + ( padding) + ")")
          .style("text-anchor", "middle")
          .text("Variability");
            d3.select("#selectButton").on('change' , function () {


              var selectedFeature= d3.select(this).property("value")
			  console.log("Select Option ", selectedFeature)
              lineChart(data, selectedFeature);
           })
             lineChart(data, "danceability");

 function lineChart(data, selectedFeature){

        console.log("selected Feature ", selectedFeature)

        svg.select("#plot-a").remove()

        const yScale = d3.scaleLinear().rangeRound([height-110, 10]);

        const yaxis = d3.axisLeft().ticks(10).scale(yScale);

        var featureValues  = data.filter(function(d) {
            return d.type == selectedFeature
        })

        console.log("featureValues ", featureValues)

        ymin = d3.min(featureValues, function(d){
            return d.value
        })

        ymax = d3.max(featureValues, function(d){
            return d.value
        })
        yScale.domain([ymin, ymax]);
        var xScale = d3.scaleBand().rangeRound([58, width], .1).domain(featureValues.map(function (d) { return d.id; }));

        var xAxis = d3.axisBottom()
         .scale(xScale);


            console.log("ymin ", ymin)
            console.log("ymax ", ymax)
            const plot = svg.append('g').attr("id","plot-a");
            var res = data.map(function(d){ return d.type }) // list of group names
            var color = d3.scaleOrdinal().domain(res)
                    .range(['#2ca25f','#8856a7','#43a2ca','#e34a33','#1c9099','#636363','#dd1c77','#d95f0e','#756bb1'])



            const line = d3.line()
			.x(function(d) {
			    return xScale(d.id);})

			.y(function(d) {
			       //console.log("here ", d.type)
			       //console.log("y value ", d.value)
			    return yScale(d.value);});


            const lines = plot.append('g').attr("id","lines-a").selectAll("lines")
                .data(featureValues)
                    .enter()
                .append("g");

            lines.append("path")

             .attr("d", function(d) { return line(featureValues); })
            .attr("fill", "none")
            .attr("stroke", function(d){
            console.log("the type is", d.type)
                console.log("The color is ", color(d.type))
             return color(d.type) })


     .attr("stroke-width", function(d) {
            return 1.5

        });

        plot.append("g")
    .attr("id","x-axis-a")
	.attr("class", "axis")
	.attr("transform", "translate(" + (-10  ) + ", "+ (height-111) +")")
	.call(xAxis)
     .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", ".15em")
            .attr("transform", "rotate(-65)" )
        ;


plot.append("g")
.attr("id","y-axis-a")
.attr("class", "axis")

 .attr("transform", "translate(" + (padding+38) + "," + (0 ) + ")")
.call(yaxis)
.append("text")
      .attr("id","y-axis-label")
            .attr("transform", "translate(" + -50+ "," + (height / 2) + ") rotate(270)")
            .style("text-anchor", "middle")
            .style('fill', 'black')
            .text(selectedFeature)

   plot.append("g")
    .selectAll("circle")
    .append("g")
    .data(featureValues)
    .enter()
    .append("circle")
    .attr("r", 3)
    .attr("cx", d =>  xScale(d.id))
    .attr("cy", d => yScale(d.value))
    .style("fill", function(d){
    //console.log("the type is", d.type)
    return color(d.type)})

 }


     })
    .catch(function (error) {
      console.log(error);
    });

