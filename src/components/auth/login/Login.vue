<template>
  <form @submit.prevent="onsubmit">
    <va-input
      v-model="nik"
      type="nik"
      :label="$t('nik')"
      :error="!!nikErrors.length"
      :error-messages="nikErrors"
    />

    <va-input
      v-model="password"
      type="password"
      :label="$t('auth.password')"
      :error="!!passwordErrors.length"
      :error-messages="passwordErrors"
    />

    <!-- <div class="auth-layout__options d-flex align--center justify--space-between">
      <va-checkbox v-model="keepLoggedIn" class="mb-0" :label="$t('auth.keep_logged_in')"/>
      <router-link class="ml-1 link" :to="{name: 'recover-password'}">{{$t('auth.recover_password')}}</router-link>
    </div> -->

    <div class="d-flex justify--center mt-3">
      <va-button type="submit" class="my-0">{{ $t('auth.login') }}</va-button>
    </div>
  </form>
</template>

<script>

export default {
  name: 'login',
  data () {
    return {
      nik: '',
      password: '',
      keepLoggedIn: false,
      nikErrors: [],
      passwordErrors: [],
    }
  },
  created () {
    if (localStorage.getItem('nik')) {
      this.$store.dispatch('get_user').then(res => {
        this.$router.push({ name: '/admin/dashboard' })
      })
    }
  },
  computed: {
    formReady () {
      return !this.nikErrors.length && !this.passwordErrors.length
    },
  },
  methods: {
    onsubmit () {
      this.nikErrors = this.nik ? [] : ['nik is required']
      this.passwordErrors = this.password ? [] : ['Password is required']
      if (!this.formReady) {
        return
      }
      this.$store.dispatch('login', {
        nik: this.nik,
        password: this.password,
      }).then(response => {
        this.$router.push({ name: 'dashboard' })
      }).catch(err => {
        this.passwordErrors = ['Password Kurang Tepat']
        this.nikErrors = ['NIK Kurang Tepat']
      })
      // axios.post('http://localhost:5000/login', {
      //   nik: this.nik,
      //   password: this.password
      // }).then((res) => {
      //   if(res.status === 200){
      //     if(res.data.values.status == 'Success'){

      //       this.$router.push({ name: 'dashboard' })
      //     }else{
      //       this.passwordErrors = "NIK atau Password Kurang Tepat"
      //     }
      //   }else{
      //     this.passwordErrors = "Mohon Maaf Koneksi Tidak Stabil"
      //   }
      // })
    },
  },
}
</script>

<style lang="scss">
</style>
