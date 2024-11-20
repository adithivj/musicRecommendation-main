const mainFilterData = ["Genres", "Release Date", "Top Artists"];

const queryConfigs = {
  "Genres": {
    param: "genre",
    apiEndpoint: `getGenreOptions`,
    formatOptionText: (d) => d.charAt(0).toUpperCase() + d.slice(1),
    formatOptionValue: (d) => d
  },
  "Release Date": {
    param: "year",
    apiEndpoint: `getReleaseDateOptions`,
    formatOptionText: (d) => d,
    formatOptionValue: (d) => d
  },
  "Top Artists": {
    param: "artistID",
    apiEndpoint: `getTopArtistOptions`,
    formatOptionText: (d) => {
      const artistName = d[0];
      return artistName.slice(2, artistName.length-2);
    },
    formatOptionValue: (d) => {
      artistID = d[1]
      return artistID;
    }
  },
};

var mainFilterSelect = document.getElementById("mainFilterSelect");

const updateSubFilterSelect = () => {
  const config = queryConfigs[mainFilterSelect.value]

  d3.json(`http://127.0.0.1:5000/api/${config.apiEndpoint}`)
    .then((result) => {
      d3.select("#subFilterSelect")
        .selectAll("option")
        .data(result.sort())
        .enter()
        .append("option")
        .text(function (d) {
          return config.formatOptionText(d);
        })
        .attr("value", function (d) {
          return config.formatOptionValue(d);
        });
    })
    .catch((error) => {
      console.error(error);
    });
};

d3.select("#mainFilterSelect")
  .selectAll("option")
  .data(mainFilterData)
  .enter()
  .append("option")
  .text(function (d) {
    return d;
  })
  .attr("value", function (d) {
    return d;
  });


d3.select("#mainFilterSelect").on("change", function () {
  d3.select("#subFilterSelect").selectAll("option").remove();
  updateSubFilterSelect();
});

updateSubFilterSelect();

const goToTopSongs = () => {
  const param = queryConfigs[mainFilterSelect.value].param;
  const value = d3.select("#subFilterSelect").node().value;
  window.location.href = `/songs?${param}=${value}`;
};

d3.select("#goButton").on("click", goToTopSongs);
