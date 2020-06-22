<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
      <alert :message=message v-if="showMessage"></alert>
        <h4>Available in the SandBox</h4>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add A/c</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Country</th>
              <th scope="col">Legal Entity</th>
              <th scope="col">Function</th>
              <th scope="col">G/L Account</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(book, ID) in books" :key="ID">
              <td>{{ book.LCTRYNUM }}</td>
              <td>{{ book.LC }}</td>
              <td>{{ book.MAJOR }}</td>
              <td>{{ book.MINOR }}</td>
              <td>
              <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="onDeleteBook(book)">
                  Delete
              </button>
                <button type="button" class="btn btn-warning btn-sm"  v-b-modal.book-update-modal   @click="editBook(book)">
                    Update</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addBookModal" id="book-modal" title="Add a new a/c" hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-title-group" label="Country:" label-for="form-title-input">
          <b-form-input id="form-title-input" type="text" v-model="addBookForm.LCTRYNUM" required placeholder="nnn">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group" label="Entity:"  label-for="form-author-input">
            <b-form-input id="form-author-input"
                          type="text"
                          v-model="addBookForm.LC"
                          required
                          placeholder="nn">
            </b-form-input>
          </b-form-group>
          <b-form-group id="form-author-group" label="Function:"  label-for="form-author-input">
              <b-form-input id="form-author-input"
                            type="text"
                            v-model="addBookForm.MAJOR"
                            required
                            placeholder="nnn">
              </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group" label="G/L A/c:"  label-for="form-author-input">
                <b-form-input id="form-author-input"
                              type="text"
                              v-model="addBookForm.MINOR"
                              required
                              placeholder="nnnn">
                </b-form-input>
              </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editBookModal"
         id="book-update-modal"
         title="Update a/c"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="Country:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editForm.LCTRYNUM"
                    required
                    placeholder="Enter LCTRYNUM">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-edit-group"
                  label="Entity:"
                  label-for="form-author-edit-input">
        <b-form-input id="form-author-edit-input"
                      type="text"
                      v-model="editForm.LC"
                      required
                      placeholder="Enter LC">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-author-edit-group"
                    label="Function:"
                    label-for="form-author-edit-input">
          <b-form-input id="form-author-edit-input"
                        type="text"
                        v-model="editForm.MAJOR"
                        required
                        placeholder="Enter MAJOR">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="G/L account:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="editForm.MINOR"
                          required
                          placeholder="Enter MINOR">
            </b-form-input>
            <br><br>
          </b-form-group>
    <b-button type="submit" variant="primary">Update</b-button>
    <b-button type="reset" variant="danger">Cancel</b-button>
  </b-form>
</b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert'

export default {
  data () {
    return {
      books: [],
      addBookForm: {
        ID: ' ',
        LCTRYNUM: ' ',
        LC: ' ',
        MAJOR: ' ',
        MINOR: ' '
      },
      editForm: {
        ID: ' ',
        LCTRYNUM: ' ',
        LC: ' ',
        MAJOR: ' ',
        MINOR: ' '
      },
      message: '',
      showMessage: false
    }
  },
  components: {
    alert: Alert
  },
  methods: {
    getBooks () {
      const path = '/api/books'
      axios.get(path)
        .then((res) => {
          this.books = res.data.books
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
        })
    },
    addBook (payload) {
      const path = '/api/books'
      axios.post(path, payload)
        .then(() => {
          this.getBooks()
          this.message = 'Account added!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    updateBook (payload, ID) {
      const path = `/api/books/${ID}`
      axios.put(path, payload)
        .then(() => {
          this.getBooks()
          this.message = 'Account updated!'
          this.showMessage = true
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          this.getBooks()
        })
    },
    removeBook (ID) {
      const path = `/api/books/${ID}`
      axios.delete(path)
        .then(() => {
          this.getBooks()
          this.message = 'Account removed!'
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
      this.addBookForm.MAJOR = ''
      this.addBookForm.MINOR = ''
      this.editForm.ID = ''
      this.editForm.LCTRYNUM = ''
      this.editForm.LC = ''
      this.editForm.MAJOR = ''
      this.editForm.MINOR = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.addBookModal.hide()
      const payload = {
        LCTRYNUM: this.addBookForm.LCTRYNUM,
        LC: this.addBookForm.LC,
        MAJOR: this.addBookForm.MAJOR,
        MINOR: this.addBookForm.MINOR
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
        MAJOR: this.editForm.MAJOR,
        MINOR: this.editForm.MINOR
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
    }
  },
  created () {
    this.getBooks()
  }
}
</script>
