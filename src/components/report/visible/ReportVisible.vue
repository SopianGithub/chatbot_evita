<template>
  <va-card :title="$t('Report Log Visbility')">
    <div class="mb-3" v-if="isSuccess">
      <va-notification closeable>
        <va-badge>
          {{ $t('notificationsPage.notifications.success') }}
        </va-badge>
        {{ $store.state.app.msgNotification }}
      </va-notification>
    </div>

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
        <va-button v-if="!props.rowData.isResponse" flat small color="danger" @click="mapping(props.rowData)" class="ma-0">
          <va-icon name="fa fa-sitemap icon-left input-icon"/> {{ $t('Mapping') }}
          <va-button v-if="props.rowData.isMapped" flat small color="warning" class="ma-0">
            <va-icon v-if="props.rowData.isPossibleMap" name="fa fa-check-circle icon-left input-icon"/>
            <va-icon v-else="props.rowData.isPossibleMap" name="fa fa-times-circle icon-left input-icon"/>
          </va-button>
        </va-button>
        <va-button v-else flat small color="primary" class="ma-0">
          <va-icon name="fa fa-check-circle icon-left input-icon"/>
        </va-button>
      </template>
    </va-data-table>

    <va-modal
      v-model="showModal"
      :fullscreen="true"
      okText="Save Mapping"
      @ok="saveMapping"
      @cancel="onCancel"
    >
      <template slot="header">
        <h2 class="flex-center row">Mapping Parameter Chatbot</h2>
      </template>
      <slot>
        <div v-html="message"></div>
        <div class="row">
          <div class="flex xs6 offset--xs3">
            <va-toggle
              v-model="isCanMap"
              small
              label="Possible To Mapping?"
            />
          </div>
        </div>
        <div v-if="isCanMap" id="category">
          <fieldset>
            <va-radio-button
              option="Customer"
              v-model="selectedCategory"
              label="Corporate Customer"
            />
            <va-radio-button
              option="PIC"
              v-model="selectedCategory"
              label="PIC Employee"
            />
            <va-radio-button
              option="Product"
              v-model="selectedCategory"
              label="Product & Solusi"
            />
          </fieldset>

          <v-select multiple v-model="selectedData" label="name" :filterable="false" :options="options" @search="onSearch">
            <template slot="no-options">
              Cari Data Berdasarkan Kategori
            </template>
            <template slot="option" slot-scope="option">
              <div class="d-center" v-if="selectedCategory=='PIC'">
                {{ option.nik }} - {{ option.name }} || {{ option.unit }} - {{ option.sub_unit }}
              </div>
              <div class="d-center" v-else-if="selectedCategory=='Product'">
                {{ option.name }}
              </div>
              <div class="d-center" v-else-if="selectedCategory=='Customer'">
                {{ option.name }}
              </div>
            </template>
            <template slot="selected-option" slot-scope="option">
              <div class="selected d-center" v-if="selectedCategory=='PIC'">
                {{ option.name }} || {{ option.unit }} - {{ option.sub_unit }}
              </div>
              <div class="selected d-center" v-else-if="selectedCategory=='Product'">
                {{ option.name }} - {{ option.desc }}
              </div>
              <div class="selected d-center" v-else-if="selectedCategory=='Customer'">
                {{ option.name }} - {{ option.segmen }}
              </div>
            </template>
          </v-select>
          <br/>
          <div class="row">
            <va-input
              v-model="params_input"
              placeholder="Input Alias"
            >
              <va-icon
                slot="prepend"
                color="gray"
                name="fa fa-keyboard"
              />
            </va-input>
          </div>
        </div>
      </slot>
    </va-modal>
  </va-card>
</template>

<script>
import axios from 'axios'
import { debounce } from 'lodash'

export default {
  name: 'report-visible',
  data () {
    return {
      perPage: 10,
      totalPages: 0,
      perPageOptions: ['5', '10', '20', '50'],
      items: [],
      loading: false,
      messageNotif: '',
      isSuccess: false,
      isCanMap: false,
      showModal: false,
      message: '',
      selectedCategory: '',
      options: [],
      logs_selected: [],
      params_input: '',
      selectedData: [],
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
        name: 'parameter',
        title: this.$t('Parameter'),
        width: '20%',
      }, {
        name: 'isResponse',
        title: this.$t('Response'),
      }, {
        name: 'idTelegram',
        title: this.$t('ID Telegram'),
      }, {
        name: '__slot:actions',
        dataClass: 'text-right',
      }]
    },
  },
  created () {
    this.readItems()
  },
  methods: {
    readItems (page = 1) {
      this.loading = true
      const params = {
        limit: this.perPage,
        offset: (page != 1 && page != 0) ? ((page - 1) * this.perPage) : 0,
      }

      axios.get('http://localhost:5000/report/page_answered', { params })
        .then(response => {
          this.items = response.data.values.data
          this.totalPages = Math.ceil(response.data.values.total_pages / this.perPage)
          this.loading = false
        })
    },
    mapping (logs) {
      const arr_context = {
        pic_page: 'PIC',
        customer_page: 'Customer',
        product_page: 'Product',
      }
      this.showModal = true
      this.message = this.contentModal(logs)
      this.selectedCategory = arr_context[logs.context]
      this.params_input = logs.parameter.params
    },
    contentModal (logs) {
      this.logs_selected = logs
      const arr_context = {
        pic_page: 'PIC Employee',
        customer_page: 'Customer',
        product_page: 'Product & Solusi',
        am_page: 'Account Manager',
      }
      return `
        <div class="row">
          <label class="flex xs6">
            Intent
          </label>
          <div class="flex xs6">
            ${logs.intent}
          </div>
        </div>
        <div class="row">
          <label class="flex xs6">
            Parameter
          </label>
          <div class="flex xs6">
            ${JSON.stringify(logs.parameter)}
          </div>
        </div>
        <div class="row">
          <label class="flex xs6">
            Konteks
          </label>
          <div class="flex xs6">
            ${arr_context[logs.context]}
          </div>
        </div>
        <hr/>
      `
    },
    saveMapping () {
      axios.post(`http://localhost:5000/report/update_logs/${this.logs_selected.id}`, {
        possible: this.isCanMap,
      }).then((res) => {
        if (res.data.values == 'Success') {
          this.readItems()
          this.messageNotif = 'Mapping Berhasil Disimpan'
        }
      })

      if (this.isCanMap) {
        if (this.logs_selected.context == 'pic_page') {
          axios.post('http://localhost:5000/report/update_pic', {
            parameter: this.params_input,
            loker: this.selectedData,
          }).then((res) => {
            if (res.status === 200) {
              this.$store.commit('set_notif', 'Mapping Berhasil Disimpan')
              this.messageNotif = 'Mapping Berhasil Disimpan'
              this.readItems()
            } else {
              this.$store.commit('set_notif', 'Mapping Gagal Disimpan')
              this.messageNotif = 'Mapping Gagal Disimpan'
            }
          })
        } else if (this.logs_selected.context == 'product_page') {
          axios.post('http://localhost:5000/report/update_product', {
            parameter: this.params_input,
            product: this.selectedData,
          }).then((res) => {
            if (res.status === 200) {
              this.$store.commit('set_notif', 'Mapping Berhasil Disimpan')
              this.messageNotif = 'Mapping Berhasil Disimpan'
              this.readItems()
            } else {
              this.$store.commit('set_notif', 'Mapping Gagal Disimpan')
              this.messageNotif = 'Mapping Gagal Disimpan'
            }
          })
        } else {
          axios.post('http://localhost:5000/report/update_customer', {
            parameter: this.params_input,
            customers: this.selectedData,
          }).then((res) => {
            if (res.status === 200) {
              this.$store.commit('set_notif', 'Mapping Berhasil Disimpan')
              this.messageNotif = 'Mapping Berhasil Disimpan'
              this.readItems()
            } else {
              this.$store.commit('set_notif', 'Mapping Gagal Disimpan')
              this.messageNotif = 'Mapping Gagal Disimpan'
            }
          })
        }
      } else {
        this.$store.commit('set_notif', 'Unmapping Berhasil Disimpan')
        this.messageNotif = 'Unmapping Berhasil Disimpan'
      }

      this.isSuccess = true
      setTimeout(() => {
        this.messageNotif = ''
        this.isSuccess = false
      }, 10000)

      this.onCancel()
    },
    onCancel () {
      this.logs_selected = []
      this.selectedCategory = ''
      this.message = ''
    },
    onSearch (search, loading) {
      if (search.length) {
        loading(true)
        this.search(loading, search, this)
      }
    },
    search: _.debounce((loading, search, vm) => {
      axios.get(`http://localhost:5000/report/searching?search=${search}&category=${vm.selectedCategory}`)
        .then(res => {
          vm.options = res.data.values.items
          loading(false)
        })
    }, 350),
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
