// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import VueVega from 'vue-vega'
import App from './App'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import VueLocalStorage from 'vue-localstorage'
import Vuex from 'vuex'
import {version} from '../../frontend/package.json'
Vue.use(Vuex)
Vue.config.devtools = true

// the root, initial state object
const state = {
  countries: [],
  ledgers: [],
  activecountry: 'IE',
  activeledger: 'Ltd',
  user: {},
  version: ' '
}

const actions = {
  selectcountry (context) {
    context.commit('selectcountry')
  },
  selectledger (context) {
    context.commit('selectledger')
  }
}

// define the possible mutations that can be applied to our state
const mutations = {
  selectcountry (state, country) {
    state.activecountry = country
  },
  selectledger (state, ledger) {
    state.activeledger = ledger
  },
  initialiseStore (state) {
    if (localStorage.getItem('store')) {
      let store = JSON.parse(localStorage.getItem('store'))
      if (store.version === version) {
        this.replaceState(
          Object.assign(state, store)
        )
      } else {
        state.version = version
      }
    }
  }
}

// create the Vuex instance by combining the state and mutations objects
// then export the Vuex store for use by our components
const store = new Vuex.Store({
  state: state,
  mutations: mutations,
  actions: actions
})

Vue.use(VueLocalStorage, {
  name: 'store',
  bind: true
})
Vue.config.productionTip = false
Vue.use(VueVega)
Vue.use(BootstrapVue)

/* eslint-disable no-new */
new Vue({
  store,
  el: '#app',
  beforeCreate () {
    this.$store.commit('initialiseStore')
  },
  router,
  components: { App },
  template: '<App/>'
})

store.subscribe((mutation, state) => {
  localStorage.setItem('store', JSON.stringify(store.state))
})
