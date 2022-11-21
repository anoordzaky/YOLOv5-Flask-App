//define the elements
const video = document.querySelector("video");
const canvas = document.querySelector("canvas");
const snapBtn = document.getElementById("snapBtn");
const startBtn = document.getElementById("startBtn");
const saveBtn = document.getElementById("saveBtn");
const result = document.getElementById("processed_img");

//add event listener for startBtn to get webcam feed
startBtn.addEventListener("click", async function () {
  try {
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 1280, height: 720 },
    });
    video.srcObject = mediaStream;
  } catch (e) {
    console.error(e);
  }
  video.onloadedmetadata = async function (event) {
    try {
      await video.play();
    } catch (e) {
      console.error(e);
    }
  };
});

//functionality for snapBtn to take the image
snapBtn.addEventListener("click", async function () {
  canvas.getContext("2d").drawImage(video, 0, 0, 1280, 720);
  let image64 = canvas.toDataURL("image/png");
});

//sending and receiving a base64 encoded image to/from flask API using AJAX
saveBtn.addEventListener("click", async function () {
  let image64 = canvas.toDataURL("image/png").match(/,(.*)$/)[1];
  ///console.log(imageData);
  const data = { image64 };
  const option = {
    method: "POST",
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(data),
  };
  const response = await fetch("/home", option); //sending request to flask API
  const json = await response.json(); //awaiting and receiving the json from flask API
  console.log(json);
  var img = json["image"];

  var img_link = "data:image/jpeg;base64," + img; //create image on base64 format
  console.log(img_link);
  var toDraw = new Image();
  toDraw.onload = function () {
    canvas.getContext("2d").drawImage(toDraw, 0, 0); //overwrite the image on the canvas with the image from flask API
  };
  toDraw.src = img_link;
  ///console.log(`img base64: ${img}`)
});
