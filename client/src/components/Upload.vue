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
    <!-- <Container @drop="onDrop">
        <Draggable v-for="item in images" :key="item.id">
            <div class="draggable-item">
              {{item.data}}
            </div>
        </Draggable>
    </Container> -->
    <br>
    <br>
    <b-button variant="primary" @click="onSubmit()">Continue</b-button>
    <div style="color: red;">{{msg}}</div>
  </b-container>
</template>

<script>
import axios from "axios";
const base64Encode = data =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(data);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

export default {
  name: 'Upload',
  data() {
    return {
      num: 10,
      images: [],
      fileArray: [],
      msg: 'Test',
    };
  },
  watch: {
    fileArray(newFiles, oldFiles) {
      if (newFiles !== oldFiles) {
        this.images = []
        if (newFiles) {
          newFiles.forEach(val =>
            base64Encode(val)
            .then(value => {
              this.images.push(value);
            })
            .catch(() => {
            })
          )
        }
      }
    }
  },
  methods: {
    formatNames(files) {
      return files.length === 1 ? files[0].name : `${files.length} files selected`;
    },
    onSubmit() {
      this.msg = 'I am here';
      var path = 'http://127.0.0.1:5000/upload_images';
      console.log(this.images)
      console.log(this.num)
      if (this.images && this.images.length === this.num) {
        axios.post(path, {
            inputs: this.images, 
            input_lengths: new Array(this.images.length).fill(1),
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
