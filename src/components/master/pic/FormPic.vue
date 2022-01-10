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
                  v-model="nik"
                  type="number"
                  placeholder="Input NIK PIC"
                >
                  <va-icon
                    slot="prepend"
                    color="gray"
                    name="fa fa-bookmark"
                  />
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="nama"
                  placeholder="Input Nama PIC"
                >
                  <va-icon
                    slot="prepend"
                    color="gray"
                    name="fa fa-user"
                  />
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="mobile"
                  type="number"
                  placeholder="Input Nama No HP PIC"
                >
                  <va-icon
                    slot="prepend"
                    color="gray"
                    name="fa fa-phone"
                  />
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <treeselect v-model="divisi" :multiple="false" :options="optionsPIC" />
              </div>
              <div class="flex md12 sm12 xs12">
                <va-input
                  v-model="title"
                  placeholder="Input Title PIC"
                >
                  <va-icon
                    slot="prepend"
                    color="gray"
                    name="fa fa-id-card"
                  />
                </va-input>
              </div>
              <div class="flex md12 sm12 xs12">
                <va-select
                  v-model="bptype"
                  label="Band Type"
                  :options="bpOpt"
                  noClear
                />
              </div>
              <div class="flex md12 sm12 xs12">
                <label class="typo__label">Nama Alias Unit/PIC</label>
                <multiselect v-model="aliasValue" tag-placeholder="Add Alias Name Unit Or PIC" placeholder="Input Alias Unit/PIC" label="name" track-by="code" :options="optionsAlias" :multiple="true" :taggable="true" @tag="addTag"></multiselect>
              </div>
              <div class="flex">
                <va-button
                  type="submit"
                  class="my-0"
                >
                  Tambah PIC</va-button>
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
      nik: '',
      nama: '',
      mobile: '',
      isMale: true,
      savingSuccessful: true,
      messageNotif: '',
      isSuccess: false,
      divisi: null,
      title: null,
      bptype: null,
      bpOpt: ['I', 'II', 'III', 'IV', 'V', 'VI'],
      optionsPIC: [],
      aliasValue: [
        { name: 'Input Alias', code: 'xxxxx' },
      ],
      optionsAlias: [],
    }
  },
  created () {
    this.getLoker()
  },
  methods: {
    clear (field) {
      this[field] = ''
    },
    oninput () {
      this.savingSuccessful = false
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') { this.savingSuccessful = true }
    },
    getLoker () {
      axios.get('http://localhost:5000/employe/loker')
        .then(response => {
          this.optionsPIC = response.data.values
        })
    },
    async onsubmit () {
      const arr_div = this.divisi.split('||')
      const tmploker = {
        bp: this.bptype,
        title: this.title,
        divisi: arr_div[0],
        unit: (arr_div[2] != null) ? arr_div[2] : arr_div[0],
        sub_unit: (arr_div[3] != null) ? arr_div[3] : arr_div[0],
        alias: this.optionsAlias.map(function (index, elem) {
          return index.name
        }),
      }
      const params = [{
        nik: this.nik,
        name: this.nama,
        mobile: this.mobile,
        loker: tmploker,
      }]
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') {
        await axios.post('http://localhost:5000/employe/', params)
          .then((res) => {
            if (res.status === 200) {
              this.messageNotif = 'Input Data PIC Berhasil'
              this.isSuccess = true
              this.savingSuccessful = true
              setTimeout(() => {
                this.$router.push({ path: '/admin/master/pic' })
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
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style>
  .row.row-inside {
    max-width: none;
  }
</style>
