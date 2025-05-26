// More API functions here:
// https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose

async function init() {
        const modelURL = URL + "model.json";
        const metadataURL = URL + "metadata.json";

        // load the model and metadata
        // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
        // Note: the pose library adds a tmPose object to your window (window.tmPose)
        model = await tmPose.load(modelURL, metadataURL);
        maxPredictions = model.getTotalClasses();

        // Convenience function to setup a webcam
        const size = 300;
        const flip = true; // whether to flip the webcam
        webcam = new tmPose.Webcam(size, size, flip); // width, height, flip
        await webcam.setup(); // request access to the webcam
        await webcam.play();
        window.requestAnimationFrame(loop);

        // append/get elements to the DOM

        const canvas = document.getElementById("canvas");
        canvas.width = size; canvas.height = size;
        ctx = canvas.getContext("2d");
        labelContainer = document.getElementById("label-container");
        for (let i = 0; i < maxPredictions; i++) { // and class labels
            labelContainer.appendChild(document.createElement("div"));
          
        }


    }

    async function loop(timestamp) {
        webcam.update(); // update the webcam frame
        await predict();
        window.requestAnimationFrame(loop);
    }

   
    let alertShown = false; // Variável para garantir que o alerta só ocorra uma vez

async function predict() {
    const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
    const prediction = await model.predict(posenetOutput);

    for (let i = 0; i < maxPredictions; i++) {
        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        labelContainer.childNodes[i].innerHTML = classPrediction;

        if (prediction[i].className === "triceps errado" && prediction[i].probability > 0.9 && !alertShown) {
            alertShown = true; // Marca o alerta como mostrado
            playSound();
            showAlertPopup();
        }
    }

    drawPose(pose);
}

    function playSound(){
        const audio = new Audio('sonoro.mp3');
        audio.play();
    }

    function drawPose(pose) {
        if (webcam.canvas) {
            ctx.drawImage(webcam.canvas, 0, 0);
            // draw the keypoints and skeleton
            if (pose) {
                const minPartConfidence = 0.5;
                tmPose.drawKeypoints(pose.keypoints, minPartConfidence, ctx);
                tmPose.drawSkeleton(pose.keypoints, minPartConfidence, ctx);
            }
        }
    }

function showAlertPopup() {
    const popup = document.createElement("div");
    popup.innerHTML = `
        <div style="position:fixed; top:50%; left:50%; transform:translate(-50%, -50%);
                    background:#fff; padding:20px; border-radius:10px; box-shadow:0px 0px 10px rgba(0,0,0,0.2);">
            <p>Alerta: Corrija sua postura!</p>
            <button id="okButton">OK</button>
        </div>
    `;
    document.body.appendChild(popup);
    
    document.getElementById("okButton").addEventListener("click", () => {
        alertShown = false; // Reseta o alerta para permitir novos avisos
        popup.remove(); // Remove o pop-up
    });
}