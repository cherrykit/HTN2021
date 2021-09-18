<template>
  <div class="container">
    <h1>Title</h1>
    <h3>Subtitle</h3>
    <b-button type="submit" variant="primary">Upload your song!</b-button>
    <b-form-file no-drop accept="mp3/*"></b-form-file>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Hello!',
    };
  },
};
</script>
