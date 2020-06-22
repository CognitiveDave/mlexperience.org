<template>
  <div>
    <div class="container">
      <b-jumbotron>
        <p class="text-center">Welcome to the Design Sandbox</p>
      </b-jumbotron>
      <div class='row'>
        <div class='col-md4'>
        <div>
          <b-card title="Learning"
                  tag="article"
                  style="max-width: 20rem;"
                  class="md-2">
            <p class="card-text">
              Educate yourself!
            </p>
            <b-button href="#" variant="primary">Courses</b-button>
          </b-card>
        </div>
        </div>
        <div class='col-md4'>
        <div>
          <b-card title="Community"
                  tag="article"
                  style="max-width: 20rem;"
                  class="md-2">
            <p class="card-text">
              Tell them how to get support!
            </p>
            <b-button href="#" variant="primary">Support</b-button>
          </b-card>
        </div>

        </div>
        <div class='col-md4'>
        <div>
          <b-card title="Global Standards"
                  tag="article"
                  style="max-width: 20rem;"
                  class="md-2">
            <p class="card-text">
              Tell them why they need to be involved!
            </p>
            <b-button href="#" variant="primary">Get involved</b-button>
          </b-card>
        </div>
        </div>
      </div>
      <div class='row'><br><br></div>
    </div>
  </div>
</template>

<script>

export default {
  data () {
    return {}
  },
  components: {},
  methods: {created () {}}
}
</script>
