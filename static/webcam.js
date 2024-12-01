const videoElement = document.getElementById("video");
        const captureBtn = document.getElementById("captureBtn");
        const uploadBtn = document.getElementById("uploadBtn");
        const imageInput = document.getElementById("imageInput");

        // 웹캠을 시작하는 함수
        async function startWebcam() {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            videoElement.srcObject = stream;
        }

        // 캡쳐 버튼 클릭 시 이미지 캡쳐 및 서버로 전송
        captureBtn.addEventListener("click", async () => {
            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

            // 이미지를 Blob 형태로 변환
            canvas.toBlob(async (blob) => {
                const formData = new FormData();
                formData.append("file", blob, "image.jpg");

                // 서버로 이미지 전송
                const response = await fetch("/predict", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();
                if (data.color) {
                    // 추천된 색상을 쿼리 파라미터로 전달
                    const queryParams = new URLSearchParams({
                        color: data.color
                    });
                    window.location.href = `/light?${queryParams.toString()}`;
                } else {
                    alert(`예측 실패: ${data.error}`);
                }
            }, "image/jpeg");
        });

        // 업로드 버튼 클릭 시 이미지 파일을 서버로 전송
        uploadBtn.addEventListener("click", async () => {
            if (imageInput.files.length === 0) {
                alert("이미지를 선택해주세요.");
                return;
            }

            const file = imageInput.files[0];
            const formData = new FormData();
            formData.append("file", file);

            // 서버로 이미지 전송
            const response = await fetch("/predict", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            if (data.color) {
                // 추천된 색상을 쿼리 파라미터로 전달
                const queryParams = new URLSearchParams({
                    color: data.color
                });
                window.location.href = `/light?${queryParams.toString()}`;
            } else {
                alert(`예측 실패: ${data.error}`);
            }
        });

        // 웹캠 시작
        startWebcam();