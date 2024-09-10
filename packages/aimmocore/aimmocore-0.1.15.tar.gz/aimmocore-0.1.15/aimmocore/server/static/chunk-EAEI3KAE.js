// projects/smart-curation-viewer/src/app/app.route.paths.ts
var route = {
  home: {
    name: "home",
    path: "",
    fullPath: "/"
  },
  dataset: {
    name: "dataset",
    path: `dataset/:datasetId`,
    fullPath: DATASET_PATH
  }
};
function DATASET_PATH(datasetId) {
  return `/dataset/${datasetId}`;
}

export {
  route
};
