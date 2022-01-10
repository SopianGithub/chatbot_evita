<template>
  <va-card :title="$t('Master Data Produk')" class="elm-product">
    <div class="mb-3" v-if="isSuccess">
      <va-notification closeable>
        <va-badge>
          {{ $t('notificationsPage.notifications.success') }}
        </va-badge>
        {{ messageNotif }}
      </va-notification>
    </div>
    <va-button
      @click="tambaProduct"
    >
      <va-icon name="fa fa-plus icon-left input-icon"/> Add Produk</va-button>
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
          @click="readItems"
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
        <va-button flat small color="info" @click="detailProd(props.rowData)" class="ma-0">
          <va-icon name="fa fa-sign-in icon-left input-icon"/>  {{ $t('Detail') }}
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
      :title=" $t('Konfirmasi Hapus Product') "
      cancelClass="Batal"
      :okText=" $t('Hapus')"
      @ok="deleteProduct"
      :message=" $t('Apakah Anda Yakin Untuk Menghapus Data Ini?') "
      noOutsideDismiss
      noEscDismiss
    />

    <modal name="detail-produk-modal"></modal>
  </va-card>

</template>

<script>
import axios from 'axios'
import { debounce } from 'lodash'

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
      showModalDetProduk: false,
      modalHeaderproduct: '',
      modalDetailContent: '',
    }
  },
  computed: {
    fields () {
      return [{
        name: 'name',
        title: this.$t('Nama Produk'),
        width: '80%',
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
    readItems (page = 1, search = null) {
      this.loading = true

      let filterTerm = this.term
      filterTerm = search != null ? search : filterTerm

      const params = {
        limit: this.perPage,
        offset: (page != 1 && page != 0) ? ((page - 1) * this.perPage) : 0,
        filter: filterTerm != null ? filterTerm : '',
      }

      axios.get('http://localhost:5000/product/page', { params })
        .then(response => {
          this.items = response.data.values.data
          this.totalPages = Math.ceil(response.data.values.total_pages / this.perPage)
          this.loading = false
        })
    },
    edit (user) {
      this.$router.push({ path: '/admin/master/edit_product/' + user.id })
      // alert('Edit CC: ' + JSON.stringify(user))
    },
    remove (user) {
      this.showModalConfirm = true
      this.selectedID = user.id
      // const idx = this.users.findIndex(u => u.id === user.id)
      // this.users.splice(idx, 1)
    },
    search: debounce(function (term) {
      this.term = term
      this.readItems(0, this.term)
    }, 400),
    tambaProduct () {
      this.$router.push({ path: '/admin/master/add_product' })
    },
    async deleteProduct () {
      await axios.delete(`http://localhost:5000/product/${this.selectedID}`)
        .then(response => {
          if (response.status === 200) {
            this.messageNotif = 'Hapus Data Produk Berhasil'
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
    detailProd (product) {
      // this.showModalDetProduk = true
      this.modalHeaderproduct = product.name
      this.modalDetailContent = this.elmProd(product)

      this.$modal.show(
        {
          template: `
            <div class="modal-custom-content va-modal__inner ">
              <p class="display-4 va-modal__header">{{ header }}</p>
              <hr/>
              <p v-html="content" class="va-modal__message"></p>
            </div>
          `,
          props: ['header', 'content'],
        },
        { header: product.name, content: this.elmProd(product) },
        { height: 'auto' },
        { 'before-close': event => {} },
      )
    },
    elmProd (product) {
      let elm_file = '<ul class="va-unordered">'
      elm_file += product.productfile.map(function (index, elem) {
        return `
          <li>
            <ul>
              <li>${index.type_file}</li>
              <li><a href="${index.url_file}" target="_blank">${index.url_file}</a></li>
            </ul>
          </li>
        `
      })
      elm_file += '</ul>'

      return `<p class="display-6">Nama Alias Produk : </p>
              <p>${product.alias ? product.alias : '-'}</p>

              <p class="display-6">Deskripsi Produk</p>
              <p>${product.desc}</p>

              <p class="display-6">File Pendukung</p>
              <p>${elm_file}</p>`
    },
  },
}
</script>

<style lang="scss">
  .elm-product {
    .data-table-server-pagination---avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }

    .modal-custom-content {
      padding: 5px;
    }
  }
</style>
