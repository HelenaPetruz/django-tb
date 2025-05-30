// More API functions here:
// https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose

async function init() {
    document.getElementById("btnTIAs").style.display = "none";
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    // load the model and metadata
    // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
    // Note: the pose library adds a tmPose object to your window (window.tmPose)
    model = await tmPose.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    // Convenience function to setup a webcam
    const size1 = 900;
    const size2 = 900;
    const flip = true; // whether to flip the webcam
    webcam = new tmPose.Webcam(size1, size2, flip); // width, height, flip
    await webcam.setup(); // request access to the webcam
    await webcam.play();
    window.requestAnimationFrame(loop);

    // append/get elements to the DOM

    const canvas = document.getElementById("canvasSmall");
    canvas.width = size1; canvas.height = size2;
    ctx = canvas.getContext("2d");
    labelContainer = document.getElementById("label-containerSmall");
    for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));

    }


}

async function init1() {
    document.getElementById("btnTIAl").style.display = "none";
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";

    // load the model and metadata
    // Refer to tmImage.loadFromFiles() in the API to support files from a file picker
    // Note: the pose library adds a tmPose object to your window (window.tmPose)
    model = await tmPose.load(modelURL, metadataURL);
    maxPredictions = model.getTotalClasses();

    // Convenience function to setup a webcam
    const size1 = 900;
    const size2 = 900;
    const flip = true; // whether to flip the webcam
    webcam = new tmPose.Webcam(size1, size2, flip); // width, height, flip
    await webcam.setup(); // request access to the webcam
    await webcam.play();
    window.requestAnimationFrame(loop);

    // append/get elements to the DOM

    const canvas = document.getElementById("canvasLarge");
    canvas.width = size1; canvas.height = size2;
    ctx = canvas.getContext("2d");
    labelContainer = document.getElementById("label-containerLarge");
    for (let i = 0; i < maxPredictions; i++) { // and class labels
        labelContainer.appendChild(document.createElement("div"));

    }


}

async function loop(timestamp) {
    webcam.update(); // update the webcam frame
    await predict();
    window.requestAnimationFrame(loop);
}
let alertShown = false;

async function predict() {
    const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
    const prediction = await model.predict(posenetOutput);
    labelContainer.innerHTML = "";

    for (let i = 0; i < maxPredictions; i++) {
        let className = prediction[i].className.trim().toLowerCase();
        const probability = prediction[i].probability;
        const percentage = Math.round(probability * 100);

        console.log("Classe detectada:", className); // <<< AJUDA A VER O NOME EXATO

        // ignora qualquer variação da classe "nada"
        if (className.includes("nada")) continue;

        const progressWrapper = document.createElement("div");
        progressWrapper.className = "mt-6 text-start";

        const label = document.createElement("div");
        label.innerText = `${prediction[i].className} (${percentage}%)`;
        label.className = "fw-bold mb-1";

        const progress = document.createElement("div");
        progress.className = "progress";
        progress.style.height = "20px";

        const progressBar = document.createElement("div");
        progressBar.className = "progress-bar";
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute("aria-valuenow", percentage);
        progressBar.setAttribute("aria-valuemin", "0");
        progressBar.setAttribute("aria-valuemax", "100");
        progressBar.innerText = `${percentage}%`;

        if (className.includes("certo")) {
            progressBar.classList.add("bg-success");
        } else {
            progressBar.classList.add("bg-danger");
        }

        progress.appendChild(progressBar);
        progressWrapper.appendChild(label);
        progressWrapper.appendChild(progress);

        labelContainer.appendChild(progressWrapper);

        const classPrediction =
            prediction[i].className + ": " + prediction[i].probability.toFixed(2);
        // labelContainer.childNodes[i].innerHTML = classPrediction;

        // if (prediction[i].className === nome_do_erro && prediction[i].probability > 0.9 && !alertShown) {
        // if (prediction[i].className === "triceps errado" && prediction[i].probability > 0.9 && !alertShown) {
        //     alertShown = true; // Marca o alerta como mostrado
        //     playSound();
        //     showAlertPopup();
        // }
    }

    drawPose(pose);
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

function mostrarDescricao() {
    var myModal = new bootstrap.Modal(document.getElementById('modalDescanso'));
    myModal.show();
}


function playSound() {
    const audio = new Audio('alerta.mp3');
    audio.play();
}

function showAlertPopup() {


const popup = document.createElement("div");
popup.innerHTML = `
<div class="modal fade show" id="modalDescanso" tabindex="-1" aria-hidden="true"
    style="display: block; background-color: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content text-center rounded-5"
            style="background-color: #1e1656; color: #ffca3a;">
            <div class="modal-header border-0">
                <h5 class="modal-title w-100 fw-bold">Oops</h5>
                <button type="button" class="btn-close" id="closeModal"></button>
            </div>
            <div class="modal-body">
                <p id="timer" class="display-4 fs-6">Alerta: Corrija sua postura!</p>
                <button id="okButton" class="btn btn-warning">OK</button>
            </div>
        </div>
    </div>
</div>
`;
document.body.appendChild(popup);

document.getElementById("okButton").addEventListener("click", () => {
popup.remove();
alertShown = false; // Remove o pop-up
});

document.getElementById("closeModal").addEventListener("click", () => {
popup.remove();
alertShown = false; // Fecha o modal ao clicar no botão de fechar
});
}
