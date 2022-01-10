<template>
  <div class="charts">
    <chart-product />
    <br/>
    <report-product />
  </div>
</template>

<script>

import axios from 'axios'
import VaChart from '../../statistics/charts/va-charts/VaChart'
import ChartProduct from './ChartProduct'
import ReportProduct from './ReportProduct'
import { getProductChart } from '../../../data/charts/ProductChart'

export default {
  name: 'charts',
  components: { VaChart, ChartProduct, ReportProduct },
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
