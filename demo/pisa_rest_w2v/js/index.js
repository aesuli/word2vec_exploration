var wi = window,
    d = document,
    e = d.documentElement,
    g = d.getElementsByTagName('body')[0],
    w = wi.innerWidth || e.clientWidth || g.clientWidth,
    h = wi.innerHeight|| e.clientHeight|| g.clientHeight;

var circleWidth = 3;

var fontFamily = 'Bree Serif',
    fontSizeHighlight = 2,
    fontSizeNormal = 0.8;

var palette = {
      "lightgray": "#819090",
      "gray": "#708284",
      "mediumgray": "#536870",
      "darkgray": "#475B62",

      "darkblue": "#0A2933",
      "darkerblue": "#042029",

      "paleryellow": "#FCF4DC",
      "paleyellow": "#EAE3CB",
      "yellow": "#A57706",
      "orange": "#BD3613",
      "red": "#D11C24",
      "pink": "#C61C6F",
      "purple": "#595AB7",
      "blue": "#2176C7",
      "green": "#259286",
      "yellowgreen": "#738A05"
  }
  
var zoom = d3.behavior.zoom()
    .scaleExtent([1, 10])
    .on("zoom", zoomed);
	
scale = 1;
	
var margin = {top: -5, right: -5, bottom: -5, left: -5},
    width = wi.w - margin.left - margin.right- margin.left - margin.right,
    height = wi.h - margin.top - margin.bottom- margin.top - margin.bottom;

var svg = d3.select("body")
    .append("svg")
      .attr("class", "stage")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
	  .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.right + ")")
      .call(zoom);
	  
var rect = svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");
		
var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .gravity(.1)
    .charge(-100)
    .linkStrength(1)
    .size([w, h]);

var link = svg.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("stroke", "#CCC")
    .attr("fill", "none")
	.attr("vector-effect", "non-scaling-stroke");

var node = svg.selectAll("circle.node")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node")
    //MOUSEOVER
    .on("mouseover", function(d,i) {
        if (i>0) {
            //CIRCLE
            d3.select(this).selectAll("circle")
            .transition()
            .duration(250)
            .style("cursor", "none")
            .attr("r", circleWidth+3)
            .attr("fill",palette.orange);

            //TEXT
            d3.select(this).select("text")
            .transition()
            .style("cursor", "none")
            .duration(250)
            .style("cursor", "none")
            .attr("font-size",fontSizeHighlight/scale+'em')
            .attr("x", 15 )
            .attr("y", 5 )
        } else {
            //CIRCLE
            d3.select(this).selectAll("circle")
            .style("cursor", "none")

            //TEXT
            d3.select(this).select("text")
            .style("cursor", "none")
        }
    })
    //MOUSEOUT
    .on("mouseout", function(d,i) {
        if (i>0) {
            //CIRCLE
            d3.select(this).selectAll("circle")
            .transition()
            .duration(250)
            .attr("r", circleWidth)
            .attr("fill",palette.pink);

            //TEXT
            d3.select(this).select("text")
            .transition()
            .duration(250)
            .attr("font-size",(fontSizeNormal/scale)+'em')
            .attr("x", 8 )
            .attr("y", 4 )
        }
    })

    .call(force.drag);


//CIRCLE
node.append("svg:circle")
  .attr("cx", function(d) { return d.x; })
  .attr("cy", function(d) { return d.y; })
  .attr("r", circleWidth)
  .attr("fill", function(d, i) { if (i>0) { return  palette.pink; } else { return palette.paleryellow } } )

//TEXT
node.append("text")
  .text(function(d, i) { return d.name; })
.attr("x",    function(d, i) { return circleWidth + 5; })
  .attr("y",            function(d, i) { if (i>0) { return circleWidth + 0 }    else { return 8 } })
  .attr("font-family",  "Bree Serif")
  .attr("fill",         function(d, i) {  return  palette.paleryellow;  })
  .attr("font-size",    function(d, i) {  return  (fontSizeNormal/scale)+'em'; })
  .attr("text-anchor",  function(d, i) { if
  (i>0) { return  "beginning"; }      else { return "end" } })

force.on("tick", function(e) {
  node.attr("transform", function(d, i) {     
        return "translate(" + d.x + "," + d.y + ")"; 
    });
    
   link.attr("x1", function(d)   { return d.source.x; })
       .attr("y1", function(d)   { return d.source.y; })
       .attr("x2", function(d)   { return d.target.x; })
       .attr("y2", function(d)   { return d.target.y; })
});

function zoomed() {
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  scale =  d3.event.scale
  svg.selectAll("text").attr("font-size",(fontSizeNormal/scale)+'em');
}

function updateWindow(){
    x = wi.innerWidth || e.clientWidth || g.clientWidth;
    y = wi.innerHeight|| e.clientHeight|| g.clientHeight;

    d3.select('svg').attr("width", x).attr("height", y);
}
window.onresize = updateWindow;


force.start();