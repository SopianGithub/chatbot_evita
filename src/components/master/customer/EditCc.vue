<template>
  <div class="form-elements">
    <div class="row">
      <div class="flex xs12">
        <va-card :title="$t('forms.inputs.title')">
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
                  v-model.number="nipnas"
                  type="number"
                  readonly
                  placeholder="Input Nipnas CC"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-address-card icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="nama"
                  placeholder="Input Nama CC"
                >
                  <template slot="prepend">
                    <va-icon name="fa fa-bank icon-left input-icon"/>
                  </template>
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-select
                  :label="$t('Pilih Segmen')"
                  v-model="selectSegmen"
                  textBy="name"
                  textValue="name"
                  :options="segmenOption"
                />
                <template slot="prepend">
                  <va-icon name="fa fa-book icon-left input-icon"/>
                </template>
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <label class="typo__label">Nama Alias CC</label>
                <multiselect v-model="aliasValue" tag-placeholder="Add Alias Name Of CC" placeholder="Input Alias CC" label="name" track-by="code" :options="optionsAlias" :multiple="true" :taggable="true" @tag="addTag" @remove="toggleUnSelectAlias"></multiselect>
              </div>
              <div class="flex">
                <va-button
                  type="submit"
                  class="my-0"
                >
                  Edit Corporate Customer</va-button>
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

export default {
  name: 'form-elements',
  data () {
    return {
      nipnas: '',
      nama: '',
      alias: '',
      isMale: true,
      savingSuccessful: true,
      messageNotif: '',
      isSuccess: false,
      segmenOption: [],
      selectSegmen: '',
      aliasValue: [],
      optionsAlias: [],
    }
  },
  created () {
    this.getSegmen()
    this.loadCC()
  },
  methods: {
    clear (field) {
      this[field] = ''
    },
    oninput () {
      this.savingSuccessful = false
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') { this.savingSuccessful = true }
    },
    getSegmen () {
      axios.get('http://localhost:5000/segmen')
        .then(response => {
          if (response.status === 200) {
            this.segmenOption = response.data.values
          } else {
            this.messageNotif = 'Terjadi Kesalahan Ketika Get Data Segmen'
          }
        })
    },
    loadCC () {
      this.nipnas = this.$route.params.id_cc
      const dataEdit = []
      axios.get(`http://localhost:5000/cc/${this.nipnas}`)
        .then(res => {
          if (res.status === 200) {
            this.nama = res.data.values[0].name
            this.selectSegmen = res.data.values[0].segmen
            const arr_alias = res.data.values[0].alias
            for (var i = 0; i < arr_alias.length; i++) {
              this.aliasValue.push({
                name: arr_alias[i], code: this.makeid(5),
              })
            }
            this.optionsAlias = this.aliasValue
          } else {
            this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
          }
        })
    },
    async onsubmit () {
      const params = {
        name: this.nama,
        segmen: this.selectSegmen,
        alias: this.optionsAlias.map(function (index, elem) {
          return index.name
        }),
      }
      if (this.nipnas !== '' && this.nama !== '' && this.segmen !== '') {
        await axios.put(`http://localhost:5000/cc/${this.nipnas}`, params)
          .then((res) => {
            if (res.status === 200) {
              this.messageNotif = 'Edit Data CC Berhasil'
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
    toggleUnSelectAlias ({ name, code }) {
      this.optionsAlias = this.optionsAlias.filter(function (index) {
        return index.name != name
      })
      this.aliasValue = this.optionsAlias
    },
    makeid (length) {
      var result = ''
      var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
      var charactersLength = characters.length
      for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength))
      }
      return result
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
