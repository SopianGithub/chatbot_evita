<template>
  <div class="dashboard">
    <div class="row">
      <div class="xs12">
        <chart-visible />
      </div>
    </div>
    <br/>
    <div class="row">
      <div class="xs6">
        <pie-chart-category />
      </div>
      <div class="xs6">
        <chart-product />
      </div>
    </div>
  </div>
</template>

<script>

import ChartVisible from '../report/visible/ChartVisible'
import PieChartCategory from '../report/category/PieChartCategory'
import ChartProduct from '../report/product/ChartProduct'

export default {
  name: 'dashboard',
  components: {
    ChartVisible,
    PieChartCategory,
    ChartProduct,
  },
  methods: {

  },
}
</script>

<style lang="scss">
  .row-equal .flex {
    .va-card {
      height: 100%;
    }
  }

  .dashboard {
    .va-card {
      margin-bottom: 0 !important;
    }
  }
</style>
