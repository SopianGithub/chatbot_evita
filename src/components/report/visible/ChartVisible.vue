<template>
  <div class="charts">
    <div class="row">
      <div class="flex md12 xs12">
        <va-card
          class="chart-widget"
          title="Log Chatbot Visibilty"
        >
          <va-chart :data="lineChartData" type="line"/>
        </va-card>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import { getLineAnsweredData } from '../../../data/charts/AnsweredData'

export default {
  name: 'chart-visible',
  components: { VaChart },
  data () {
    return {
    	valAnswered: [],
    	valNotAnwered: [],
      	lineChartData: getLineAnsweredData(this.$themes, this.labelchart, this.valueChart),
    }
  },
  created () {
    this.getCategory()
  },
  methods: {
  	async getCategory () {
  		await axios.get('http://localhost:5000/report/answered')
  			.then(response => {
	        if (response.status === 200) {
	        	this.valAnswered = []
	        	this.valNotAnwered = []
	        	const category = ['Corporate Customer', 'Account Manager', 'Product', 'PIC']
	        	for (var item in category) {
	        		this.valAnswered.push(response.data.values.Answered[category[item]])
	        	}
	        	for (var item in category) {
	        		this.valNotAnwered.push(response.data.values['Not Answered'][category[item]])
	        	}
	        	this.lineChartData = getLineAnsweredData(this.$themes, this.valAnswered, this.valNotAnwered)
	        } else {

	        }
        })
  	},
  },
}

</script>
