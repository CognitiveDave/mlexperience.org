<template>
  <div>
      <div class='container'>
        <navman></navman>
        <p> Current Country: {{ cur_country }} current Ledger: {{ cur_led }} </p>
              <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="onSetCountry('866','10')">
                  Set Selection
              </button>
        <foot></foot>
        </div>
  </div>
</template>

<script>
import NavBar from './nav'
import Footer from './footer'

export default {
  data () {
    return {

    }
  },
  components: {
    navman: NavBar,
    foot: Footer
  },
  methods: {
    created () {},
    onSetCountry (cty, lc) {
      console.log(cty, lc)
      this.$store.commit('selectcountry', cty)
      this.$store.commit('selectledger', lc)
    }
  },
  computed: {
    cur_country () {
      return this.$store.state.activecountry
    },
    cur_led () {
      return this.$store.state.activeledger
    }
  }
}
</script>
