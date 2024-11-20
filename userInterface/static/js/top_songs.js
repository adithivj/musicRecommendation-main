
var filterType = document.getElementById("filterType").value;
var uri = document.getElementById("uri").value;

function CustomTooltip() {}

CustomTooltip.prototype.init = function(params) {

  var eGui = (this.eGui = document.createElement('div'));
  var color = params.color || 'white';
  var data = params.api.getDisplayedRowAtIndex(params.rowIndex).data;

  eGui.classList.add('custom-tooltip');
  eGui.style['background-color'] = color;
  eGui.innerHTML =
    '<p><span class"name">' +
    data.songName +
    '</span></p>' +
    '<p><span>Artists: </span>' +
    data.artists +
    '</p>' +
    '<p><span>Duration in MS: </span>' +
    data.duration_ms +
    '</p>' +
     '<p><span>Popularity </span>' +
    data.popularity +
    '</p>' +
    '<p><span>genres: </span>' +
        data.genres +
    '</p>'
    +
    '<p><span>Playcount: </span>' +
        data.playcount +
    '</p>'
    +
    '<p><span>listeners: </span>' +
        data.listeners +
    '</p>'
    +
    '<p><span>energy: </span>' +
        data.energy +
    '</p>'
    +
     '<p><span>key: </span>' +
        data.key +
    '</p>'
    +
     '<p><span>speechiness: </span>' +
        data.speechiness +
    '</p>'
    +
    '<p><span>acousticness: </span>' +
        data.acousticness +
    '</p>'
    +
    '<p><span>instrumentalness: </span>' +
        data.instrumentalness +
    '</p>'
    +
    '<p><span>liveness: </span>' +
        data.liveness +
    '</p>'
    +
    '<p><span>valence: </span>' +
        data.valence +
    '</p>'
    +
     '<p><span>tempo: </span>' +
        data.tempo +
    '</p>';
};

CustomTooltip.prototype.getGui = function() {
  return this.eGui;
};

d3.json(uri, function (error,data) {

    console.log(data);

    var columnDefs = [
    { field: 'index', tooltipField: 'artists' }, 
    { field: 'songId', tooltipField: 'artists' ,hide: true},
    { field: 'songName', tooltipField: 'artists' }];

	const songDetails = new Map();

    for (var i = 0; i < data.length; i++) {
    	songDetails.set(data[i].index, data[i])
    } 

    var gridOptions = {
    	defaultColDef: {
		    editable: true,
		    sortable: true,
		    flex: 1,
		    minWidth: 100,
		    filter: true,
		    resizable: true,
		    tooltipComponent: 'customTooltip',
 		},
        columnDefs: columnDefs,
        rowData: data,
        animateRows: true,
		components: {
		    customTooltip: CustomTooltip,
		},
		rowSelection: 'multiple',
		rowMultiSelectWithClick: true,
  		onSelectionChanged: onSelectionChanged,
    };

    function onSelectionChanged() {
	  const selectedRows = gridOptions.api.getSelectedRows();
	  function onRecommendButtonClick() {
	  		//Navigate to recommendation page  with get params  
        var songIds = []
        if (selectedRows) {
          for (var i = 0; i < selectedRows.length; i++) {
            songIds.push(selectedRows[i].songId)
          }
          songIds.join(",")
  	  	  window.location.href = `/song_graph?songIds=${songIds}`;
      }
    }

	  const recommendButton = d3.select("#recoomendButtonEl") 
	  d3.select("#recoomendButtonEl").remove()
	  d3.select("#recommendButton")
		.append("button")
		.text("Recommend")
		.attr("id", "recoomendButtonEl")
		.on("click", onRecommendButtonClick)
		.style("font-size", "20px")
	}

    var songsInput = document.getElementById('songs');
    agGrid.Grid(songsInput, gridOptions);
});
