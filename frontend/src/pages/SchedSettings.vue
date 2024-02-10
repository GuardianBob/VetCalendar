<template>
  <q-page class="">
    <div class="row justify-center">
      <div class="col-8">
        <div class="col-12 q-pa-md text-left">
          <DataTablePopEdit :rowData="shift_settings" :columns="shift_columns" :parentFunc01="save" title="Shift Time Settings" separator="vertical"/>
          <!-- <q-btn color="secondary" dense class="q-px-sm q-mx-xs" size="sm" label="Reset" icon="cancel" @click="cancel_shift()"/> -->
          <!-- <q-btn color="primary" dense class="q-px-sm q-mx-xs" size="sm" label="Save" icon="save" @click="save_shift()"/> -->
        </div>
        <div class="col-12 q-pa-md text-left">
          <DataTablePopEdit :rowData="type_settings" :columns="type_columns" :parentFunc01="save" title="Shift Type Settings" separator="vertical"/>
          <!-- <q-btn color="secondary" dense class="q-px-sm q-mx-xs" size="sm" label="Reset" icon="cancel" @click="cancel_shift()"/> -->
        </div>
      </div>
      <div class="col-8 q-my-md">
        <q-btn outline color="grey-8" class="q-px-xl q-mx-xs" size="md" label="Save" icon="save" @click="save()"/>
      </div>
    </div>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import { Notify } from "quasar"
import DataTablePopEdit from 'components/DataTablePopEdit.vue'
import APIService from "../../services/api"

export default defineComponent({
  name: "ScheduleSettings",
  components: {
    // vue linter no use error bypass

    // Forms,
    DataTablePopEdit,
  },
  data() {
    return {
    }
  },
  setup() {    
    return {
      show: ref(true),
      shift_settings: ref([]),
      type_settings: ref([]),
      shift_columns: ref([]),
      type_columns: ref([])
    };
  },
  watch: {
    
  },
  computed: {
    
  },
  methods: {
    get_settings() {
      // get settings from database
      APIService.schedule_settings().then(response => {
        console.log(response.data)        
        this.shift_settings = response.data.shift_settings  
        this.type_settings = response.data.type_settings 
        this.shift_columns = this.get_headers(this.shift_settings)
        this.type_columns = this.get_headers(this.type_settings)
      })
    },

    get_headers(array) {
      let obj = array[0];
      const transformedEntries = Object.entries(obj)
      .filter(([key, value]) => !key.includes('id'))
      .map(([key, value]) => {
        const transformedKey = key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        // console.log(transformedKey, key)
        let type = "text"
        if (key.includes('time')) {
          type = "time"
        }
        if (key.includes('color')) {
          type = "color"
        }
        if (key.includes('id') || key.includes('name')) {
          type = "fixed"
        }
        return {"name": key, "label": transformedKey, "field": key, sortable: true, align: 'left', "type": type};
      });
      // console.log(transformedEntries)
      return transformedEntries
    },

    save_shift() {
      console.log(this.shift_settings)
    },

    cancel_shift() {
      this.get_settings()
    },

    save() {
      console.log(this.type_settings)
      APIService.schedule_settings({shift_settings: this.shift_settings, type_settings: this.type_settings})
      .then((response) => {
        console.log(response.data)
        Notify.create({
          message: response.data.message,
          color: "green",
          textColor: "white",
          position: "center",
          timeout: 3000,
        });
      })
      .catch((error) => {
        console.log(error.response.data);
        Notify.create({
          message: error.response.data.error,
          color: "red",
          textColor: "white",
          position: "center",
          timeout: 3000,
        });
      });
    },
      
  },

  created() {
  },
  
  mounted() {
    this.get_settings()
  },

})
</script>
