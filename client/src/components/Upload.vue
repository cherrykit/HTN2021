<template>
  <b-container id="page">
    <h1>Please upload {{ num }} images.</h1>
    <br>
    <b-form-file
      v-show="this.fileArray.length==0"
      v-model="fileArray"
      :state="Boolean(fileArray)"
      :file-name-formatter="formatNames"
      placeholder="Upload images"
      no-drop
      accept="image/*"
      multiple
    ></b-form-file>
    <Container @drop="onDrop" v-show="this.fileArray.length">
        <Draggable v-for="item in items" :key="item.id">
            <b-row class="draggable-item dragRow">
                <b-col>
                <b-img :src="images[item.id]" height=50 width=50 rounded></b-img>
                </b-col>
                <b-col><img @click="onEdit" class="image" src="../assets/edit.png" alt="edit"></b-col>
                <b-col><img @click="onDelete" class="image" src="../assets/delete.png" alt="delete"></b-col>
            </b-row>
        </Draggable>
    </Container>
    <b-row class="dragRow" v-show="this.fileArray.length">
        <b-col> Add new image </b-col>
    </b-row>
    <br>
    <br>
    <b-button variant="primary" @click="onSubmit()">Continue</b-button>
    <div style="color: red;">{{msg}}</div>
  </b-container>
</template>

<script>
import axios from "axios";
import { Container, Draggable } from "vue-dndrop";
import { applyDrag, generateItems } from "../main.js";
const base64Encode = data =>
  new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(data);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

export default {
  name: 'Upload',
  components: {Container, Draggable},
  data() {
    return {
      num: 10,
      images: [],
      fileArray: [],
      msg: 'Test',
      items: [],
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
      if (this.items.length == 0) {
        this.items = generateItems(this.fileArray.length, i => ({ id: i, data: this.fileArray[i].name }))
        console.log(this.items)
      }
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
            console.log("Success")
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
      } else {
        this.msg = 'You selected an incorrect number of files.';
      }
    },
    onDrop(dropResult) {
      this.items = applyDrag(this.items, dropResult);
    },
    onEdit() {
        console.log("edit")
    },
    onDelete() {
        console.log("delete")
    }
  },
};
</script>

<style>
#page {
    padding: 20px;
    text-align: center;
}
.dragRow {
    padding-top: 10px;
    padding-bottom: 10px;
    border: solid;
}
</style>
