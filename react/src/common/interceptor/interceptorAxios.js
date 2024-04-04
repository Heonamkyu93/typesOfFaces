import axios from 'axios';



const serverIp = process.env.REACT_APP_SPRING_BOOT_IP;
const serverPort = process.env.REACT_APP_SPRING_BOOT_PORT;
// Axios 인스턴스 생성
const axiosInstance = axios.create({
  baseURL: `http://${serverIp}:${serverPort}`
});

// 요청 인터셉터 추가
axiosInstance.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('jwt');
    if (token) {
      config.headers["Authorization"] = 'Bearer ' + token;
    }
    return config;
  },
  error => {
    Promise.reject(error);
  }
);

// 응답 인터셉터 추가
axiosInstance.interceptors.response.use((response) => {
  return response;
}, async function (error) {
  const originalRequest = error.config;
  if (error.response.status === 403 && !originalRequest._retry) {
    originalRequest._retry = true;
    const refreshToken = sessionStorage.getItem('refreshToken');
    return axiosInstance.post('/refresh-token', {}, { // 요청 본문은 비워두고
      headers: { "Refresh-Token": `Bearer ${refreshToken}` } // 리프레쉬 토큰을 헤더에 추가
    })
      .then(res => {
        if (res.status === 200) {
          const authToken = res.headers.get('Authorization');
          sessionStorage.setItem('jwt', authToken);
          
          axios.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.jwt;
          return axiosInstance(originalRequest);
        }
      });
  }
  return Promise.reject(error);
});


export default axiosInstance;