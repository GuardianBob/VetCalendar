<template>
  <!-- <q-page class="items-center flex flex-center"> -->
    <div class="row justify-center">
      <!-- <q-dialog v-model="show"> -->
        <!-- <Forms /> -->
        <!-- <FormTest :getForm="get_form_api" :multiDateSelect="true" :submitForm="save_form_api" :closeButton="true" page_title="Build Form" @done="submitted" columns="one"/> -->
      <!-- </q-dialog> -->
      <div class="col-10 q-pt-md">
        <div class="q-pa-m">
          <q-input
            v-model="formJSON"
            filled
            type="textarea"
            :placeholder="placeholder"
          />
          <q-btn
            label="Submit"
            color="primary"
            @click="submit"
          />
        </div>
      </div>
    </div>
  <!-- </q-page> -->
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
// import Forms from 'components/Forms.vue'
// import FormTest from 'components/FormTest.vue'
import APIService from "../../services/api";

export default defineComponent({
  name: "FormsPage",
  components: {
    // vue linter no use error bypass

    // Forms,
    // FormTest,
  },
  data() {
    return {
    }
  },
  setup() {    
    return {
      show: ref(true),
      formJSON: ref(''),
      placeholder: ref(''),
      // get_form_api: ref("/get_formbuilder_form/add_shift/12"),
      // save_form_api: ref("/submit_formbuilder_form"),
    };
  },
  watch: {
    
  },
  computed: {

  },
  methods: {
    update_form_json(){
      this.placeholder = `
      {
        "form_name": "Add Shift", 
        "module": "VetCalendar", 
        "table": "Shifts", 
        "fields": {
          "user": {"label": "User", "type": "select", "value": "None", "required": true, "model_edit_field": "user_id"},
          "shift": {"label": "Shift", "type": "select", "value": "None", "required": true, "model_edit_field": "shift_name_id"},
          "shift_type": {"label": "Shift Type", "type": "select", "value": "None", "required": true, "model_edit_field": "shift_type_id"},
          "shift_date": {"label": "Shift Date", "type": "date", "value": "None", "required": true,"model_edit_field": "shift_start"}
        },
        "field_options": {
          "shift": {"field": "shift", "related_model": "ShiftName", "option_label": "shift_label", "option_value": "id", "type": "select"},
          "shift_type": {"field": "shift_type", "related_model": "ShiftType", "option_label": "type_label", "option_value": "id", "type": "select"},
          "user": {"field": "user", "related_model": "User", "option_label": "last_name", "option_value": "id", "type": "select"}
        },
        "custom_options": {},
        "save_function": "add_user",
      }
      `
    },
    submit(){
      this.formJSON = this.formJSON.replace(/\n/g, '');
      APIService.add_json_form(this.formJSON).then((response) => {
        console.log(response);
      });
    },
  },

  created() {
  },
  
  mounted() {
    this.update_form_json()
    // APIService.get_formbuilder_form().then((response) => {
    //   console.log(response);
    // });
  },

})
</script>
