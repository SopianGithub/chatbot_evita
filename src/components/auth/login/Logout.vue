<template>
</template>

<script>
export default {
  name: 'logout',
  data () {
    return {}
  },
  created () {
    this.logout()
  },
  methods: {
  	logout () {
      	this.$store.dispatch('logout').then(() => {
  			this.$router.push({ name: 'login' })
  		})
    },
  },
}
</script>
