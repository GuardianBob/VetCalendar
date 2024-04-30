<template>
  <q-page class="" @keydown="checkForCtrlS">
    <div class="row justify-center">
      <div class="col-12 q-px-md text-center">
        <h1 class="text-h4">{{ page_title }}</h1>
      </div>
      <div class="col-8 col-xs-10 col-lg-8 col-md-8 col-sm-10 text-right">
        <q-btn outline color="grey-8" class="q-px-xl q-mx-xs" size="sm" label="Save" icon="save" @click="save()"/>
      </div>
      <div class="col-8">
        <q-card flat>
          <q-tabs
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            v-model="tab"
          >
            <span v-for='(data, title) in settings' :key="title">
              <q-tab :name="title" :label="title"/>
            </span>
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated v-for='(data, title) in settings' :key="title">
            <q-tab-panel :name="title" class="q-pa-none">
              <AdminSettings 
                :rowData="data.data" 
                :columns="data.columns" 
                :model="data.model" 
                :parentFunc01="save" 
                :title="title" 
                separator="vertical" 
                :add_item="true" 
                @add_item="addNewItem" 
                :delete_item="true" 
                @delete_item="deleteItem"
              />
            </q-tab-panel>

            <!-- <q-tab-panel name="schedule">
              <div class="text-h6">Scheduling Tools</div>
              <div class="col-12 q-my-sm">
                <q-btn class="q-mx-xs" color="accent" id="add_shifts" :size="button_size" @click="quick_add" icon="more_time" label="Quick Add"></q-btn>
                <q-btn class="q-mx-xs" color="secondary" id="upload" :size="button_size" @click="upload_file = true" icon="upload_file" label="Upload"></q-btn>
              </div>
            </q-tab-panel>

            <q-tab-panel name="admin">
              <div class="text-h6">Admin Tools</div>
              <div class="col-4 q-my-sm">
                <q-btn class="q-mx-xs" color="negative" id="clear_shifts" :size="button_size" @click="confirm = true" icon="cancel" label="Clear Month"></q-btn>
              </div>
            </q-tab-panel> -->
          </q-tab-panels>
        </q-card>
        <!-- <div v-for='(data, title) in settings' :key="title" class="col-12 q-pa-md text-left">
          <DataTablePopEdit 
            :rowData="data.data" 
            :columns="data.columns" 
            :model="data.model" 
            :parentFunc01="save" 
            :title="title" 
            separator="vertical" 
            :add_item="true" 
            @add_item="addNewItem" 
            :delete_item="true" 
            @delete_item="deleteItem"
          />
        </div> -->
      </div>
      
    </div>
    <q-dialog v-model="new_item" transition-show="slide-down" transition-hide="slide-up">  
      <div class="dialog-60">
        <component :is="dynamicComponent" :getForm="get_form_api" :submitForm="save_form_api" :forms="forms" :closeButton="true" page_title="Add New Item" @done="item_created" columns="one"/>
      </div>    
    </q-dialog>
    <q-dialog v-model="confirm" persistent>
      <ConfirmDialog 
        :doubleVerify="false"
        :text="confirm_text"
        @confirmed="confirm_delete"
      />
    </q-dialog>
  </q-page>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
import { Notify } from "quasar"
import AdminSettings from 'components/AdminSettings.vue'
import FormTest from 'components/FormTest.vue';
import BaseForm from 'components/BaseForm.vue';
import APIService from "../../services/api"
import { api } from "boot/axios";
import ConfirmDialog from "components/ConfirmDialog.vue";

export default defineComponent({
  name: "AdminPage",
  props: [
    'api_route',
    'page_title',
    'forms_input',
    'get_form_api',
    'save_form_api',
  ],
  components: {
    // Forms,
    AdminSettings,
    ConfirmDialog,
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
      tab: ref('shift_label'),
      splitterModel: ref(20),
      show: ref(true),
      shift_settings: ref([]),
      type_settings: ref([]),
      shift_columns: ref([]),
      type_columns: ref([]),
      settings: ref(),
      forms: ref([]),
      new_item: ref(false),
      confirm: ref(false),
      confirm_text: ref('Are you sure you want to delete this item?'),
      item_data: ref(),      
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
        console.log(Object.keys(response.data)[0])   
        this.tab = Object.keys(response.data)[0]
        this.settings = response.data
      })
    },
    checkForCtrlS(event) {
      if (event.ctrlKey && event.key === 's') {
        this.save();
        event.preventDefault(); // Prevent the browser's default 'ctrl + S' behavior
      }
    },

    item_created() {
      this.new_item = false
      this.get_settings()
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

    deleteItem(event){
      // console.log(event["model"], '\n', event['id'], '\n', this.api_route)
      this.item_data = event
      this.confirm = true
    },

    confirm_delete(event) {
      this.confirm = false
      // console.log(event, '\n', this.item_data)
      if (event) {
        api.delete(this.api_route, {data: this.item_data})
        .then((response) => {
          // console.log(response.data)
          this.get_settings()
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
      }
    },

    save() {
      console.log(this.settings)
      api.post(this.api_route, this.settings)
      .then((response) => {
        console.log(response.data)
        this.get_settings()
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
