var selectedSongs = document.getElementById("selectedSongs").value.split(",");
var playListAdditionCandidates = new Set();

function handleMouseClick(d, i) {  // Add interactivity
    allSongs =[]
    previousSelectedSongs = new Set(selectedSongs)
    allSongs.push(...previousSelectedSongs)

    if (playListAdditionCandidates.has(d.id)) {
          playListAdditionCandidates.delete(d.id);
          d3.select(this).style("fill","white").style("cursor", "pointer");
    } else {
      d3.select(this).style("fill","green").style("cursor", "pointer");
      playListAdditionCandidates.add(d.id);
    }

    if (playListAdditionCandidates.length != 0) {
      allSongs.push(...Array.from(playListAdditionCandidates))
      allSongsSet = new Set(allSongs)
      allSongs = Array.from(allSongsSet)
      function onAddToPlayListButton() {
              //Navigate to recommendation page  with get params  
              allSongs.join(",")
              window.location.href = `/song_graph?songIds=${allSongs}`;
      }
      const addToPlayListButton = d3.select("#addToPlayList") 
          d3.select("#addToPlayListEl").remove()
          d3.select("#addToPlayList")
          .append("button")
          .text("Add To Playlist")
          .attr("id", "addToPlayListEl")
          .on("click", onAddToPlayListButton)
          .style("font-size", "20px")
    }
}


const endRecommendationButton = d3.select("#endRecommedations")
          .append("button")
          .text("End Recommendations")
          .attr("id", "endRecommedationsEL")
          .on("click", onEndRecommendation)
          .style("font-size", "20px")

function onEndRecommendation() {
              //Navigate to recommendation page  with get params
              window.location.href = `/variability`;
 }

const generateSimilarityGraph = (selectedSongId, algorithm) => {
  d3.select("#similarityGraphDiv").remove();
  d3.json(
    `http://127.0.0.1:5000/api/recommendations?selectedSong=${selectedSongId}&algorithm_type=${algorithm}`,
    function (graph) {
      return {
        nodes: graph.nodes,
        links: graph.links,
      };
    }
  )
    .then(function (data) {
      similarityGraph = d3.select("#similarityGraph");

      var width = 1200,
        height = 800;

      const tooltip = similarityGraph
        .append("div")
        .style("position", "absolute")
        .style("z-index", "10")
        .style("visibility", "hidden")
        .text("");

      var svg = similarityGraph
        .append("svg")
        .attr("id", "similarityGraphDiv")
        .attr("width", "100%")
        .attr("height", height);
      var force = d3
        .forceSimulation()
        .nodes(data.nodes)
        .force("link", d3.forceLink(data.links).distance(300))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("charge", d3.forceManyBody().strength(-250))
        .alphaTarget(1)
        .on("tick", tick);

      var link = svg
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .attr("stroke-width", 2)
        .style("stroke", "black");

      var node = svg
          .selectAll("g.node")
          .data(data.nodes)
          .enter()
          .append("g")
          .on("click", handleMouseClick)
          .style("fill", function (d) {
            if (playListAdditionCandidates.has(d.id)) {
              return "green"
            } else {
              return "white"
            }
          })
          .attr("class", "node");

      var cricle = node
        .append("circle")
        .attr("class", "circle")
        .attr("r", 100)
        .on("mouseover", function(d) {
            return tooltip.style("visibility", "visible")
                          .html( `<span>Name: </span> ${d.label} <br/>
                                  <span>Duration in MS: </span> ${d.duration_ms} <br/>
                                  <span>Release Date: </span> ${d["Release Date"]} <br/>
                                  <span>genres: </span> ${d.genres} <br/>
                                  <span>playcount: </span> ${d.playcount} <br/>
                                  <span>listeners :</span> ${d.listeners} <br/>
                                  <span>energy : </span> ${d.energy} <br/>
                                  <span>key : </span> ${d.key} <br/>
                                  <span>loudness : </span> ${d.loudness} <br/>
                                  <span>mode : </span> ${d.mode} <br/>
                                  <span>speechiness : </span> ${d.speechiness} <br/>
                                  <span>acousticness : </span> ${d.acousticness} <br/>
                                  <span>instrumentalness : </span> ${d.instrumentalness} <br/>
                                  <span>liveness :  </span> ${d.liveness} <br/>
                                  <span>valence : </span> ${d.valence} <br/>
                                  <span>tempo :</span> ${d.tempo} <br/>
                                  `)
          })
        .on("mousemove", function() {
            return tooltip.style("top", (d3.event.pageY - 10) + "px").style("left", (d3.event.pageX + 10) + "px");
          })
        .on("mouseout", function() {
            return tooltip.style("visibility", "hidden");
          })
        .on("dblclick", dblclick);

      var label = node
        .append("svg:text")
        .text(function (d) {
          return d.label;
        })
        .style("text-anchor", "middle")
        .style("font-family", "Arial")
        .style("font-size", 12);
      function dragstart(d) {
        d3.select(this).classed("fixed", (d.fixed = false));
      }
      function dblclick(d) {
        d3.select(this).classed("fixed", (d.fixed = false));
      }
      function tick() {
        link
          .attr("x1", function (d) {
            return d.source.x;
          })
          .attr("y1", function (d) {
            return d.source.y;
          })
          .attr("x2", function (d) {
            return d.target.x;
          })
          .attr("y2", function (d) {
            return d.target.y;
          });

        cricle
          .attr("cx", function (d) {
            return d.x;
          })
          .attr("cy", function (d) {
            return d.y;
          });

        label
          .attr("x", function (d) {
            return d.x;
          })
          .attr("y", function (d) {
            return d.y;
          });
      }
    })
    .catch(function (error) {
      console.log(error);
    });
};


for (var songIndex = 0; songIndex < selectedSongs.length; songIndex++) {
  const songId = selectedSongs[songIndex];
  d3.json(
    `http://127.0.0.1:5000/api/song?songId=${songId}`,
    function (songDetail) {
      return songDetail;
    }
  ).then(function (data) {
      d3.select("#selectedSongsList")
          .append("button")
          .on("click", function () {
           
            algorithm = d3.select("#recommendationAlgorithm").node().value

            generateSimilarityGraph(songId, algorithm);
          })
          .style("width", "400px")
          .style("table-layout", "fixed")
          .style("margin-top", "10px")
          .style("height", "30px")
          .text(data["name"]);
  })
}