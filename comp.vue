<template>
  <div class='container'>
      <br>
    <div class='row'>
        <b-col>
        <b-btn size='sm' @click="showCollapse = !showCollapse"
                   :class="showCollapse ? 'collapsed' : null"
                   aria-controls="collapse1"
                   :aria-expanded="showCollapse ? 'true' : 'false'">
                   Local</b-btn>
        <b-collapse id="collapse1" class="mt-2" v-model="showCollapse">
        <b-card>
        <p>Currency: {{account[0].local}}</p>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Item</th>
              <th scope="col">Year</th>
              <th scope="col">Y-1</th>
              <th scope="col">Y-2</th>
              </tr>
          </thead>
          <tbody>
            <tr v-if="view_lvl == line.lvl" v-for="(line, index) in account[0].entry" :key="index">
              <td> {{ line.entry_des }} </td>
              <td>{{ line.cur.local }}</td>
              <td>{{ line.pre.local }}</td>
              <td>{{ line.pre_pre.local }}</td>
            </tr>
              <p v-if="(account[0].max_lvl-view_lvl)>0"> <b-button size='sm' @click="expanded = false; view_lvl = view_lvl+1"> + </b-button></p>
              <p v-if="view_lvl > 0"><b-button size='sm' @click="expanded = false; view_lvl = view_lvl-1">-</b-button></p>
              <p> Lvl {{view_lvl}} of {{account[0].max_lvl}} </p>
          </tbody>
        </table>
        </b-card>
        </b-collapse>
        </b-col>
        <div v-if="expanded == false">
        <b-col>
        <b-btn size='sm' @click="showCollapse_usd = !showCollapse_usd"
                   :class="showCollapse_usd ? 'collapsed' : null"
                   aria-controls="collapse2"
                   :aria-expanded="showCollapse_usd ? 'true' : 'false'">
                   Dollar</b-btn>
        <b-collapse id="collapse2" class="mt-2" v-model="showCollapse_usd">
        <b-card>
        <p>Currency: USD</p>
        <table class="table table-hover">
          <thead>
            <tr>
            <th scope="col"> </th>
            <th scope="col">Item</th>
            <th scope="col">Year</th>
            <th scope="col">Y-1</th>
            <th scope="col">Y-2</th>
              </tr>
          </thead>
          <tbody>
            <tr v-for="(line, index) in account[0].entry" :key="index">
              <td><b-button size='sm'>+</b-button></td>
              <td>{{ line.entry_des }}</td>
              <td>{{ line.cur.USD }}</td>
              <td>{{ line.pre.USD }}</td>
              <td>{{ line.pre_pre.USD }}</td>
            </tr>
          </tbody>
        </table>
        </b-card>
        </b-collapse>
        </b-col>
        </div>
        <div v-if="expanded == false">
        <b-col>
        <b-btn size='sm' @click="showCollapse_veg = !showCollapse_veg"
                   :class="showCollapse_veg ? 'collapsed' : null"
                   aria-controls="collapse3"
                   :aria-expanded="showCollapse_veg ? 'true' : 'false'">
                   Graphic</b-btn>
        <b-collapse id="collapse3" class="mt-2" v-model="showCollapse_veg">
        <b-card>
        <div class='dashboard'>
          <vega-lite :data="veg.values" mark="bar" :encoding="veg.encoding"/>
          </div>
        </b-card>
        </b-collapse>
        </b-col>
        </div>
      </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      showCollapse: true,
      showCollapse_usd: false,
      showCollapse_veg: false,
      expanded: false,
      view_lvl: 0,
      account: [{
        cty: '754',
        lc: '30',
        yr: 2018,
        local: 'EUR',
        entries: 3,
        max_lvl: 1,
        'entry': [
          {
            entry_des: 'profit',
            cur: {
              local: 0,
              USD: 0},
            pre: {
              local: 0,
              USD: 0},
            pre_pre: {
              local: 0,
              USD: 0},
            index: 1,
            lvl: 0
          },
          {
            entry_des: 'taxes',
            cur: {
              local: 0,
              USD: 0},
            pre: {
              local: 0,
              USD: 0},
            pre_pre: {
              local: 0,
              USD: 0},
            index: 1,
            lvl: 1
          },
          {
            entry_des: 'pti',
            cur: {
              local: 0,
              USD: 0},
            pre: {
              local: 0,
              USD: 0},
            pre_pre: {
              local: 0,
              USD: 0},
            index: 1,
            lvl: 1
          }]}],
      veg: {
        values: [
          {a: 'A', b: 28}, {a: 'B', b: 55}, {a: 'C', b: 43},
          {a: 'D', b: 91}, {a: 'E', b: 81}, {a: 'F', b: 53},
          {a: 'G', b: 19}, {a: 'H', b: 87}, {a: 'I', b: 52}],
        encoding: {
          x: {field: 'a', type: 'ordinal'},
          y: {field: 'b', type: 'quantitative'}
        }
      }
    }
  },
  components: {
  },
  methods: {}
}
</script>
