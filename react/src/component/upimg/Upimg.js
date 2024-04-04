import React, { useState } from 'react';
import axios from 'axios';
import styles from './Upimg.module.css';
import { Bar } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

// 차트 구성 요소를 등록합니다.
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const serverIp = process.env.REACT_APP_FASTAPI_IP;
const serverPort = process.env.REACT_APP_FASTAPI_PORT;

const Upimg = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState('');
    const [fileName, setFileName] = useState('');
    // 차트 데이터 상태를 null로 초기화합니다.
    const [chartData, setChartData] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            // 이미지 선택 시, 차트 데이터를 초기화합니다.
            setChartData(null); // 이미지가 변경될 때 차트를 지웁니다.

            const reader = new FileReader();
            reader.onload = (e) => {
                const img = document.createElement("img");
                img.onload = () => {
                    const canvas = document.createElement("canvas");
                    canvas.width = img.width;
                    canvas.height = img.height;

                    const ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);

                    canvas.toBlob((blob) => {
                        const newFile = new File([blob], "converted.jpg", { type: "image/jpeg", lastModified: Date.now() });
                        setSelectedFile(newFile);
                        setPreview(URL.createObjectURL(newFile));
                        setFileName(newFile.name);
                    }, 'image/jpeg', 1);
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            alert('이미지 파일이 아닙니다.');
        }
    };

    const handleUpload = async () => {
        if (selectedFile) {
            const formData = new FormData();
            formData.append('file', selectedFile);

            try {
                const response = await axios.post(`http://${serverIp}:${serverPort}/in/img`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                console.log('서버 응답:', response.data);
                updateChartData(response.data);
            } catch (error) {
                console.error('업로드 실패:', error);
                alert(error.response.data.detail);
            }
        }
    };

    const updateChartData = (data) => {
        const labels = data.predictions.map(item => item[0]);
        const values = data.predictions.map(item => parseFloat(item[1].replace('%', '')));

        setChartData({
            labels: labels,
            datasets: [{
                label: '분석 결과 (%)',
                data: values,
                backgroundColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#cc65fe', '#445ce2', '#e244b1', '#0c420f'
                ],
                borderColor: [
                    '#FF6384', '#36A2EB', '#FFCE56', '#cc65fe', '#445ce2', '#e244b1', '#0c420f'
                ],
                borderWidth: 1,
            }]
        });
        
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.font}>나와 닮은 동물은?</h1>
            <div className={styles.uploadControl}>
                <input type="file" id="fileInput" className={styles.fileInput} onChange={handleFileChange} />
                <label htmlFor="fileInput" className={styles.fileInputLabel}>{fileName || '파일 선택'}</label>
                <button onClick={handleUpload} className={styles.uploadButton}>얼굴분석</button>
            </div>
            {preview && <img src={preview} alt="Preview" className={styles.imagePreview} />}
            {/* 차트 데이터가 있을 때만 차트를 표시합니다. */}
            <div className={styles.graphContainer}> {/* 스타일 적용 */}
            {chartData && (
                <Bar data={chartData} options={{
                    indexAxis: 'y',
                    scales: {
                        x: {
                            beginAtZero: true,
                        },
                    },
                    plugins: {
                        legend: {
                            display: true,
                        },
                        title: {
                            display: true,
                            text: '분석 결과',
                        },
                    },
                }} />
            )}
        </div>
        </div>
    );
}

export default Upimg;
