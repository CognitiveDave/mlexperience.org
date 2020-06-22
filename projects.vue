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
    <div class="row">
      <div class="col-sm-10">
      <alert :message=message v-if="showMessage"></alert>
        <h3>Manage events</h3>
        <hr>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Filing Event</button>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Country</th>
              <th scope="col">Project</th>
              <th scope="col">start</th>
              <th scope="col">end</th>
              <th scope="col">Status</th>
              <th scope="col">Owner</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(proj, ID) in project" :key="ID">
              <td>{{ proj.LCTRYNUM }}/{{ proj.LC }}</td>
              <td>{{ proj.NAME }}</td>
              <td>{{ proj.START}}</td>
              <td>{{ proj.END }}</td>
              <td>{{ proj.STATUS }}</td>
              <td>{{ proj.OWNER }}</td>
              <td>
              <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="onDeleteBook(proj)">
                  Delete
              </button>
                <button type="button" class="btn btn-warning btn-sm"  v-b-modal.book-update-modal   @click="editBook(proj)">
                    Update</button>
                <button type="button" class="btn btn-warning btn-sm"  v-b-modal.task-modal   @click="tasks_init(proj)">
                    Tasks</button>
                <button type='button' class='btn btn-warning btm-sm'  v-b-modal.attmodal @click="onEnvokeAtt(proj,'p')"> Att </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal" id="book-modal" title="Adding a Filing plan" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group" label="Country:" label-for="form-title-input">
          <b-form-input id="form-title-input" type="text" v-model="addBookForm.LCTRYNUM" required placeholder=" ">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group" label="Entity:"  label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.LC"
                          required
                          placeholder=" ">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group" label="Name:"  label-for="form-author-input">
              <b-form-input id="form-author-input"
                            type="text"
                            v-model="addBookForm.NAME"
                            required
                            placeholder=" ">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group" label="START:"  label-for="form-author-input">
                <b-form-input id="form-author-input"
                              type="date"
                              v-model="addBookForm.START"
                              required
                              placeholder=" ">
                </b-form-input>
              </b-form-group>
            <b-form-group id="form-author-group" label="END:"  label-for="form-author-input">
                <b-form-input id="form-author-input"
                              type="date"
                              v-model="addBookForm.END"
                              required
                              placeholder=" ">
                </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group" label="STATUS:"  label-for="form-author-input">
                <b-form-input id="form-author-input"
                              type="text"
                              v-model="addBookForm.STATUS"
                              required
                              placeholder=" ">
                </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group" label="OWNER:"  label-for="form-author-input">
                <b-form-input id="form-author-input"
                              type="text"
                              v-model="addBookForm.OWNER"
                              required
                              placeholder=" ">
                </b-form-input>
            </b-form-group>
              <b-form-group>
                <div>
                  <b-btn v-b-toggle.addFileDesc variant="primary">Description</b-btn>
                  <b-collapse id="addFileDesc" class="mt-2">
                    <b-card>
                      <vue-editor v-model="addBookForm.DESC"></vue-editor>
                    </b-card>
                  </b-collapse>
                </div>
              </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
         id="book-update-modal"
         title="Update project"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="Country:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editForm.LCTRYNUM"
                    required
                    placeholder=" ">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-edit-group"
                  label="Entity:"
                  label-for="form-author-edit-input">
        <b-form-input id="form-author-edit-input"
                      type="text"
                      v-model="editForm.LC"
                      required
                      placeholder=" ">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-author-edit-group"
                    label="NAME:"
                    label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.NAME"
                        required
                        placeholder=" ">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="START:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="date"
                          v-model="editForm.START"
                          required
                          placeholder="">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-edit-group"
                        label="END:"
                        label-for="form-author-edit-input">
              <b-form-input id="form-author-edit-input"
                            type="date"
                            v-model="editForm.END"
                            required
                            placeholder="">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-edit-group"
                          label="STATUS:"
                          label-for="form-author-edit-input">
                <b-form-input id="form-author-edit-input"
                              type="text"
                              v-model="editForm.STATUS"
                              required
                              placeholder="">
                </b-form-input>
              </b-form-group>
              <b-form-group id="form-author-edit-group"
                            label="OWNER:"
                            label-for="form-author-edit-input">
                  <b-form-input id="form-author-edit-input"
                                type="text"
                                v-model="editForm.OWNER"
                                required
                                placeholder="">
                  </b-form-input>
                  </b-form-group>
                <b-form-group>
                  <div>
                    <b-btn v-b-toggle.editFileDesc variant="primary">Description</b-btn>
                    <b-collapse id="editFileDesc" class="mt-2">
                      <b-card>
                        <vue-editor v-model="editForm.DESC"></vue-editor>
                      </b-card>
                    </b-collapse>
                  </div>
                </b-form-group>
    <b-button type="submit" variant="primary">Update</b-button>
    <b-button type="reset" variant="danger">Cancel</b-button>
  </b-form>
</b-modal>

<b-modal ref="tasksModal" id="task-modal" title="Tasks" hide-footer>
  <div class="row">
    <div class="col-sm-10">
    <alert :message=task_message v-if="showMessage"></alert>
      <h1>Tasks</h1>
      <button type="button" class="btn btn-success btn-sm" v-b-modal.task-modaladd>Add Task</button>
      <br>
      <table class="table table-hover">
        <thead>
          <tr>
            <th scope="col">start</th>
            <th scope="col">end</th>
            <th scope="col">Stat</th>
            <th scope="col">Owner</th>
            </tr>
        </thead>
        <tbody>
          <tr v-for="(task, ID) in tasks" :key="ID">
            <td>{{ task.START}}</td>
            <td>{{ task.END }}</td>
            <td>{{ task.STATUS }}</td>
            <td>{{ task.OWNER }}</td>
            <td>
            <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteTask(task)">
                Del
            </button>
              <button type="button" class="btn btn-warning btn-sm"  v-b-modal.task-update-modal   @click="onEditTask(task)">
                  Edit</button>
              <button type='button' class='btn btn-warning btm-sm'  v-b-modal.attmodal @click="onEnvokeAtt(task,'t')"> Att </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
    </b-modal>
    <b-modal ref='attmodal'
        id='attmodal'
        title='Attachments'
        hide-footer
        @hidden="onHidden">
          <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <alert :message=att_message v-if="att_showMessage"></alert>
      <p> Event:{{ cur_proj }},  Task:{{ cur_task }}</p>
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
  </div>
    </b-modal>
    <b-modal ref="editTaskModal"
         id="task-update-modal"
         title="Update task"
         hide-footer>
  <b-form @submit="onSubmitTaskUpdate" @reset="onResetTaskUpdate"  class="w-100">
  <b-form-group id="form-title-edit-group"
                label="Name:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editTaskForm.NAME"
                    required
                    placeholder=" ">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-edit-group"
                  label="Start:"
                  label-for="form-author-edit-input">
        <b-form-input id="form-author-edit-input"
                      type="date"
                      v-model="editTaskForm.START"
                      required
                      placeholder=" ">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-author-edit-group"
                    label="End:"
                    label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="date"
                        v-model="editTaskForm.END"
                        required
                        placeholder=" ">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Status:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editTaskForm.STATUS"
                          required
                          placeholder="">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-edit-group"
                        label="Owner:"
                        label-for="form-author-edit-input">
              <b-form-input id="form-author-edit-input"
                            type="text"
                            v-model="editTaskForm.OWNER"
                            required
                            placeholder="">
              </b-form-input>
              </b-form-group>
            <b-form-group>
              <div>
                <b-btn v-b-toggle.editTaxDesc variant="primary">Description</b-btn>
                <b-collapse id="editTaxDesc" class="mt-2">
                  <b-card>
                    <vue-editor v-model="editTaskForm.TDESC"></vue-editor>
                  </b-card>
                </b-collapse>
              </div>
            </b-form-group>
    <b-button type="submit" variant="primary">Update</b-button>
    <b-button type="reset" variant="danger">Cancel</b-button>
  </b-form>
</b-modal>
  <b-modal ref="addTaskModal" id="task-modaladd" title="Add a task" hide-footer>
    <b-form @submit="onSubmitTask" @reset="onResetTask"  class="w-100">
    <b-form-group id="form-title-group" label="Name:" label-for="form-title-input">
    <b-form-input id="form-title-input" type="text" v-model="addTaskForm.NAME" required placeholder=" ">
   </b-form-input>
   </b-form-group>
   <b-form-group id="form-author-group" label="Start:"  label-for="form-author-input">
              <b-form-input id="form-author-input"
                            type="date"
                            v-model="addTaskForm.START"
                            required
                            placeholder=" ">
              </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-group" label="End:"  label-for="form-author-input">
    <b-form-input id="form-author-input"
                  type="date"
                  v-model="addTaskForm.END"
                  required
                  placeholder=" ">
    </b-form-input>
  </b-form-group>
  <b-form-group id="form-author-group" label="Status:"  label-for="form-author-input">
      <b-form-input id="form-author-input"
                    type="text"
                    v-model="addTaskForm.STATUS"
                    required
                    placeholder=" ">
      </b-form-input>
    </b-form-group>
  <b-form-group id="form-author-group" label="Owner:"  label-for="form-author-input">
      <b-form-input id="form-author-input"
                    type="text"
                    v-model="addTaskForm.OWNER"
                    required
                    placeholder=" ">
      </b-form-input>
  </b-form-group>
  <b-form-group>
    <div>
      <b-btn v-b-toggle.addTaxDesc variant="primary">Description</b-btn>
      <b-collapse id="addTaxDesc" class="mt-2">
        <b-card>
          <vue-editor v-model="addTaskForm.TDESC"></vue-editor>
        </b-card>
      </b-collapse>
    </div>
  </b-form-group>
    <b-button type="submit" variant="primary">Submit</b-button>
    <b-button type="reset" variant="danger">Reset</b-button>
  </b-form>
   </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert'
import { VueEditor } from 'vue2-editor'
import FileMgr from './SelectFiles'

export default {
  data () {
    return {
      tester: '',
      files: [],
      attac: [],
      blank: '',
      file2: null,
      cur_proj: '',
      cur_task: '',
      project: [],
      tasks: [],
      addBookForm: {
        ID: ' ',
        LCTRYNUM: ' ',
        LC: ' ',
        NAME: ' ',
        START: ' ',
        END: ' ',
        STATUS: ' ',
        OWNER: ' ',
        DESC: ' ',
        FILE2: ''
      },
      editForm: {
        ID: ' ',
        LCTRYNUM: ' ',
        LC: ' ',
        NAME: ' ',
        START: ' ',
        END: ' ',
        STATUS: ' ',
        OWNER: ' ',
        DESC: ' ',
        FILE2: ''
      },
      addTaskForm: {
        NAME: ' ',
        START: ' ',
        END: ' ',
        STATUS: ' ',
        OWNER: ' ',
        ID: ' ',
        PR_ID: ' ',
        TDESC: '',
        FILET: ''
      },
      editTaskForm: {
        NAME: ' ',
        START: ' ',
        END: ' ',
        STATUS: ' ',
        OWNER: ' ',
        PR_ID: ' ',
        ID: ' ',
        TDESC: '',
        FILET: ''
      },
      message: '',
      task_message: '',
      att_message: ' ',
      showMessage: false,
      att_showMessage: false,
      modalShow: false,
      content: 'Add text here',
      att_ev: ''
    }
  },
  components: {
    alert: Alert,
    fmgr: FileMgr,
    VueEditor
  },
  methods: {
    getBooks () {
      const path = '/api/projects'
      axios.get(path)
        .then((res) => {
          this.project = res.data.project
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    onHidden (evt) {
      this.$refs.attmodal.hide()
      if (this.att_ev === 't') {
        this.$refs.tasksModal.show()
      }
      this.CloseFiles()
    },
    addBook (payload) {
      const path = '/api/projects'
      axios.post(path, payload)
        .then(() => {
          this.getBooks()
          this.message = 'Project added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    updateBook (payload, ID) {
      const path = `/api/projects/${ID}`
      axios.put(path, payload)
        .then(() => {
          this.getBooks()
          this.message = 'Project updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    removeBook (ID) {
      const path = `/api/projects/${ID}`
      axios.delete(path)
        .then(() => {
          this.getBooks()
          this.message = 'Project removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    initForm () {
      this.addBookForm.LCTRYNUM = ''
      this.addBookForm.LC = ''
      this.addBookForm.NAME = ''
      this.addBookForm.START = ''
      this.addBookForm.END = ''
      this.addBookForm.STATUS = ''
      this.addBookForm.OWNER = ''
      this.addBookForm.DESC = ''
      this.addBookForm.FILE2 = ''
      this.editForm.LCTRYNUM = ''
      this.editForm.LC = ''
      this.editForm.NAME = ''
      this.editForm.START = ''
      this.editForm.END = ''
      this.editForm.STATUS = ''
      this.editForm.OWNER = ''
      this.editForm.DESC = ''
      this.editForm.FILE2 = ''
      this.editTaskForm.NAME = ''
      this.editTaskForm.START = ''
      this.editTaskForm.END = ''
      this.editTaskForm.STATUS = ''
      this.editTaskForm.OWNER = ''
      this.editTaskForm.PR_ID = ''
      this.editTaskForm.TDESC = ''
      this.addTaskForm.TDESC = ''
      this.addTaskForm.NAME = ''
      this.addTaskForm.START = ''
      this.addTaskForm.END = ''
      this.addTaskForm.STATUS = ''
      this.addTaskForm.OWNER = ''
      this.addTaskForm.PR_ID = ''
      this.addTaskForm.FILET = ''
      this.editTaskForm.FILET = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addBookModal.hide()
      const payload = {
        LCTRYNUM: this.addBookForm.LCTRYNUM,
        LC: this.addBookForm.LC,
        NAME: this.addBookForm.NAME,
        START: this.addBookForm.START,
        END: this.addBookForm.END,
        STATUS: this.addBookForm.STATUS,
        OWNER: this.addBookForm.OWNER,
        DESC: this.addBookForm.DESC,
        FILE2: this.addBookForm.FILE2
      }
      this.addBook(payload)
      this.initForm()
    },
    onSubmitUpdate (evt) {
      evt.preventDefault()
      this.$refs.editBookModal.hide()
      const payload = {
        LCTRYNUM: this.editForm.LCTRYNUM,
        LC: this.editForm.LC,
        NAME: this.editForm.NAME,
        START: this.editForm.START,
        END: this.editForm.END,
        STATUS: this.editForm.STATUS,
        OWNER: this.editForm.OWNER,
        DESC: this.editForm.DESC,
        FILE2: this.editForm.FILE2
      }
      this.updateBook(payload, this.editForm.ID)
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.addBookModal.hide()
      this.initForm()
    },
    onResetUpdate (evt) {
      evt.preventDefault()
      this.$refs.editBookModal.hide()
      this.initForm()
      this.getBooks() // why?
    },
    onDeleteBook (book) {
      this.removeBook(book.ID)
    },
    editBook (book) {
      this.editForm = book
    },
    onEditTask (task) {
      this.editTaskForm = task
    },
    onDeleteTask (task) {
      this.removeTask(task.ID, task.PR_ID)
    },
    tasks_init (proj) {
      this.getTasks(proj.ID)
      this.cur_proj = proj.ID
    },
    onEnvokeAtt (elm, type) {
      if (type === 'p') {
        this.cur_proj = elm.ID
        this.cur_task = '-'
      }
      if (type === 't') {
        this.cur_proj = elm.PR_ID
        this.cur_task = elm.ID
      }
      this.CloseFiles()
      this.Files()
      this.att_ev = type
    },
    addTask (payload, PR_ID) {
      const path = `/api/tasks/${PR_ID}`
      axios.post(path, payload)
        .then(() => {
          this.getTasks(PR_ID)
          this.task_message = 'Task added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getTasks(PR_ID)
        })
    },
    updateTask (payload, ID, PR_ID) {
      const path = `/api/tasks/${ID}/${PR_ID}`
      axios.put(path, payload)
        .then(() => {
          this.getTasks(PR_ID)
          this.task_message = 'Task updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getTasks(PR_ID)
        })
    },
    removeTask (ID, PR_ID) {
      const path = `/api/tasks/${ID}/${PR_ID}`
      axios.delete(path)
        .then(() => {
          this.getTasks(PR_ID)
          this.task_message = 'Task removed!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getTasks(PR_ID)
        })
    },
    getTasks (PR_ID) {
      const path = `/api/tasks/${PR_ID}`
      axios.get(path)
        .then((res) => {
          this.tasks = res.data.tasks
          this.$refs.tasksModal.show()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    onSubmitTaskUpdate (evt) {
      evt.preventDefault()
      this.$refs.editTaskModal.hide()
      const payload = {
        NAME: this.editTaskForm.NAME,
        START: this.editTaskForm.START,
        END: this.editTaskForm.END,
        STATUS: this.editTaskForm.STATUS,
        OWNER: this.editTaskForm.OWNER,
        TDESC: this.editTaskForm.TDESC,
        FILET: this.editTaskForm.FILET
      }
      this.updateTask(payload, this.editTaskForm.ID, this.editTaskForm.PR_ID)
    },
    onSubmitTask (evt) {
      evt.preventDefault()
      this.$refs.addTaskModal.hide()
      const payload = {
        NAME: this.addTaskForm.NAME,
        START: this.addTaskForm.START,
        END: this.addTaskForm.END,
        STATUS: this.addTaskForm.STATUS,
        OWNER: this.addTaskForm.OWNER,
        TDESC: this.addTaskForm.TDESC,
        FILET: this.addTaskForm.FILET
      }
      this.addTask(payload, this.cur_proj)
      this.initForm()
    },
    onResetTask (evt) {
      evt.preventDefault()
      this.$refs.addTaskModal.hide()
      this.initForm()
      this.$refs.tasksModal.show()
    },
    onResetTaskUpdate (evt) {
      evt.preventDefault()
      this.$refs.editTaskModal.hide()
      this.initForm()
      this.$refs.tasksModal.show()
    },
    addFiles () {
      this.$refs.files.click()
    },
    CloseFiles () {
      this.att_message = ''
      this.att_showMessage = false
      this.files = []
      this.attac = []
    },
    submitFiles () {
      let formData = new FormData()
      for (var i = 0; i < this.files.length; i++) {
        let file = this.files[i]
        formData.append('files[' + i + ']', file)
      }
      const path = `/api/upload/${this.cur_task}/${this.cur_proj}`
      this.message = 'sending..'
      axios.post(path,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/mixed'
          }
        }
      ).then((res) => {
        this.att_message = res.data
        this.files = []
        this.att_showMessage = true
        this.Files()
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error)
      })
    },
    Files () {
      const path = `/api/attachments/${this.cur_task}/${this.cur_proj}`
      axios.get(path)
        .then((res) => {
          this.attac = res.data.project
        }).catch((error) => {
        // eslint-disable-next-line
          console.error(error)
        })
    },
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
  },
  created () {
    this.getBooks()
  }
}
</script>
