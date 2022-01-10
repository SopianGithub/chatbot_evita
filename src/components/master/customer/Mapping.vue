<template>
  <div class="form-elements">
    <div class="row">
      <div class="flex xs12">
        <va-card :title="$t('Detail CC')">
          <div class="row">
            <div class="flex xs12">
              <p class="display-3">{{ nama_cc }}</p>
            </div>
          </div>
          <div class="row">
            <div class="flex xs12">
              <va-accordion>
                <va-collapse>
                  <span slot="header"> Segmen </span>
                  <div slot="body">
                    <p class="display-5">{{ segmen }}</p>
                    <div>
                      {{ segmen_desc }}
                    </div>
                  </div>
                </va-collapse>
                <va-collapse>
                  <span slot="header"> Alias </span>
                  <div slot="body">
                    <div>
                      <ul class="va-unordered">
                        <li v-for="(data, index) in aliasCC" :key="index">{{ data }}</li>
                      </ul>
                    </div>
                  </div>
                </va-collapse>
              </va-accordion>
            </div>
          </div>
          <div class="row">
            <div class="flex xs12">
              <p class="display-6">List Account Manager</p>
              <div class="mb-4">
                <table class="va-table">
                  <thead>
                    <tr>
                      <th>NIK</th>
                      <th>Nama</th>
                      <th>No. HP</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(data, index) in mappingAM" :key="index">
                      <td v-for="(i, index) in data" :key="index">{{i}}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </va-card>
      </div>
    </div>
    <form @submit.prevent="onsubmit" >
      <div class="row">
        <div class="flex md12 sm12 xs12">
          <multiselect v-model="selectedAM" id="ajax" label="name" track-by="nik" placeholder="Type to search" open-direction="bottom" :options="listAM" :multiple="true" :searchable="true" :loading="isLoadingSearchAM" :internal-search="false" :clear-on-select="false" :close-on-select="false" :options-limit="300" :limit="3" :limit-text="limitText" :max-height="600" :show-no-results="false" :hide-selected="true" @search-change="asyncFind">
            <template slot="tag" slot-scope="{ option, remove }"><span class="custom__tag"><span>{{ option.name }}</span><span class="custom__remove" @click="remove(option)">❌</span></span></template>
            <template slot="clear" slot-scope="props">
              <div class="multiselect__clear" v-if="selectedAM.length" @mousedown.prevent.stop="clearAll(props.search)"></div>
            </template><span slot="noResult">Oops! No elements found. Consider changing the search query.</span>
          </multiselect>
        </div>
      </div>
      <div class="flex">
        <va-button
          type="submit"
          class="my-0"
        >
          Mapping AM</va-button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'mapping-modal',
  data () {
    return {
    	nipnas: null,
      	selectedAM: [],
      	isLoadingSearchAM: false,
      	listAM: [],
      	savingSuccessful: true,
	    messageNotif: '',
	    isSuccess: false,
	    aliasCC: [],
	    mappingAM: [],
	    nama_cc: '',
	    segmen: '',
	    segmen_desc: '',
    }
  },
  created () {
  	this.init()
  },
  methods: {
  	async init () {
      this.nipnas = this.nipnas = this.$route.params.id_cc
      await axios.get(`http://localhost:5000/cc/mapping/${this.nipnas}`)
        	.then((res) => {
        		if (res.status === 200) {
        			this.nama_cc = res.data.values[0].name
        			this.aliasCC = res.data.values[0].alias
        			this.mappingAM = res.data.values[0].mapping
        			this.segmen = res.data.values[0].segmen.name
        			this.segmen_desc = res.data.values[0].segmen.descr
        		}
        	})
    },
    async asyncFind (query) {
      this.isLoadingSearchAM = true
      await axios.get(`http://localhost:5000/ams/search/${query}`)
        .then(response => {
          if (response.status === 200) {
            this.listAM = response.data.values
            this.isLoadingSearchAM = false
          }
        })
    },
    limitText (count) {
      return `and ${count} other AM`
    },
    clearAll () {
      this.selectedAM = []
    },
    async onsubmit () {
    	console.log(this.selectedAM)
    	await axios.put(`http://localhost:5000/cc/mapping/${this.nipnas}`, this.selectedAM)
        .then((res) => {
          if (res.status === 200) {
            this.messageNotif = 'Mapping Data CC Berhasil'
            this.isSuccess = true
            this.savingSuccessful = true
            setTimeout(() => {
              this.$router.push({ path: '/admin/master/customer' })
            }, 1000)
          } else {
            this.messageNotif = 'Terjadi Kesalahan Pada Proses Penyimpanan Data'
          }
        })
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
