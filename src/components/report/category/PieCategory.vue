<template>
  <div class="charts">
    <pie-chart-category />
    <br/>
    <report-category />
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import PieChartCategory from './PieChartCategory'
import ReportCategory from './ReportCategory'
import { getCategoryChart } from '../../../data/charts/CategoryData'

export default {
  name: 'charts',
  components: { VaChart, PieChartCategory, ReportCategory },
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
