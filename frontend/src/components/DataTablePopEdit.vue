<template>
  <div class="row full-width justify-around ">
    <div class="col-12 text-center text-body1 text-weight-medium" style="font-size:20px">{{ title }}</div>
    <q-table
      :rows="rowData"
      :columns="columns"
      row-key="name"
      class="col-12"
      flat
      dense
      :separator="separator"
      :rows-per-page-options="[0]"
      hide-pagination
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="col in columns" :key="col.name" :props="props">
            <div v-if="col.type == 'text'">
              <q-btn dense flat no-caps color="primary" size="16px">{{ props.row[col.name] }}</q-btn>
              <q-popup-edit v-model="props.row[col.name]" v-slot="scope">
                <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set" />
                <div class="text-center">
                  <q-btn v-close-popup label="OK" color="grey-8" size="sm" flat @click="scope.set"/>
                  <q-btn v-close-popup label="Cancel" color="deep-orange-13" size="sm" flat/>
                </div>
              </q-popup-edit>
            </div>
            <div v-else-if="col.type == 'textarea'">
              <q-btn dense flat no-caps color="primary" size="16px">{{ props.row[col.name] }}</q-btn>
              <q-popup-edit v-model="props.row[col.name]" v-slot="scope">
                <q-input type="textarea" v-model="scope.value" dense autofocus/>
                <div class="text-center">
                  <q-btn v-close-popup label="OK" color="grey-8" size="sm" flat @click="scope.set"/>
                  <q-btn v-close-popup label="Cancel" color="deep-orange-13" size="sm" flat/>
                </div>
              </q-popup-edit>
            </div>
            <div v-else-if="col.type == 'time'">
              <q-btn dense flat color="primary" size="16px">{{ props.row[col.name] }}</q-btn>
              <q-popup-edit v-model="props.row[col.name]" v-slot="scope">
                <q-time v-model="scope.value" flat autofocus @keyup.enter="scope.set" >
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="OK" color="primary" flat @click="scope.set"/>
                    <q-btn v-close-popup label="Cancel" color="deep-orange-13" flat/>
                  </div>
                </q-time>
              </q-popup-edit>
            </div>
            <div v-else-if="col.type == 'color'" class="text-center">
              <q-btn :style="{backgroundColor: props.row[col.name], color: getTextColor(props.row[col.name])}" @click="showColorPicker = true">
                <span class="q-mx-md">
                  {{ props.row[col.name] }}
                  <q-icon size="xs" name="colorize" class="cursor-pointer q-ml-sm" />
                </span>
              </q-btn>
              <q-popup-proxy ref="colorPicker" transition-show="scale" transition-hide="scale">
                <q-color no-header-tabs default-view="palette" v-model="props.row[col.name]" @input="showColorPicker = false" />
              </q-popup-proxy>
            </div>
            <div v-else>
              {{ props.row[col.name] }}
            </div>
          </q-td>
        </q-tr>
      </template>
      <template v-slot:no-data="{ icon, message, filter }">
        <div class="full-width row flex-center text-accent q-gutter-sm">
          <q-icon size="2em" name="sentiment_dissatisfied" />
          <span>
            Well this is sad... {{ message }}
          </span>
          <q-icon size="2em" :name="filter ? 'filter_b_and_w' : icon" />
        </div>
      </template>
      <template v-if="add_item" v-slot:bottom>
        <q-tr class="">
          <q-btn icon="add" round color="accent" @click="addItem"></q-btn>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"

export default {
  name: "DataTable",
  props: [
    "columns",
    "rowData",
    "model",
    "separator",
    "add_item",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
    "parentFunc04",
    "parentFunc05",
    "title"],
  setup() {
    return {
      info: ref(false),
      userData: ref([]),
      pageTitle: ref(''),   
      newItem: ref({}),
    }
  },

  watch: {
    
  },

  computed: {
    
  },

  methods: {
    editBtn(data) {
      this.parentFunc01(data)
    },

    addItem() {
      this.$emit('add_item', this.model)
      // this.newItem = {};
    },

    getBrightness(color) {
      let r, g, b, hsp;
      if (color.match(/^rgb/)) {
        color = color.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d+(?:\.\d+)?))?\)$/);
        r = color[1];
        g = color[2];
        b = color[3];
      } else {
        color = +("0x" + color.slice(1).replace(color.length < 5 && /./g, '$&$&'));
        r = color >> 16;
        g = color >> 8 & 255;
        b = color & 255;
      }
      hsp = Math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b));
      return hsp;
    },

    getTextColor(color) {
      return this.getBrightness(color) > 175 ? '#000000' : '#ffffff';
    },
  },

  mounted() {
    // this.userData = this.rowData
    this.pageTitle = this.title
  }
};
</script>


