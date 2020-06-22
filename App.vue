<template>
  <div id="app">
    <navman></navman>
    <alert :message=mess_alr v-if="alerter"></alert>
    <router-view/>
    <foot></foot>
   </div>
</template>

<script>
import NavBar from './components/nav'
import Footer from './components/footer'
import Alerter from './components/Alert'

export default {
  name: 'App',
  data () {
    return {
      timer: 25,
      interval: null,
      counter: false,
      mess_alr: 'You are now being logged out',
      alerter: false
    }
  },
  components: {
    navman: NavBar,
    foot: Footer,
    alert: Alerter
  },
  created () {
    this.mess_alr = 'create'
    // this.inactivityTime()
    this.alerter = false
  },
  mounted: function () {
    this.mess_alr = 'mounted'
    this.inactivityTime()
    this.alerter = false
  },
  methods: {
    inactivityTime () {
      document.onload = this.resetTimer
      document.onmousemove = this.resetTimer
      document.onmousedown = this.resetTimer
      document.ontouchstart = this.resetTimer
      document.onclick = this.resetTimer
      document.onscroll = this.resetTimer
      document.onkeypress = this.resetTimer
    },
    logout () {
      location.href = '/logout'
    },
    resetTimer () {
      clearTimeout(this.interval)
      this.interval = setTimeout(this.countDown, 1000000)
    },
    countDown () {
      clearTimeout(this.interval)
      this.mess_alr = 'auto time out'
      this.alerter = true
      this.logout()
    }
  }
}

</script>

<style>
#app {
  margin-top: 30px
}
</style>
