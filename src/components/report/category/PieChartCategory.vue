<template>
  <div class="charts">
    <div class="row">
      <div class="flex md12 xs12">
        <va-card
          class="chart-widget"
          title="Chart By Category"
        >
          <va-chart :data="pieChartData" type="pie"/>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import { getCategoryChart } from '../../../data/charts/CategoryData'

export default {
  name: 'pie-chart-category',
  components: { VaChart },
  data () {
    return {
    	labelchart: ['Corporate Customer', 'PIC', 'Product', 'Account Manager'],
    	valueChart: [2478, 5267, 734, 1233],
      	pieChartData: getCategoryChart(this.$themes, this.labelchart, this.valueChart),
    }
  },
  created () {
    this.getCategory()
  },
  methods: {
  	async getCategory () {
  		await axios.get('http://localhost:5000/report/category')
  			.then(response => {
	        if (response.status === 200) {
	        	// console.log(response.data.values)
	        	this.labelchart = []
	        	this.valueChart = []
	        	for (var item in response.data.values) {
	        		this.labelchart.push(item)
	        		this.valueChart.push(response.data.values[item])
	        	}
	        	this.pieChartData = getCategoryChart(this.$themes, this.labelchart, this.valueChart)
	        } else {

	        }
        })
  	},
  },
}

</script>
