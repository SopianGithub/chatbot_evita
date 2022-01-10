<template>
  <va-card :title="$t('Report Log Product')">

    <va-data-table
      :fields="fields"
      :data="items"
      :loading="loading"
      :totalPages="totalPages"
      @page-selected="readItems"
      :per-page="parseInt(perPage)"
      api-mode
    >

      <template slot="actions" slot-scope="props">
        <!-- <va-button flat small color="info" @click="edit(props.rowData)" class="ma-0">
          <va-icon name="fa fa-pencil-square icon-left input-icon"/> {{ $t('tables.edit') }}
        </va-button> -->
      </template>
    </va-data-table>

  </va-card>
</template>

<script>
import axios from 'axios'
import { debounce } from 'lodash'

export default {
  name: 'report-category',
  data () {
    return {
      perPage: 10,
      totalPages: 0,
      perPageOptions: ['5', '10', '20', '50'],
      items: [],
      loading: false,
      messageNotif: '',
      isSuccess: false,
    }
  },
  computed: {
    fields () {
      return [{
        name: 'potretdate',
        title: this.$t('Potretdate'),
        width: '20%',
      }, {
        name: 'intent',
        title: this.$t('Intent'),
        width: '20%',
      }, {
        name: 'context',
        title: this.$t('Context'),
        width: '20%',
      }, {
        name: 'isResponse',
        title: this.$t('Response'),
      },,
        {
          name: 'idTelegram',
          title: this.$t('ID Telegram'),
        }]
    },
  },
  created () {
    this.readItems()
  },
  methods: {
    readItems (page = 1) {
      this.loading = true
      console.log(page)
      const params = {
        limit: this.perPage,
        offset: (page != 1 && page != 0) ? ((page - 1) * this.perPage) : 0,
      }

      axios.get('http://localhost:5000/report/page_catgeory', { params })
        .then(response => {
          this.items = response.data.values.data
          this.totalPages = Math.ceil(response.data.values.total_pages / this.perPage)
          this.loading = false
        })
    },
  },
}
</script>

<style lang="scss">
  .data-table-server-pagination---avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
</style>
