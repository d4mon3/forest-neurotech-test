<template>
  <div id="app">
    <div>
      <label for="plot-type">Plot Type:</label>
      <select v-model="plotType" @change="fetchPlot">
        <option value="scatter">Scatter Plot</option>
        <option value="histogram">Histogram</option>
      </select>
    </div>
    <div>
      <label for="flipper-length">Flipper Length:</label>
      <input type="range" v-model="flipperLengthMin" :min="0" :max="flipperLengthMax" @input="fetchPlot">
      <span>{{ flipperLengthMin }} - {{ flipperLengthMax }} mm</span>
    </div>
    <div id="plot"></div>
    <div id="summary">
      <h2>Summary Statistics</h2>
      <div v-if="summary">
        <div v-for="(stats, species) in summary" :key="species">
          <h3>{{ species }}</h3>
          <pre>{{ stats }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      plotType: 'scatter',
      summary: null,
      flipperLengthMin: 0,
      flipperLengthMax: 230,
    };
  },
  methods: {
    async fetchPlot() {
      try {
        const response = await this.$http.get(`http://localhost:5000/plot`, {
          params: {
            type: this.plotType,
            flipper_length_min: this.flipperLengthMin,
            flipper_length_max: this.flipperLengthMax,
          }
        });
        this.$Plotly.newPlot('plot', response.data.data, response.data.layout);
      } catch (error) {
        console.error("There was an error fetching the plot!", error);
      }
    },
    async fetchSummary() {
      try {
        const response = await this.$http.get('http://localhost:5000/summary');
        this.summary = response.data;
      } catch (error) {
        console.error("There was an error fetching the summary statistics!", error);
      }
    },
  },
  mounted() {
    this.fetchPlot();
    this.fetchSummary();
  },
};
</script>

<style>
#plot {
  width: 100%;
  height: 600px;
}
#summary {
  margin-top: 20px;
}
</style>