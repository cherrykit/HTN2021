<template>
  <b-container id="page">
    <style>
dropdown: { 
  position: relative; 
  cursor: pointer;
}

multiselect: {
  position: relative;
  
  ul {
    border: 1px solid #ddd;
    border-top: 0;
    border-radius: 0 0 3px 3px;
    left: 0px;
    padding: 8px 8px;
    position: absolute;
    top: -1rem;
    width: 100%;
    list-style: none;
    max-height: 150px;
    overflow: auto;
  }
}

overselect: {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
    </style>
    <b-navbar fixed="top" style="background-color: #434343; justify-content: center;">
    <h1 v-show="this.fileArray.length==0 && !preview">Please upload {{ num }} images.</h1>
    <h1 v-show="this.fileArray.length && !preview"><div :class="items.length !== num ? 'textColor' : ''"> {{ items.length }} / {{ num }} </div> images uploaded.</h1>
    <h1 v-show="preview && !video">Loading your preview...</h1>
    <h1 v-show="preview && video">Preview your result</h1>
    </b-navbar>
    <b-form-file style="margin-top: 100px;"
      v-show="this.fileArray.length==0 && !preview"
      v-model="fileArray"
      :state="Boolean(fileArray)"
      :file-name-formatter="formatNames"
      placeholder="Upload images"
      no-drop
      accept="image/*"
      multiple
    ></b-form-file>
    <Container @drop="onDrop" v-show="this.fileArray.length && !preview" style="padding-top: 100px;">
        <Draggable v-for="item in items" :key="item.id">
            <b-row class="draggable-item dragRow" align-v="center">
                <b-col>
                <b-img :src="images[item.id]" height=50 width=50 rounded></b-img>
                </b-col>
                <!-- b-col><img @click="onEdit(item.id)" class="image" src="../assets/edit.png" alt="edit"></b-col -->
                <b-col><img @click="onDelete(item.id)" class="image" src="../assets/delete.png" alt="delete"></b-col>
                <div>
                <!-- <b-dropdown id="dropdown-1" text="Select Effects" class="m-md-2" v-for="(option, index) in effects" :key="index">
                  <b-dropdown-item>First Action</b-dropdown-item>
                  <b-dropdown-item>Second Action</b-dropdown-item>
                  <b-dropdown-item>Third Action</b-dropdown-item>
                  
                </b-dropdown> -->
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
    <br>
    <b-button variant="primary" @click="onSubmit()" v-show="this.items.length == num && !preview">Continue</b-button>
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
      num: 10,
      images: [],
      fileArray: [],
      msg: '',
      items: [],
      file: null,
      input_lengths: new Array(10).fill(1),
      preview: false,
      video: null,
      effects: [
      {
        text: 'Black & White',
        value: 'bw'
      },
      {
        text: 'Brighten',
        value: 'bright'
      },
      {
        text: 'Darken',
        value: 'dark'
      },
      {
        text: 'Invert Colours',
        value: 'invert'
      },
      {
        text: 'Flip Horizontally',
        value: 'horizontal'
      },
      {
        text: 'Flip Vertically',
        value: 'vertical'
      },
      {
        text: 'Painting',
        value: 'horizontal'
      }
    ]
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
            audio_name: "audio1",
            file_type: "mp3"
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
