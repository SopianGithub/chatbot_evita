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
                  placeholder="Input NIK AM"
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
                  placeholder="Input Nama AM"
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
                  placeholder="Input Nama No HP"
                >
                  <va-icon
                    slot="prepend"
                    color="gray"
                    name="fa fa-phone"
                  />
                </va-input>
              </div>
              <div class="flex">
                <va-button
                  type="submit"
                  class="my-0"
                >
                  Edit AM</va-button>
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
    }
  },
  created () {
    this.loadAM()
  },
  methods: {
    clear (field) {
      this[field] = ''
    },
    oninput () {
      this.savingSuccessful = false
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') { this.savingSuccessful = true }
    },
    loadAM () {
      this.nik = this.$route.params.id
      axios.get(`http://localhost:5000/ams/${this.nik}`)
        .then(res => {
          if (res.status === 200) {
            this.nama = res.data.values[0].name
            this.mobile = res.data.values[0].mobile
          } else {
            this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
          }
        })
    },
    async onsubmit () {
      const params = {
        name: this.nama,
        mobile: this.mobile,
      }
      if (this.nik !== '' && this.name !== '' && this.mobile !== '') {
        await axios.put(`http://localhost:5000/ams/${this.nik}`, params)
          .then((res) => {
            if (res.status === 200) {
              this.messageNotif = 'Ubah Data AM Berhasil'
              this.isSuccess = true
              this.savingSuccessful = true
              setTimeout(() => {
                this.$router.push({ path: '/admin/master/account' })
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
  },
}
</script>

<style>
  .row.row-inside {
    max-width: none;
  }
</style>
