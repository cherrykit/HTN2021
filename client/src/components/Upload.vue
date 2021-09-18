<template>
  <b-container id="page">
    <h1>Please upload {{ num }} images.</h1>
    <br>
    <b-form-file
      v-model="fileArray"
      :state="Boolean(fileArray)"
      :file-name-formatter="formatNames"
      placeholder="Upload images"
      no-drop
      accept="image/*"
      multiple
    ></b-form-file>
    <br>
    <br>
    <b-button variant="primary" @click="onSubmit()">Continue</b-button>
    <div style="color: red;">{{msg}}</div>
  </b-container>
</template>

<script>
export default {
  name: 'Upload',
  data() {
    return {
      num: 10,
      fileArray: null,
      msg: 'Test',
    };
  },
  methods: {
    formatNames(files) {
      return files.length === 1 ? files[0].name : `${files.length} files selected`;
    },
    onSubmit() {
      this.msg = '';
      if (this.fileArray && this.fileArray.length === this.num) {
        this.msg = 'Success';
      } else {
        this.msg = 'You selected an incorrect number of files.';
      }
    },
  },
};
</script>

<style>
#page {
    padding: 20px;
    text-align: center;
}
</style>
