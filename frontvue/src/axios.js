import axios from 'axios';

const axiosInstance = axios.create({
  timeout: 30000, // Set timeout to 10 seconds
});

export default {
  install(app) {
    app.config.globalProperties.$http = axiosInstance;
  }
};
