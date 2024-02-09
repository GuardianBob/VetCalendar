<template>
  <q-page class="">
    <div class="row justify-center">
      <div class="col-6 q-px-md text-left">
        <DataTablePopEdit :rowData="shift_settings" :columns="shift_columns" :parentFunc01="save" :title="pageTitle" separator="vertical"/>
        <!-- <q-btn color="secondary" dense class="q-px-sm q-mx-xs" size="sm" label="Reset" icon="cancel" @click="cancel_shift()"/> -->
        <q-btn color="primary" dense class="q-px-sm q-mx-xs" size="sm" label="Save" icon="save" @click="save_shift()"/>
      </div>
      <div class="col-6 q-px-md text-left">
        <DataTablePopEdit :rowData="type_settings" :columns="type_columns" :parentFunc01="save" :title="pageTitle" separator="vertical"/>
        <!-- <q-btn color="secondary" dense class="q-px-sm q-mx-xs" size="sm" label="Reset" icon="cancel" @click="cancel_shift()"/> -->
      </div>
      <q-btn color="primary" dense class="q-px-sm q-mx-xs" size="sm" label="Save" icon="save" @click="save_type()"/>
    </div>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
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
        console.log(transformedKey, key)
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

    save_type() {
      console.log(this.type_settings)
    },
      
  },

  created() {
  },
  
  mounted() {
    this.get_settings()
  },

})
</script>
