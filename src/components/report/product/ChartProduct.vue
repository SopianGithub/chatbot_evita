<template>
  <div class="charts">
    <div class="row">
      <div class="flex md12 xs12">
        <va-card
          class="chart-widget"
          title="Chart Trend Product"
        >
          <va-chart :data="productChartData" type="donut"/>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import { getProductChart } from '../../../data/charts/ProductChart'

export default {
  name: 'chart-product',
  components: { VaChart },
  data () {
    return {
    	labelchart: ['North Americas', 'South America', 'Australia'],
    	valueChart: [2478, 5267, 734],
      	productChartData: getProductChart(this.$themes, this.labelchart, this.valueChart),
    }
  },
  created () {
    this.getStatProduct()
  },
  methods: {
  	async getStatProduct () {
  		await axios.get('http://localhost:5000/report/product')
  			.then(response => {
	        if (response.status === 200) {
	        	// console.log(response.data.values)
	        	this.labelchart = []
	        	this.valueChart = []
	        	for (var item in response.data.values) {
	        		this.labelchart.push(item)
	        		this.valueChart.push(response.data.values[item])
	        	}
	        	this.productChartData = getProductChart(this.$themes, this.labelchart, this.valueChart)
	        	console.log(this.productChartData)
	        } else {

	        }
        })
  	},
  },
}

</script>
