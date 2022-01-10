<template>
  <va-card :title="$t('forms.inputs.title')">
    <form>
      <div class="row">
        <div class="flex md4 sm6 xs12">
          <va-input
            v-model="simple"
            placeholder="Text Input"
          />
        </div>
      </div>
    </form>
  </va-card>
</template>
