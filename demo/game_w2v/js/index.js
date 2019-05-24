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



var vis = d3.select("body")
    .append("svg:svg")
      .attr("class", "stage")
      .attr("width", w)
      .attr("height", h);

var force = d3.layout.force()
    .nodes(nodes)
    .links(links)
    .gravity(.4)
    .charge(-200)
    .linkStrength(10)
    .size([w, h]);

var link = vis.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .attr("stroke", "#CCC")
    .attr("fill", "none");

var node = vis.selectAll("circle.node")
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
            .attr("font-size",fontSizeHighlight)
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
            .attr("font-size",fontSizeNormal)
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
  .attr("font-size",    function(d, i) {  return  fontSizeNormal; })
  .attr("text-anchor",  function(d, i) { if (i>0) { return  "beginning"; }      else { return "end" } })

force.on("tick", function(e) {
  node.attr("transform", function(d, i) {     
        return "translate(" + d.x + "," + d.y + ")"; 
    });
    
   link.attr("x1", function(d)   { return d.source.x; })
       .attr("y1", function(d)   { return d.source.y; })
       .attr("x2", function(d)   { return d.target.x; })
       .attr("y2", function(d)   { return d.target.y; })
});

function updateWindow(){
    x = wi.innerWidth || e.clientWidth || g.clientWidth;
    y = wi.innerHeight|| e.clientHeight|| g.clientHeight;

    vis.attr("width", x).attr("height", y);
}
window.onresize = updateWindow;


force.start();