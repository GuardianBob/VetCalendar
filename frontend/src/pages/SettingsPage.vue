<template>
  <q-page class="" @keydown="checkForCtrlS">
    <div class="row justify-center">
      <div class="col-12 q-pa-md text-center">
        <h1 class="text-h4">{{ page_title }}</h1>
      </div>
      <div class="col-8 col-xs-12 col-lg-8 col-md-8 col-sm-10">
        <div v-for='(data, title) in settings' :key="title" class="col-12 q-pa-md text-left">
          <DataTablePopEdit :rowData="data.data" :columns="data.columns" :model="data.model" :parentFunc01="save" :title="title" separator="vertical" :add_item="true" @add_item="addNewItem"/>
        </div>
      </div>
      <div class="col-8 col-xs-10 col-lg-8 col-md-8 col-sm-10 q-my-md">
        <q-btn outline color="grey-8" class="q-px-xl q-mx-xs" size="md" label="Save" icon="save" @click="save()"/>
      </div>
    </div>
    <q-dialog v-model="new_item" transition-show="slide-down" transition-hide="slide-up">  
      <div class="dialog-60">
        <component :is="dynamicComponent" :getForm="get_form_api" :submitForm="save_form_api" :forms="forms" :closeButton="true" page_title="Add New Item" @done="user_created" columns="one"/>
      </div>    
    </q-dialog>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import { Notify } from "quasar"
import DataTablePopEdit from 'components/DataTablePopEdit.vue'
import FormTest from 'components/FormTest.vue';
import BaseForm from 'components/BaseForm.vue';
import APIService from "../../services/api"
import { api } from "boot/axios";

export default defineComponent({
  name: "ScheduleSettings",
  props: [
    'api_route',
    'page_title',
    'forms_input',
    'get_form_api',
    'save_form_api',
  ],
  components: {
    // Forms,
    DataTablePopEdit,
    // BaseForm,
  },
  data() {
    return {
      dynamicComponent: null,
      components: {
        FormTest,
        BaseForm
      }
    }
  },
  setup() {    
    return {
      show: ref(true),
      shift_settings: ref([]),
      type_settings: ref([]),
      shift_columns: ref([]),
      type_columns: ref([]),
      settings: ref(),
      forms: ref([]),
      new_item: ref(false),
    };
  },
  watch: {
    api_route: {
      immediate: true,
      handler(newValue) {
        console.log(newValue)
        this.get_settings()
      }
    },
    
  },
  computed: {
    
  },
  methods: {
    get_settings() {
      // get settings from database
      console.log(this.api_route)
      api.get(this.api_route).then(response => {
        console.log(response.data)   
        this.settings = response.data
      })
    },
    checkForCtrlS(event) {
      if (event.ctrlKey && event.key === 's') {
        this.save();
        event.preventDefault(); // Prevent the browser's default 'ctrl + S' behavior
      }
    },

    addNewItem(model) {
      console.log(model)
      console.log(this.forms_input)
      let obj = [
        { model: 'ShiftName', form: 'add_shift_info'}, 
        { model: 'ShiftType', form: 'add_shift_type' },
        ]
      console.log(this.forms_input.find(item => item.model === model).form)
      // if (model === 'ShiftName') {
      //   this.forms = ['add_shift_info']
      // } else if (model === 'ShiftType') {
      //   this.forms = ['add_shift_type']
      // }
      this.forms = [this.forms_input.find(item => item.model === model).form]
      console.log(this.get_form_api, this.forms)
      // this.get_form_api = `/get_model_form/${model}`
      // this.save_form_api = `/get_model_form`
      this.new_item = true
      // APIService.get_model_form(model).then((response) => {
      //   console.log(response.data)
      // })
    },

    save() {
      console.log(this.settings)
      api.post(this.api_route, this.settings)
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
    const componentName = process.env.VUE_APP_FORM_PAGE;
    this.dynamicComponent = this.components[componentName];
    // this.get_settings()
  },

})
</script>
