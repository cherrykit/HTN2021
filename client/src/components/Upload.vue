<template>
  <div class="container">
    <p>Please upload {{ num }} images.</p>
  </div>
</template>

<script>
export default {
  name: 'Upload',
  data() {
    return {
      num: 10
    };
  },
};
</script>