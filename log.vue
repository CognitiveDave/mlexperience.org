<template>
  <div class='container'>
    <div class='row'>
      <br>
    </div>
    <div class='row'>
      <div class="col-sm-10">
        <button
          type="button"
          class="btn btn-danger btn-sm"
          @click="onRefresh">
              Refresh
        </button>
      </div>
      <div class="col-sm-10">
        <div class='dashboard'>
          <vega-lite :data="veg.values" mark="bar" :encoding="veg.encoding"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      stats: [],
      veg: {
        'values': [
          {'ip_city': 'Dublin', 'c': 1}, {'ip_city': 'Dubllin', 'c': 1}, {'ip_city': 'Dublin', 'c': 1},
          {'ip_city': 'Mayo', 'c': 1}, {'ip_city': 'Fre', 'c': 1}, {'ip_city': 'Fdf', 'c': 1}
        ],
        'title': 'By Country',
        'mark': 'bar',
        'encoding': {
          'y': {'field': 'ip_city',
            'type': 'ordinal',
            'axis': {'title': 'Cities'}
          },
          'x': {'field': 'c',
            'aggregate': 'sum',
            'type': 'quantitative',
            'axis': {'title': 'Request count'}
          }
        }
      }
    }
  },
  components: {
  },
  methods: {
    onRefresh () {
      this.getStats()
    },
    getStats () {
      const path = '/api/stats'
      axios.get(path)
        .then((res) => {
          this.veg.values = res.data.log
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.error(error)
        })
    }
  }
}
</script>
