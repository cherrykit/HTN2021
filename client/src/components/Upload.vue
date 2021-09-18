<template>
  <div class="container">
    <h1>Please upload {{ num }} images.</h1>
    <b-button type="submit" variant="danger">Upload</b-button>
  </div>
</template>

<script>
export default {
  name: 'Upload',
  data() {
    return {
      num: 10,
    };
  },
};
</script>
