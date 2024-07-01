import { createApp } from "vue";
import App from "./App.vue";
import axiosSetup from "./axios";
import Plotly from "plotly.js-dist-min";

const app = createApp(App);
app.use(axiosSetup);
app.config.globalProperties.$Plotly = Plotly;
app.mount("#app");
