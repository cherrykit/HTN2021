<template>
  <b-container id="page">
    <h1>Please upload {{ num }} images.</h1>
    <br>
    <b-button type="submit" variant="primary">Upload images</b-button>
    <b-form-file no-drop accept="image/*"></b-form-file>
  </b-container>
</template>

<script>
export default {
  name: 'Upload',
  data() {
    return {
      num: 10,
      file: null,
    };
  },
};
</script>

<style>
#page {
    padding: 20px;
    text-align: center;
}
</style>
