<template>
  <div>
    <chart-visible />
    <br/>
    <report-visible />
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import ChartVisible from './ChartVisible'
import ReportVisible from './ReportVisible'

export default {
  name: 'charts',
  components: { VaChart, ChartVisible, ReportVisible },
  data () {
    return {
    }
  },
  created () {
  },
  methods: {

  },
}

</script>
