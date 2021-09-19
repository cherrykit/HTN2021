<template>
  <b-container id="page">
    <b-navbar fixed="top" style="background-color: #061E3E; justify-content: center;">
    <h1 v-show="!music">Choose a song</h1>
    <h1 v-show="music && num == -1">Processing your song...</h1>
    <h1 v-show="this.fileArray.length==0 && !preview && music && num != -1">Please upload {{ num }} images.</h1>
    <h1 v-show="this.fileArray.length && !preview"><div :class="items.length !== num ? 'textColor' : ''"> {{ items.length }} / {{ num }} </div> images uploaded.</h1>
    <h1 v-show="preview && !video">Loading your preview...</h1>
    <h1 v-show="preview && video">Preview your result</h1>
    </b-navbar>
    <b-form-file style="margin-top: 100px;"
      v-show="!this.music && !preview"
      v-model="music"
      :state="Boolean(music)"
      placeholder="Upload an mp3 file"
      no-drop
      accept="audio/mpeg"
    ></b-form-file>
    <b-form-file style="margin-top: 100px;"
      v-show="this.fileArray.length==0 && !preview && music && num != -1"
      v-model="fileArray"
      :state="Boolean(fileArray)"
      :file-name-formatter="formatNames"
      placeholder="Upload images"
      no-drop
      accept="image/*"
      multiple
    ></b-form-file>
    <Container style="padding-top: 100px;" @drop="onDrop" v-show="this.fileArray.length && !preview">
        <Draggable v-for="item in items" :key="item.id">
            <b-row class="draggable-item dragRow" align-v="center">
                <b-col>
                <b-img :src="images[item.id]" height=50 width=50 rounded></b-img>
                </b-col>
                <!-- b-col><img @click="onEdit(item.id)" class="image" src="../assets/edit.png" alt="edit"></b-col -->
                <b-col><img @click="onDelete(item.id)" class="image" src="../assets/delete.png" alt="delete"></b-col>
            </b-row>
        </Draggable>
    </Container>
    <b-row style="padding-top: 10px;" v-show="this.fileArray.length && !preview">
        <b-col> <b-form-file
            v-model="file"
            :state="Boolean(fileArray)"
            :file-name-formatter="formatName"
            placeholder="Add new image"
            no-drop
            accept="image/*"
        ></b-form-file> </b-col>
    </b-row>
    <h1 v-show="this.fileArray.length && !preview">Choose filters and text:</h1>
    <b-form-checkbox-group
      v-show="this.fileArray.length && !preview"
      v-model="effectsSelected"
      :options="effects"
      class="mb-3"
      value-field="item"
      text-field="name"
      disabled-field="notEnabled"
    ></b-form-checkbox-group>
    <!-- <input v-show="this.fileArray.length && !preview" v-model="message" placeholder="Intro Text"> -->
    <br>
    <br>
    <b-row v-show="music && !preview && num != -1">
    <b-col>
    <b-button @click="reset()">Choose different song</b-button>
    </b-col>
    <b-col>
    <b-button variant="primary" @click="onSubmit()" v-show="this.items.length == num">Continue</b-button>
    </b-col>
    </b-row>

    <video controls v-show="preview && video" :src="video">
    </video>
    <br>
    <b-row v-show="preview && video">
    <b-col>
    <b-button variant="secondary" @click="goBack()">Change images</b-button>
    </b-col><b-col>
    <a class="btn btn-primary" :href="video" download target="_blank">Download!</a>
    </b-col>
    </b-row>
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
      num: -1,
      images: [],
      fileArray: [],
      msg: '',
      items: [],
      file: null,
      input_lengths: [],
      preview: false,
      video: null,
      effects: [
      {
        name: 'Black & White',
        item: 'bw'
      },
      {
        name: 'Brighten',
        item: 'bright'
      },
      {
        name: 'Darken',
        item: 'dark'
      },
      {
        name: 'Invert Colours',
        item: 'invert'
      },
      {
        name: 'Flip Horizontally',
        item: 'horizontal'
      },
      {
        name: 'Flip Vertically',
        item: 'vertical'
      },
      {
        name: 'Painting',
        item: 'painting'
      }
    ],
    effectsSelected: [],
      music: null,
      filename: null,
      message: ""
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
    },
    music(newMusic, oldMusic){
      if (newMusic) {
        base64Encode(newMusic).then(val => {
          var mp3 = val;
          var path = 'http://127.0.0.1:5000/upload_audio';
          axios.post(path, {
            audio_data: mp3,
            file_type: "mp3"
          }).then((res) => {
            this.num = res.data.num_inputs
            this.input_lengths = res.data.input_lengths
            this.filename = res.data.audio_name
            this.file_type = res.data.file_type
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });

        })
      }
    }
  },
  methods: {
    formatNames(files) {
      if (this.items.length == 0) {
        this.items = generateItems(this.fileArray.length, i => ({ id: i }))
        console.log(this.items)
      }
      return files.length === 1 ? files[0].name : `${files.length} files selected`;
    },
    formatName(file) {
        if (file) {
            this.items.push({id: this.fileArray.length})
            this.fileArray.push(file[0])
            base64Encode(file[0]).then(value => {
                this.images.push(value);
                this.file = null;
            })
        }
    },
    onSubmit() {
      this.msg = '';
      var path = 'http://127.0.0.1:5000/upload_images';
      console.log(this.images)
      console.log(this.num)
      if (this.items && this.items.length === this.num) {
        var submit_img = []
        this.items.forEach(val => submit_img.push(this.images[val.id]))
        axios.post(path, {
            inputs: submit_img, 
            input_lengths: this.input_lengths,
            audio_name: this.filename,
            file_type: this.file_type,
            effectsSelected: this.effectsSelected,
            message: this.message
        }).then((res) => {
            this.video = 'data:video/' + res.data.file_type + ';base64,' + res.data.video_encoding.substring(2).slice(0, -1);
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
          });
        this.preview = true;
      } else {
        this.msg = 'You selected an incorrect number of files.';
      }
    },
    onDrop(dropResult) {
      this.items = applyDrag(this.items, dropResult);
    },
    onDelete(id) {
        this.items = this.items.filter(val => val.id != id)
        if (this.items.length == 0) {
            this.fileArray = []
            this.images = []
        }
    },
    goBack() {
      this.video = null;
      this.preview = false;
    },
    reset() {
      this.fileArray = [];
      this.items = [];
      this.music = null;
      this.num = -1;
    }
  }
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
.textColor {
    color: red;
}
</style>
