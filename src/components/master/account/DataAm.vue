<template>
  <va-card :title="$t('Master Data Account Manager')">
    <div class="mb-3" v-if="isSuccess">
      <va-notification closeable>
        <va-badge>
          {{ $t('notificationsPage.notifications.success') }}
        </va-badge>
        {{ messageNotif }}
      </va-notification>
    </div>
    <va-button
      @click="tambahAM"
    >
      Tambah AM</va-button>
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
        <va-button flat small color="info" @click="edit(props.rowData)" class="ma-0">
          <va-icon name="fa fa-pencil-square icon-left input-icon"/> {{ $t('tables.edit') }}
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

export default {
  data () {
    return {
      perPage: 10,
      totalPages: 0,
      perPageOptions: ['5', '10', '20', '50'],
      items: [],
      loading: false,
      term: null,
      showModalConfirm: false,
      selectedID: '',
      savingSuccessful: true,
      messageNotif: '',
      isSuccess: false,
    }
  },
  computed: {
    fields () {
      return [{
        name: 'nik',
        title: this.$t('NIK'),
        width: '20%',
      }, {
        name: 'name',
        title: this.$t('tables.headings.name'),
        width: '20%',
      }, {
        name: 'mobile',
        title: this.$t('No. Telp'),
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

      axios.get('http://localhost:5000/ams/page', { params })
        .then(response => {
          this.items = response.data.values.data
          this.totalPages = Math.ceil(response.data.values.total_pages / this.perPage)
          this.loading = false
        })
    },
    edit (user) {
      this.$router.push({ path: '/admin/master/edit_am/' + user.nik })
    },
    remove (user) {
      this.showModalConfirm = true
      this.selectedID = user.nik
    },
    search: debounce(function (term) {
      this.term = term
      this.readItems(0, this.term)
    }, 400),
    tambahAM () {
      this.$router.push({ path: '/admin/master/add_account' })
    },
    async deleteCC () {
      await axios.delete(`http://localhost:5000/ams/${this.selectedID}`)
        .then(response => {
          if (response.status === 200) {
            this.messageNotif = 'Hapus Data AM Berhasil'
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
