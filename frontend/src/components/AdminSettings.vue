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
      wrap-cells
      :separator="separator"
      :rows-per-page-options="[0]"
      hide-pagination
    >
      <template v-slot:body="props">
        <q-tr :props="props">
          <q-td v-for="row in columns" :key="row.name" :props="props">
            <div v-if="row.type == 'text'">
              <q-btn dense flat no-caps color="primary" size="16px">{{ props.row[row.name] }}</q-btn>
              <q-popup-edit v-model="props.row[row.name]" v-slot="scope">
                <q-input v-model="scope.value" dense autofocus @keyup.enter="scope.set" />
                <div class="text-center">
                  <q-btn v-close-popup label="OK" color="grey-8" size="sm" flat @click="scope.set"/>
                  <q-btn v-close-popup label="Cancel" color="deep-orange-13" size="sm" flat/>
                </div>
              </q-popup-edit>
            </div>
            <div v-else-if="row.type == 'textarea'">
              <q-btn dense flat no-caps color="primary" size="16px">{{ props.row[row.name] }}</q-btn>
              <q-popup-edit v-model="props.row[row.name]" v-slot="scope">
                <q-input type="textarea" v-model="scope.value" dense autofocus/>
                <div class="text-center">
                  <q-btn v-close-popup label="OK" color="grey-8" size="sm" flat @click="scope.set"/>
                  <q-btn v-close-popup label="Cancel" color="deep-orange-13" size="sm" flat/>
                </div>
              </q-popup-edit>
            </div>
            <div v-else-if="row.type == 'multi-select'">
              <q-btn dense flat no-caps color="primary" size="16px">{{ props.row[row.name] }}</q-btn>
              <q-popup-edit v-model="props.row[row.name]" v-slot="scope">
                <!-- <span>{{ row.name }}</span>
                <span>{{ cellOptions }}</span> -->
                <q-select        
                  :options="cellOptions.flat().filter(option => option.field == row.name).map(option => (option.label))"
                  v-model="scope.value"
                  :label="scope.label"
                  :id="key"
                  class="q-my-xs q-py-none"
                  outlined
                  multiple
                  use-chips
                  map-options
                  label-color="primary"
                  :rules="scope.required ? [rules.required] : []"
                  @update:modelValue="handleFieldSelected(scope.value)"
                >
                  <template v-if="scope.value" v-slot:append>
                    <q-icon name="cancel" color="red" @click.stop.prevent="scope.value = null" class="cursor-pointer" />
                  </template>
                </q-select>
                <div class="text-center">
                  <q-btn v-close-popup label="OK" color="grey-8" size="sm" flat @click="scope.set"/>
                  <q-btn v-close-popup label="Cancel" color="deep-orange-13" size="sm" flat/>
                </div>
              </q-popup-edit>
            </div>
            <div v-else-if="row.type == 'time'">
              <q-btn dense flat color="primary" size="16px">{{ props.row[row.name] }}</q-btn>
              <q-popup-edit v-model="props.row[row.name]" v-slot="scope">
                <q-time v-model="scope.value" flat autofocus @keyup.enter="scope.set" >
                  <div class="row items-center justify-end">
                    <q-btn v-close-popup label="OK" color="primary" flat @click="scope.set"/>
                    <q-btn v-close-popup label="Cancel" color="deep-orange-13" flat/>
                  </div>
                </q-time>
              </q-popup-edit>
            </div>
            <div v-else-if="row.type == 'color'" class="text-center">
              <q-btn :style="{backgroundColor: props.row[row.name], color: getTextColor(props.row[row.name])}" @click="showColorPicker = true">
                <span class="q-mx-md">
                  {{ props.row[row.name] }}
                  <q-icon size="xs" name="colorize" class="cursor-pointer q-ml-sm" />
                </span>
              </q-btn>
              <q-popup-proxy ref="colorPicker" transition-show="scale" transition-hide="scale">
                <q-color no-header-tabs default-view="palette" v-model="props.row[row.name]" @input="showColorPicker = false" />
              </q-popup-proxy>
            </div>            
            <div v-else>
              {{ props.row[row.name] }}
            </div>
          </q-td>
          <q-td v-if="delete_item">
            <q-btn dense flat class="q-px-sm q-mx-xs" color="negative" size="sm" icon="highlight_off" @click="deleteItem(props.row)">
              <q-tooltip class="bg-negative" anchor="bottom middle">Delete Item</q-tooltip>
            </q-btn>
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
    "cellOptions",
    "model",
    "separator",
    "add_item",
    "delete_item",
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
    delete_item: {
      immediate: true,
      handler() {
        console.log(this.columns)
      }
    }
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

    deleteItem(event) {
      console.log("clicked on delete \n", `model: ${this.model} \n`, event['id'])
      this.$emit('delete_item', { id: event['id'], model: this.model})
    },

    handleFieldSelected(event) {
      console.log("handleFieldSelected", event)
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


