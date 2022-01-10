<template>
  <div class="form-elements">
    <div class="row">
      <div class="flex xs12">
        <va-card :title="$t('FORM INPUT PRODUK')">
          <div class="mb-3" v-if="isSuccess">
            <va-notification closeable>
              <va-badge>
                {{ $t('notificationsPage.notifications.success') }}
              </va-badge>
              {{ messageNotif }}
            </va-notification>
          </div>
          <div class="mb-3" v-if="!savingSuccessful">
            <va-notification color="danger" closeable @click="removeNotif">
              <va-badge color="danger" >
                {{ $t('notificationsPage.notifications.danger') }}
              </va-badge>
              {{ messageNotif }}
            </va-notification>
          </div>
          <form @submit.prevent="onsubmit" >
            <div class="row">
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="nama"
                  placeholder="Input Nama Produk"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-shopping-bag icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="descr"
                  placeholder="Input Deskripsi Product"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-newspaper-o icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="benefit"
                  placeholder="Input Benefit Product"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-briefcase icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
            </div>
            <div class="row">
              <div class="flex md12 sm12 xs12">
                <label class="typo__label">Nama Alias Produk</label>
                <multiselect v-model="aliasValue" tag-placeholder="Add Alias Name Of Product" placeholder="Input Nama Alias Produk" label="name" track-by="code" :options="optionsAlias" :multiple="true" :taggable="true" @tag="addTag"></multiselect>
              </div>
            </div>
            <div class="row">
              <div class="flex xs12">
                <va-select
                  :label="$t('Pilih Tipe File Produk')"
                  v-model="selectTypeFile"
                  textBy="name"
                  textValue="name"
                  :options="kindOfFileOption"
                  icon="fa fa-book"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-book icon-left input-icon"/>
                  </template>
                </va-select>
              </div>
            </div>
            <div class="row">
              <div class="flex xs10">
                <va-input
                  v-model="urlFile"
                  placeholder="Input Link File"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-link icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
              <div class="flex xs2">
                <va-button
                  small outline
                  color="info"
                  icon="fa fa-plus-circle"
                  type="button"
                  class="my-0"
                  @click="addElmLink"
                />
              </div>
            </div>
            <div>
              <product-files
                v-for="(component, index) in elmFileInput"
                :key="index"
                :indexArr="index"
                :is="component"
                :kindOfFileOption="kindOfFileOption"
                @update-type-file="appendTypeFile"
                @remove-elm-file="removeTypeFile"
                @update-url-file="appendUrlFile"
              />
            </div>
            <div class="row">
              <div class="flex">
                <va-button
                  type="submit"
                  class="my-0"
                >
                  Tambah Produk</va-button>
              </div>
            </div>
          </form>
        </va-card>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ProductFiles from './ProductFiles'

export default {
  name: 'add-product',
  components: {
    ProductFiles,
  },
  data () {
    return {
      descr: '',
      nama: '',
      alias: '',
      benefit: '',
      savingSuccessful: true,
      messageNotif: '',
      isSuccess: false,
      kindOfFileOption: ['PROPOSAL', 'MARKETING COLLATERAL (EXTERNAL)', 'INFO PRODUK (INTERNAL)', 'OTHERS'],
      selectTypeFile: 'PROPOSAL',
      urlFile: 'http://',
      selectTypeFileArr: [],
      urlFileArr: [],
      aliasValue: [
        { name: 'Input Alias', code: 'xxxxx' },
      ],
      optionsAlias: [],
      elmFileInput: [],
    }
  },
  created () {

  },
  methods: {
    clear (field) {
      this[field] = ''
    },
    oninput () {
      this.savingSuccessful = false
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') { this.savingSuccessful = true }
    },
    async onsubmit () {
      const params = [{
        id_cc: this.nipnas,
        name: this.nama,
        segmen: this.selectSegmen,
        alias: this.optionsAlias.map(function (index, elem) {
          return index.name
        }),
      }]
      if (this.nipnas !== '' && this.nama !== '' && this.segmen !== '') {
        await axios.post('http://localhost:5000/cc/', params)
          .then((res) => {
            if (res.status === 200) {
              this.messageNotif = 'Input Data CC Berhasil'
              this.isSuccess = true
              this.savingSuccessful = true
              setTimeout(() => {
                this.$router.push({ path: '/admin/master/customer' })
              }, 1000)
            } else {
              this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
            }
          })
      } else {
        this.savingSuccessful = false
        this.isSuccess = false
        this.messageNotif = 'Harap Diisi Semua Inputan'
      }
    },
    removeNotif () {
      this.savingSuccessful = true
    },
    addTag (newTag) {
      const tag = {
        name: newTag,
        code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000)),
      }
      this.optionsAlias.push(tag)
      this.aliasValue.push(tag)
    },
    addElmLink () {
      this.elmFileInput.push(ProductFiles)
    },
    appendUrlFile (index, arrUrl) {
      this.urlFileArr[index] = arrUrl
    },
    appendTypeFile (index, arrFile) {
      this.selectTypeFileArr[index] = arrFile
    },
    removeTypeFile (indexElm) {
      console.log(this.elmFileInput)
      this.elmFileInput.splice(indexElm, 1)
      this.selectTypeFileArr.splice(indexElm, 1)
      this.urlFileArr.splice(indexElm, 1)
    },
    getFileProd () {
      this.selectTypeFileArr.push(this.selectTypeFile)
      this.urlFileArr.push(this.urlFile)
      const ObjFiles = []
      for (var i = 0; i < this.selectTypeFileArr.length; i++) {
        ObjFiles[i] = {
          type_file: this.selectTypeFileArr[i],
          url_file: this.urlFileArr[i],
        }
      }
      const FileProdProposal = ObjFiles.filter(function (index, elem) {
        if (index.type_file == 'PROPOSAL') { return index }
      }).map(({ url_file }) => url_file)
      const FileProdExt = ObjFiles.filter(function (index, elem) {
        if (index.type_file == 'MARKETING COLLATERAL (EXTERNAL)') { return index }
      }).map(({ url_file }) => url_file)
      const FileProdInt = ObjFiles.filter(function (index, elem) {
        if (index.type_file == 'INFO PRODUK (INTERNAL)') { return index }
      }).map(({ url_file }) => url_file)
      const FileProdOth = ObjFiles.filter(function (index, elem) {
        if (index.type_file == 'OTHERS') { return index }
      }).map(({ url_file }) => url_file)
      const productFilesArr = []
      if (FileProdProposal.length > 0) productFilesArr.push({ type_file: 'PROPOSAL', url_file: FileProdProposal })
      if (FileProdExt.length > 0) productFilesArr.push({ type_file: 'MARKETING COLLATERAL (EXTERNAL)', url_file: FileProdExt })
      if (FileProdInt.length > 0) productFilesArr.push({ type_file: 'INFO PRODUK (INTERNAL)', url_file: FileProdInt })
      if (FileProdOth.length > 0) productFilesArr.push({ type_file: 'OTHERS', url_file: FileProdOth })

      return productFilesArr
    },
    async onsubmit () {
      const params = [{
        name: this.nama,
        desc: this.descr,
        benefit: this.benefit,
        alias: this.optionsAlias.map(function (index, elem) {
          return index.name
        }),
        files: this.getFileProd(),
      }]
      if (this.name !== '' && this.descr !== '') {
        await axios.post('http://localhost:5000/product/', params)
          .then((res) => {
            if (res.status === 200) {
              this.messageNotif = 'Input Data Produk Berhasil'
              this.isSuccess = true
              this.savingSuccessful = true
              setTimeout(() => {
                this.$router.push({ path: '/admin/master/product' })
              }, 1000)
            } else {
              this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
            }
          })
      } else {
        this.savingSuccessful = false
        this.isSuccess = false
        this.messageNotif = 'Harap Diisi Semua Inputan'
      }
    },
  },
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
  .row.row-inside {
    max-width: none;
  }
</style>
