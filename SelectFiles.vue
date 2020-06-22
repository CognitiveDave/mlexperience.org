<style>
  input[type="file"]{
    position: absolute;
    top: -500px;
  }

  div.file-listing{
    width: 200px;
  }

  span.remove-file{
    color: red;
    cursor: pointer;
    float: right;
  }
</style>

<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <alert :message=message v-if="showMessage"></alert>
      <p> Event:{{ PR_ID }},  Task:{{ ID }}</p>
      <div v-for="(file, key) in files" :key="key" class="file-listing">{{ file.name }} <span class="remove-file" v-on:click="removeFile( key )">Remove</span></div>
       <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Upload Date</th>
            <th scope="col">Size</th>
            </tr>
        </thead>
        <tbody>
          <tr v-for="(attac, key) in attac" :key="key">
            <td>{{ attac.key}}</td>
            <td>{{ attac.name }}</td>
            <td>{{ attac.date}}</td>
            <td>{{ attac.size}}</td>
            <td>
            <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="deleteFile(key)">
                Del
            </button>
            <button type="button" class="btn btn-warning btn-sm" @click="downloadFile(key)">
                  Download</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <br>
    <div class="large-12 medium-12 small-12 cell">
     <label>Files
        <input type="file" id="files" ref="files" multiple v-on:change="handleFilesUpload()"/>
     </label>
    </div>
    <div class="large-12 medium-12 small-12 cell">
      <button v-on:click="addFiles()">Add Files</button>
    </div>
    <br>
    <div class="large-12 medium-12 small-12 cell">
      <button v-on:click="submitFiles()">Submit</button>
    </div>
    <div class="large-12 medium-12 small-12 cell">
      <button v-on:click="Files()">Attachments</button>
    </div>
    <div class="large-12 medium-12 small-12 cell">
      <button v-on:click="CloseFiles()">Close</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert'

export default {
  /*
    Defines the data used by the component
  */
  props: ['PR_ID', 'ID', 'MES', 'BAR'],
  data () {
    return {
      files: [],
      message: this.MES,
      showMessage: this.BAR,
      attac: []
    }
  },
  components: {
    alert: Alert
  },
  /*
    Defines the method used by the component
  */
  methods: {
    /*
      Adds a file
    */
    mount: function () {
    // `this` points to the vm instance
      this.Closefiles()
      this.Files()
    },
    addFiles () {
      this.$refs.files.click()
    },
    CloseFiles () {
      this.message = ''
      this.showMessage = false
      this.files = []
      this.attac = []
    },
    /*
      Submits files to the server
    */
    submitFiles () {
      /*
        Initialize the form data
      */
      let formData = new FormData()
      /*
        Iteate over any file sent over appending the files
        to the form data.
      */
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i]
        formData.append('files[' + i + ']', file)
      }
      /*
        Make the request to the POST /select-files URL
      */
      const path = `/api/upload/${this.ID}/${this.PR_ID}`
      this.message = 'sending..'
      axios.post(path,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/mixed'
          }
        }
      ).then((res) => {
        this.message = res.data
        this.files = []
        this.showMessage = true
        this.Files()
      })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    Files () {
      const path = `/api/attachments/${this.ID}/${this.PR_ID}`
      axios.get(path)
        .then((res) => {
          this.attac = res.data.project
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    /*
      Handles the uploading of files
    */
    handleFilesUpload () {
      let uploadedFiles = this.$refs.files.files
      /*
        Adds the uploaded file to the files array
      */
      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push(uploadedFiles[i])
      }
    },
    /*
      Removes a select file the user has uploaded
    */
    removeFile (key) {
      this.files.splice(key, 1)
    },
    deleteFile (key) {
      const path = `/api/attachment/${this.attac[key].name}`
      axios.delete(path)
        .then((res) => {
          this.Files()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    downloadFile (key) {
      const path = `/api/attachment/${this.attac[key].name}`
      axios.get(path, {method: 'GET',
        responseType: 'blob'})
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', this.attac[key.name])
          document.body.appendChild(link)
          link.click()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    }
  }
}
</script>
