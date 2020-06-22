<template>
<div class='container'>
  <b-navbar type="dark" variant="primary" toggleable>
    <b-navbar-toggle target="nav_dropdown_collapse"></b-navbar-toggle>
    <b-collapse is-nav id="nav_dropdown_collapse">
      <b-navbar-nav>
        <b-nav-item href="/">Home</b-nav-item>
        <!-- Navbar dropdowns -->
        <b-nav-item-dropdown text="Manage" right>
          <b-dropdown-item href="/taxr">Reporting Home</b-dropdown-item>
          <b-dropdown-item href="/books">Master Data</b-dropdown-item>
          <b-dropdown-item href="/income">Taxes</b-dropdown-item>
          <b-dropdown-item href="/projs">Filings</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Planning" right>
          <b-dropdown-item href="/taxp">Planning Home</b-dropdown-item>
          <b-dropdown-item href="/books">Master Data</b-dropdown-item>
          <b-dropdown-item href="#">Financials</b-dropdown-item>
          <b-dropdown-item href="#">Manage</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Reports" right>
          <b-dropdown-item href="/reports">Reporting</b-dropdown-item>
          <b-dropdown-item href="/logs">Log</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="Reference" right>
          <b-dropdown-item href="/ref">References</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item-dropdown text="User" right>
          <b-dropdown-item href="/Profile">Profile</b-dropdown-item>
          <b-dropdown-item href="/messages">Messages <b-badge variant="danger">4</b-badge> </b-dropdown-item>
          <b-dropdown-item href="/logout">Logout</b-dropdown-item>
        </b-nav-item-dropdown>
        <b-nav-item href="/contact">Contact</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
      <b-button variant='success' @click="onSetCountry()">
        <b-badge variant="success">Status: {{cur_country}}: {{cur_led}}</b-badge>
      </b-button>
  </b-navbar>
      <b-modal ref="selector" id="selector" title="Selection" hide-footer>
        <div class='container'>
          <b-form @submit="onSubmit" @reset="onReset" class="w-100">
            <b-form-group id="form-title-group" label="Country:" label-for="form-title-input">
              <b-form-input id="form-title-input" type="text" v-model="selectForm.country" required placeholder="nnn">
            </b-form-input>
            </b-form-group>
            <b-form-group id="form-title-group" label="Legal Entity:" label-for="form-title-input">
              <b-form-input id="form-title-input" type="text" v-model="selectForm.ledger" required placeholder="nn">
            </b-form-input>
            </b-form-group>
            <b-form-group id="form-title-group" label="Year:" label-for="form-title-input">
              <b-form-input id="form-title-input" type="text" v-model="selectForm.year" required placeholder="yyyy">
              </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
          </div>
        </b-modal>
 </div>
</template>

<script>

export default {
  data () {
    return {
      select: false,
      cty: '',
      lc: '',
      selectForm: {
        country: ' ',
        ledger: ' ',
        year: ''
      }
    }
  },
  components: {},
  methods: {
    created () {},
    onSetCountry () {
      this.$refs.selector.show()
      this.selectForm.country = this.cur_country
      this.selectForm.ledger = this.cur_led
    },
    onReset (evt) {
      evt.preventDefault()
      this.$refs.selector.hide()
      this.initForm()
    },
    initForm () {
      this.selectForm.country = ''
      this.selectForm.ledger = ''
      this.selectForm.year = ''
    },
    onSubmit (evt) {
      evt.preventDefault()
      this.$refs.selector.hide()
      this.$store.commit('selectcountry', this.selectForm.country)
      this.$store.commit('selectledger', this.selectForm.ledger)
      this.initForm()
      this.used = true
    }
  },
  computed: {
    cur_country () {
      return this.$store.state.activecountry
    },
    cur_led () {
      return this.$store.state.activeledger
    },
    check_scope () {
      return false
    }
  }
}
</script>
