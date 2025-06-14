// More API functions here:
// https://github.com/googlecreativelab/teachablemachine-community/tree/master/libraries/pose

 async function init() {
            // Mostra o modal de "Aguarde"
            const modal = new bootstrap.Modal(document.getElementById('modalTreinoIAAguarde'));
            modal.show();

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

            // Agora que tudo foi carregado, esconda o modal
            modal.hide();


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
        let erroInicio = null; // Variável para armazenar o tempo de início do erro
        const tempoTolerancia = 3000; // 3 segundos de tolerância
        let alertShown = false; // Flag para evitar alertas repetitivos


        let soundInterval;

        async function predict() {
            const { pose, posenetOutput } = await model.estimatePose(webcam.canvas);
            const prediction = await model.predict(posenetOutput);
            labelContainer.innerHTML = "";


            for (let i = 0; i < maxPredictions; i++) {
                let className = prediction[i].className.trim().toLowerCase();
                const probability = prediction[i].probability;
                const percentage = Math.round(probability * 100);

                //console.log("Classe detectada:", className); // Log para depuração

                // Ignora qualquer variação da classe "nada"
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

                // Define cor conforme a postura detectada
                if (className.includes("certo")) {
                    progressBar.classList.add("bg-success");
                } else {
                    progressBar.classList.add("bg-danger");
                }

                progress.appendChild(progressBar);
                progressWrapper.appendChild(label);
                progressWrapper.appendChild(progress);

                labelContainer.appendChild(progressWrapper);

            //     // Verifica se "Errado abdominal" foi detectado e se a probabilidade é alta
            //     if (className.includes("errado")== true && probability > 0.9) {
            //         erradoDetectado = true;
            //     }
            // }

            // if (erradoDetectado) {
            //     if (!soundInterval) {
            //         soundInterval = setInterval(playSound, 5000);
            //     }
            // } else {
            //     if (soundInterval) {
            //         clearInterval(soundInterval);
            //         soundInterval = null;
            //     }
            // }

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
            const audio = new Audio(alertaPath);
            audio.play();
            setTimeout(5000);
        }