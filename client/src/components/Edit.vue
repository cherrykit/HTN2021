<template>
  <b-container id="page">
    <h1>{{formatNames(fileArray)}}</h1>
    <b-button variant="primary" @click="sendImages()">Continue</b-button>
    <div> {{msg}} </div>
  </b-container>
</template>

<script>
import axios from "axios";
import { mapState } from 'vuex';
export default {
  name: 'Edit',
  computed: mapState({
    fileArray: state => state.fileArray
  }),
  data() {
    return {
      num: 10,
      msg: 'Test',
    };
  },
  methods: {
    formatNames(files) {
      return files.length === 1 ? files[0].name : `${files.length} files selected`;
    },
    sendImages() {
      this.msg = 'I am here';
      var path = 'http://127.0.0.1:5000/upload_images'
      console.log(path)
      if (this.fileArray && this.fileArray.length === this.num) {
        axios.post(path, {
            inputs: this.fileArray, 
            input_lengths: new Array(this.fileArray.length).fill(1),
            audio_name: "audio1",
            file_type: "mp3"
        }).then((res) => {
            this.msg = 'Success';
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
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
