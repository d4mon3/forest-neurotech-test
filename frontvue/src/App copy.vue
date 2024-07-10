<template>
  <div id="app">
    <div>
      <label for="plot-type">Plot Type:</label>
      <select v-model="plotType" @change="fetchPlot">
        <option value="scatter">Scatter Plot</option>
        <option value="histogram">Histogram</option>
        <option value="barplot">Bar Plot</option>

      </select>
    </div>
    <div>
      <label for="flipper-length">Flipper Length:</label>
      <input
        type="range"
        v-model="flipperLengthMin" :min="flipperLengthRange.min" :max="flipperLengthRange.max" @input="fetchPlot"
      />
      <span>{{ flipperLengthMin }} - {{ flipperLengthRange.max }} mm</span>
    </div>
    <div>
      <label for="bodyMass">Body Mass:</label>
      <input
        type="range" id="bodyMass" v-model="bodyMassMin"
        @input="fetchPlot" :min="bodyMassRange.min" :max="bodyMassRange.max"
      />
      <span>{{ bodyMassMin }} - {{ bodyMassRange.max }} kg</span>
    </div>
    <div id="plot"></div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      plotType: "scatter",
      flipperLengthMin: 0,
      flipperLengthRange: { min: 0, max: 230 },
      bodyMassMin: 0,
      bodyMassRange: { min: 0, max: 6500 },
    };
  },
  methods: {
    async fetchPlot() {
      try {
        const response = await this.$http.get(`http://localhost:5000/plot`, {
          params: {
            type: this.plotType,
            flipper_length_min: this.flipperLengthMin,
            flipper_length_max: this.flipperLengthRange.max,
            body_mass_min: this.bodyMassMin,
            body_mass_max: this.bodyMassRange.max,
          },
        });
        this.$Plotly.newPlot("plot", response.data.data, response.data.layout);
      } catch (error) {
        console.error("There was an error fetching the plot!", error);
      }
    },
    async fetchMinMaxValues() {
      try {
        const response = await this.$http.get('http://localhost:5000/get_min_max_values');
        const data = response.data;
        this.flipperLengthRange.min = data.flipper_length_min;
        this.flipperLengthRange.max = data.flipper_length_max;
        this.bodyMassRange.min = data.body_mass_min;
        this.bodyMassRange.max = data.body_mass_max;
        this.flipperLengthMin = data.flipper_length_min;
        this.bodyMassMin = data.body_mass_min;
      } catch (error) {
        console.error("There was an error fetching the min and max values!", error);
      }
    }
  },
  mounted() {
    this.fetchMinMaxValues().then(() => {
      this.fetchPlot();
    });
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
  background-color: #f0f0f0;
  color: #333333;
  font-family: "Roboto", sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
  background-color: #f0f0f0;
}

label {
  color: #333333;
  margin-top: 10px;
  display: block;
}

select,
input[type="range"] {
  background-color: #c0c0c0;
  color: #333333;
  border: none;
  padding: 10px;
  border-radius: 5px;
  margin-top: 5px;
}

input[type="range"] {
  -webkit-appearance: none;
  width: 100%;
  height: 5px;
  background: #d0d0d0;
  outline: none;
  opacity: 0.7;
  transition: opacity 0.2s;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 15px;
  height: 15px;
  background: #666666;
  cursor: pointer;
  border-radius: 50%;
}

input[type="range"]::-moz-range-thumb {
  width: 15px;
  height: 15px;
  background: #666666;
  cursor: pointer;
  border-radius: 50%;
}

#plot {
  width: 100%;
  height: 600px;
  background-color: #f0f0f0;
}
</style>

