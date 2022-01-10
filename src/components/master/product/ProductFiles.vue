<template>
  <div>
    <div class="row">
      <div class="flex xs12">
        <va-select
          :label="$t('Pilih Tipe File Produk')"
          v-model="selectTypeFileProps"
          textBy="name"
          textValue="name"
          :options="kindOfFileOption"
          @input="changeFileType"
        >
          <template slot="prepend">
            <va-icon name="fa fa-file-archive-o icon-left input-icon"/>
          </template>
        </va-select>
      </div>
    </div>
    <div class="row">
      <div class="flex xs10">
        <va-input
          v-model="urlFileProps"
          placeholder="Input Link File"
          @input="changeUrl"
        >
          <template slot="prepend">
            <va-icon name="fa fa-link icon-left input-icon"/>
          </template>
        </va-input>
      </div>
      <div class="flex xs2">
        <va-button
          small outline
          color="danger"
          icon="fa fa-minus-circle"
          type="button"
          class="my-0"
          @click="removeElmLink(indexArr)"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'product-files',
  props: {
	     	kindOfFileOption: {
	          type: Array,
	     	},
	     	indexArr: {
	     	  type: Number,
	     	},
	     	selectedTypeFile: {
	     		type: String,
	     	},
  },
  data () {
    return {
      selectTypeFileProps: '',
      urlFileProps: 'http://',
    }
  },
  created () {
		    console.log('Test' + kindOfFileOption)
  },
  methods: {
    changeFileType () {
		     	this.$emit('update-type-file', this.indexArr, this.selectTypeFileProps)
		    },
    removeElmLink (keyin) {
      this.$emit('remove-elm-file', keyin)
		    },
		    changeUrl () {
		    	this.$emit('update-url-file', this.indexArr, this.urlFileProps)
		    },
  },
}
</script>
