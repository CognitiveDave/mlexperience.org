<template>
  <div>
    <div class="container">
        <div class="jumbotron">
            <h3>Your Profile</h3>
            <p>Your settings, privacy, subscriptions,  and activity log</p>
        </div>
      <b-card no-body>
      <b-tabs pills card>
        <b-tab title="Your details" active>
          Tab Contents 1
        </b-tab>
        <b-tab title="Your assignments">
          Tab Contents 2
        </b-tab>
        <b-tab title="Your settings">
          Tab Contents 3
        </b-tab>
        <b-tab title="Activity">
          Tab Contents 4
        </b-tab>
        <b-tab title="Notifications">
          Tab Contents 5
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</div>
</template>

<script>

export default {
  data () {
    return {}
  },
  components: { },
  methods: {created () {}}
}
</script>
