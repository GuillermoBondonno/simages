
var lastCompletedBoundingBox = {"ulx" : 0,
                                "uly" : 0,
                                "brx" : 0,
                                "bry" : 0,};

let NDVIImageUrl = "";
let NDVIIndexValue = 0;
let lastUpdatedNDVIIndex = "";
let headers;
            
function initMap() {
                    const map = new google.maps.Map(document.getElementById("map"), {
                    center: { lat: -34.669376, lng: -58.645895 },
                    zoom: 10,
                    });
                    const drawingManager = new google.maps.drawing.DrawingManager({
                    drawingMode: google.maps.drawing.OverlayType.MARKER,
                    drawingControl: true,
                    drawingControlOptions: {
                    position: google.maps.ControlPosition.TOP_CENTER,
                    drawingModes: [
                    //google.maps.drawing.OverlayType.MARKER,
                    //google.maps.drawing.OverlayType.CIRCLE,
                    //google.maps.drawing.OverlayType.POLYGON,
                    //google.maps.drawing.OverlayType.POLYLINE,
                    google.maps.drawing.OverlayType.RECTANGLE,
                    ],
                    },
                    markerOptions: {
                    icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
                    },
                    });

                    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(shape) {
                                                    console.log("A shape has been completed!");
                                                    lastCompletedBoundingBox.ulx = shape.overlay.bounds.Hb.g;
                                                    lastCompletedBoundingBox.uly = shape.overlay.bounds.tc.i;
                                                    lastCompletedBoundingBox.brx = shape.overlay.bounds.Hb.i;
                                                    lastCompletedBoundingBox.bry = shape.overlay.bounds.tc.g;
                                                                                                    });
                    drawingManager.setMap(map);

                    }


function generateNDVIImage() {
    //make the request to the localhost endpoint
    //using lastCompletedBoundingBox as coordinates for the area of interest
    NDVIImageUrl = "http://127.0.0.1:8094/demo/ulx/"+lastCompletedBoundingBox.ulx
                    +"/uly/"+lastCompletedBoundingBox.uly+"/brx/"
                    +lastCompletedBoundingBox.brx+"/bry/"+lastCompletedBoundingBox.bry;
    
    console.log("To make request and set the img source to "+NDVIImageUrl);

    var oReq = new XMLHttpRequest();
    oReq.open("GET", NDVIImageUrl, true);
    oReq.responseType = "arraybuffer";

    oReq.onloadstart = function(){
      console.log("onloadstart called!")
    document.getElementById("NDVIImage").src = "https://i.stack.imgur.com/hzk6C.gif";

    }
    
    oReq.onload = function (oEvent) {
    console.log("Headers: ", oReq.getAllResponseHeaders());

      headers = oReq.getAllResponseHeaders();
      NDVIIndexValue = oReq.getResponseHeader("ndvi");
      lastUpdatedNDVIIndex = oReq.getResponseHeader("last_updated");
      console.log(NDVIIndexValue, lastUpdatedNDVIIndex);

      var arrayBuffer = oReq.response; // Note: not oReq.responseText
      if (arrayBuffer) {
        console.log("Arraybuffer found!")
        byteArray = new Uint8Array(arrayBuffer);
        console.log(byteArray)
        var blob = new Blob([byteArray], { type: "image/png" });
        var url = URL.createObjectURL(blob);
        console.log(NDVIIndexValue, lastUpdatedNDVIIndex);
        document.getElementById("NDVIImage").src = url;
        document.getElementById("NDVIValue").innerHTML = NDVIIndexValue;
        document.getElementById("NDVILastUpdated").innerHTML = "Last updated: "+lastUpdatedNDVIIndex;

      }
    };

    oReq.send(null);


        

  
};