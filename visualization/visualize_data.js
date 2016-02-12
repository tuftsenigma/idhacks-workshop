
    // IDHacks 2016 Workshop - Visualize Tufts Graduate Outcomes:

    // Javascript to take data from Python processing stage and visualize using D3
    // library. (3/3)


    
d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)             
            .attr("y", 40)
            .style("font-size", "24px")
            .text("Jumbo Graduates in the United States");

d3.select("#title").append("svg")
            .attr("width", 900)
            .attr("height", 50)
            .append("text")
            .attr("x", 100)             
            .attr("y", 20)
            .attr("fill", "#989898")
            .style("font-size", "14px")
            .text("Domestic first outcomes of Tufts graduates (hover for statistics)");

var map = new Datamap({
  element: document.getElementById('container'),
  scope: 'usa',
  geographyConfig: {
  popupTemplate: function(geography, data) {
    return '<div style="border-radius:10px; padding: 10px; position: relative; top: -50px; right: -50px; opacity: 0.85;" class="hoverinfo"><b><div style="font-size:20px">' + geography.properties.name + '</div></b>' + "<br>" + 
    '<b>Reported # of grads:</b> &#09;' +  data["number of graduates"] + '<br>' +        
    '<b>Most popular position:</b> &#09;' +  data["most popular title"] + '<br>' +
    '<b>Most popular destination:</b> &#09;' +  data["most popular city"] + '<br>' +
    '<b>Most popular institution:</b> &#09;' +  data["most popular company"] + '<br>';
    }
},
  fills: {
        "0" : "#EAE7E6",
        "1-9": '#C1B7B2',
        "10-19": '#988780',
        "20-49": '#6E574D',
        "50-99": '#593F33',
        "100+": '#300F00',
        defaultFill: '#EAE7E6'
    },
dataUrl : "final_jobs_data.json",

});
map.legend();