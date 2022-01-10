<template>
  <va-card :title="$t('Master Data Corporate Customer')">
    <div class="mb-3" v-if="isSuccess">
      <va-notification closeable>
        <va-badge>
          {{ $t('notificationsPage.notifications.success') }}
        </va-badge>
        {{ messageNotif }}
      </va-notification>
    </div>
    <va-button
      @click="tambahCC"
    >
      <va-icon name="fa fa-plus icon-left input-icon"/> Add CC</va-button>
    <div class="row align--center">
      <div class="flex xs12 md6">
        <va-input
          :value="term"
          :placeholder="$t('tables.searchByName')"
          @input="search"
          removable
        >
          <va-icon name="fa fa-search" slot="prepend" />
        </va-input>
      </div>

      <div class="flex xs12 md3 offset--md3">
        <va-select
          v-model="perPage"
          :label="$t('tables.perPage')"
          :options="perPageOptions"
          noClear
          @input="readItems"
        />
      </div>
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
        <va-button flat small color="success" @click="addmapping(props.rowData)" class="ma-0">
          <va-icon name="fa fa-sitemap icon-left input-icon"/> {{ $t('AM') }}
        </va-button>

        <va-button flat small color="info" @click="edit(props.rowData)" class="ma-0">
          <va-icon name="fa fa-pencil-square icon-left input-icon"/>  {{ $t('tables.edit') }}
        </va-button>

        <va-button flat small color="danger" @click="remove(props.rowData)" class="ma-0">
          <va-icon name="fa fa-trash icon-left input-icon"/> {{ $t('tables.delete') }}
        </va-button>
      </template>
    </va-data-table>

    <va-modal
      v-model="showModalConfirm"
      :title=" $t('Konfirmasi Hapus CC') "
      cancelClass="Batal"
      :okText=" $t('Hapus')"
      @ok="deleteCC"
      :message=" $t('Apakah Anda Yakin Untuk Menghapus Data Ini?') "
      noOutsideDismiss
      noEscDismiss
    />

  </va-card>
</template>

<script>
import axios from 'axios'
import { debounce } from 'lodash'

import Mapping from './Mapping.vue'

export default {
  data () {
    return {
      perPageOptions: ['5', '10', '20', '50'],
      perPage: 10,
      totalPages: 0,
      items: [],
      loading: false,
      term: null,
      showModalConfirm: false,
      selectedID: '',
      savingSuccessful: true,
      messageNotif: '',
      isSuccess: false,
      modalHeaderproduct: '',
      modalDetailContent: '',
      selectedAM: [],
      isLoadingSearchAM: false,
      listAM: [],
    }
  },
  computed: {
    fields () {
      return [{
        name: 'id_cc',
        title: this.$t('NIPNAS'),
        width: '20%',
      }, {
        name: 'name',
        title: this.$t('Nama CC'),
        width: '20%',
      }, {
        name: 'segmen',
        title: this.$t('Segmen'),
      }, {
        name: 'alias',
        title: this.$t('Nama Alias'),
      },,
        {
          name: '__slot:actions',
          dataClass: 'text-right',
        }]
    },
  },
  created () {
    this.readItems()
  },
  methods: {
    readItems (page = 1, search = null) {
      this.loading = true

      let filterTerm = this.term
      filterTerm = search != null ? search : filterTerm

      const params = {
        limit: this.perPage,
        offset: (page != 1 && page != 0) ? ((page - 1) * this.perPage) : 0,
        filter: filterTerm != null ? filterTerm : '',
      }

      axios.get('http://localhost:5000/cc/page', { params })
        .then(response => {
          this.items = response.data.values.data
          this.totalPages = Math.ceil(response.data.values.total_pages / this.perPage)
          this.loading = false
        })
    },
    edit (user) {
      this.$router.push({ path: '/admin/master/edit_cc/' + user.id_cc })
      // alert('Edit CC: ' + JSON.stringify(user))
    },
    remove (user) {
      this.showModalConfirm = true
      this.selectedID = user.id_cc
      // const idx = this.users.findIndex(u => u.id === user.id)
      // this.users.splice(idx, 1)
    },
    search: debounce(function (term) {
      this.term = term
      this.readItems(0, this.term)
    }, 400),
    tambahCC () {
      this.$router.push({ path: '/admin/master/add_cc' })
    },
    async deleteCC () {
      await axios.delete(`http://localhost:5000/cc/${this.selectedID}`)
        .then(response => {
          if (response.status === 200) {
            this.messageNotif = 'Hapus Data CC Berhasil'
            this.isSuccess = true
            this.savingSuccessful = true
            setTimeout(() => {
              this.messageNotif = ''
              this.isSuccess = false
              this.savingSuccessful = false
              this.readItems()
            }, 3000)
          } else {
            this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
          }
        })
    },
    addmapping (user) {
      this.$router.push({ path: '/admin/master/mapping/' + user.id_cc })
    },
    mapping (cc) {
      this.$modal.show(
        {
          template: `
            <div>
              <p class="display-4 va-modal__header">{{ title }}</p>
              <hr/>
              <p class="va-modal__message">
                <multiselect v-model="selectedAM" id="ajax" label="name" track-by="nik" placeholder="Type to search" open-direction="bottom" :options="listAM" :multiple="true" :searchable="true" :loading="isLoadingSearchAM" :internal-search="false" :clear-on-select="false" :close-on-select="false" :options-limit="300" :limit="3" :limit-text="limitText" :max-height="600" :show-no-results="false" :hide-selected="true" @search-change="asyncFind">
                    <template slot="tag" slot-scope="{ option, remove }"><span class="custom__tag"><span>{{ option.name }}</span><span class="custom__remove" @click="remove(option)">❌</span></span></template>
                    <template slot="clear" slot-scope="props">
                      <div class="multiselect__clear" v-if="selectedAM.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
                    </template><span slot="noResult">Oops! No elements found. Consider changing the search query.</span>
                  </multiselect>
              </p>
            </div>
          `,
          props: ['title', 'selectedAM', 'listAM', 'isLoadingSearchAM', 'limitText', 'asyncFind', 'clearAll'],
        },
        {
          title: cc.name,
          selectedAM: this.selectedAM,
          isLoadingSearchAM: this.isLoadingSearchAM,
          listAM: this.listAM,
          limitText: this.limitText,
          asyncFind: this.asyncFind,
          clearAll: this.clearAll,
        },
        {
          width: 500,
          height: 500,
        },
        { 'before-close': event => {} },
      )
    },
    async asyncFind (query) {
      this.isLoadingSearchAM = true
      await axios.get(`http://localhost:5000/ams/search/${query}`)
        .then(response => {
          if (response.status === 200) {
            const dataam = response.data.values
            Object.entries(dataam).forEach(([key, user]) => {
              this.listAM[key] = dataam[key]
            })
            this.isLoadingSearchAM = false
            this.getListAM()
          }
        })
    },
    limitText (count) {
      return `and ${count} other AM`
    },
    clearAll () {
      this.selectedAM = []
    },
    getListAM () {
      console.log(this.listAM)
      // if (typeof (this.listAM) === 'object') {
      //   console.log(JSON.parse(JSON.stringify(this.listAM)))
      // }
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
