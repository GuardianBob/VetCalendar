<template>
  <div class="row justify-center" >
    <div class="col-12 justify-right text-right" v-if="closeButton">
      <q-btn class="q-pt-md" color="primary" flat v-close-popup icon="close"/>
    </div>
    <div class="col-12 text-center">
      <h1 class="text-h3 text-primary">{{ page_title }}</h1>
    </div>
    <q-form>
      <div v-for="(data, title) in formData" :key="title" class="row justify-center">
        <div class="row justify-center">
          <div class="col-12 col-md-12 col-lg-12">
            <h4 class="text-h5 q-mt-md q-mb-none text-bold">{{ title }}</h4>
          </div>
          <div v-for="(field, key) in data" :key="key" :class="cols">
            <q-input 
              v-if="field.type === 'input' || field.type === 'number' || field.type === 'url' || field.type === 'time' || field.type === 'datetime-local' || field.type === 'search' || field.type === 'color' || field.type === 'file' || field.type === 'month' || field.type === 'week' || field.type === 'range' || field.type === 'textarea'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
              :rules="[field.required ? requiredRule : '']"
            />
            <q-input 
              v-else-if="field.type === 'email'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              outlined
              label-color="primary"
              :rules="[rules.required, rules.email]"
            /> 
            <q-input 
              v-else-if="field.type === 'tel'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              mask="(###) ###-####"
              fill-mask
              outlined
              label-color="primary"
            /> 
            <q-input 
              v-else-if="field.type === 'password'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="isPwd ? 'password' : 'text'"
              outlined
              label-color="primary"
              :rules="[field.required ? requiredRule : '']"
            > 
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" @click="isPwd = !isPwd" />
              </template>
            </q-input>
            <q-select
              v-else-if="field.type === 'select' && key === 'state'"
              v-model="field.value"
              :label="field.label"
              :id="key"
              :options="states.map(state => ({label: Object.values(state)[0], value: Object.keys(state)[0]}))"
              class="q-my-xs q-py-none"
              outlined
              label-color="primary"
              map-options
              :rules="[field.required ? requiredRule : '']"
            />
            <q-select
              v-else-if="field.type === 'select'"
              :options="options.filter(option => option.field === key).map(option => ({label: option.label, value: option.option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              map-options
              label-color="primary"
              :rules="[field.required ? rules.required : '']"
            />
            <q-input
              v-else-if="field.type === 'date'"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              label-color="primary"
              :rules="[field.required ? requiredRule : '']"
              >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="field.value" mask="MMM DD YYYY" multiple>
                      <div class="row items-center justify-end">
                        <q-btn label="Clear" color="negative" flat dense class="q-mr-sm" @click="field.value = ''" /> 
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <span v-else></span>
          </div>
        </div>
      </div>
      <div class="row justify-around q-my-md">
        <q-btn @click="submit" color="primary">Save</q-btn>
      </div>
    </q-form>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
import { useQuasar, Notify } from "quasar";
import APIService from "../../services/api";
import ValidateService from "../../services/ValidateService";
import { api } from "boot/axios";
import statesJson from "components/states.json";

export default defineComponent({
  props: [
    "page_title",
    "getForm",
    "submitForm",
    "form_data",
    "form_options",
    "closeButton",
    "editButton",
    "columns",
    "parentFunc01",
    "parentFunc02",
    "parentFunc03",
    "parentFunc04",
    "parentFunc05",
  ],

  setup() {
    return {};
  },
  data() {
    return {
      loading: false,
      formData: ref(this.form_data),
      options: ref(this.form_options),
      states: ref(statesJson.states),
      isPwd: ref(true),
      isRequired: ref(false),
      rules: ref(ValidateService.validators),
      requiredRule: val => (val && val.length > 0) || 'This field is required',
      one: ref('col-12 col-sm-12 col-md-12 col-lg-12 q-px-sm f-field'),
      two: ref('col-10 col-sm-6 col-md-6 col-lg-6 q-px-sm f-field'),
      cols: ref('')

    };
  },

  watch: {
    formData: {
      deep: true,
      handler(newVal) {
        if (newVal[''] && newVal[''].shift_date && newVal[''].shift_date.value) {
          const dateRanges = newVal[''].shift_date.value;
          console.log(dateRanges);
        }
      },
    },
    columns: {
      immediate: true,
      handler(newValue) {
        console.log(newValue);
        if (newValue === "one") {
          this.cols = this.one;
        } else {
        this.cols = this.two;
        }
      }
    },
  },

  methods: {
    isValidEmail(event) {
      console.log(event);
      const regex = /^[A-Za-z0-9+_.-]+@(.+)$/;
      return regex.test(event);
    },

    submit(event) {
      try {
        console.log(this.formData)
        // RETURNS VALUES ONLY 
        // const values = Object.values(this.formData).map(item => item.value);

        // ACCOUNTS FOR NESTED OBJECTS
        // const values = Object.values(this.formData).map(item => {
        //   if (typeof item.value === 'object' && item.value !== null) {
        //     return item.value.value;
        //   }
        //   return item.value;
        // });
        // console.log(values);

        // // RETURNS KEY VALUE PAIRS AND ACCOUNTS FOR NESTED OBJECTS
        // const entries = Object.entries(this.formData).map(([key, item]) => {
        //   let value;
        //   if (typeof item.value === 'object' && item.value !== null) {
        //     value = item.value.value;
        //   } else {
        //     value = item.value;
        //   }
        //   return { key, value };
        // });

        // RETURNS KEY VALUE PAIRS AND ACCOUNTS FOR NESTED OBJECTS WITHIN NESTED OBJECTS.
        // YEAH, I know it's bad, but it works.
        const entries = Object.entries(this.formData).map(([key, item]) => {
          let value;
          if (typeof item === 'object' && item !== null) {
            // console.log("===> ", value)
            value = Object.entries(item).reduce((acc, [subKey, subItem]) => {
              if (typeof subItem.value === 'object' && subItem !== null) {
                if (Array.isArray(subItem.value)) {
                  // console.log(subItem.value)
                  // If subItem.value is an array, assign it directly to acc[subKey]
                  acc[subKey] = subItem.value.map(item => item);
                } else {
                  acc[subKey] = subItem.value.value;
                }
                // acc[subKey] = subItem.value.value;
                return acc;
              } else {
                acc[subKey] = subItem.value;
                return acc;
              }
            }, {});
          } else {
            value = item;
          }
          // console.log(value)
          return { [key]: value };
        });
        console.log(entries);
        api.post(this.submitForm, entries).then((res) => {
          console.log(res.data);
          this.$emit("done");
          Notify.create({
            message: res.data.message,
            color: "green",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
        })
        .catch((error) => {
          console.log(error.response.data);
          Notify.create({
            message: error.response.data.message,
            color: "red",
            textColor: "white",
            position: "center",
            timeout: 3000,
          });
        });
      } catch (error) {
        console.error(error);
      }
    },

    async get_form() {
      // console.log(this.getForm); // login/create_user
      await api.get(this.getForm).then(async (results) => {
        console.log(results.data);
        this.formData = results.data.forms;
        this.options = results.data.options;
        // if ("login" in this.api_call || "register" in this.api_call) {
        //   add_verify_watcher("#verify_password");
        // }
      });
    },

    async add_password_watcher(id) {
      if ($(id)) {
        $(id).on("input", function () {
          // console.log('Input value changed to:', this.value.length);
          if (this.value.length >= 8) {
            $("#submit_btn").prop("disabled", false);
          } else {
            $("#submit_btn").prop("disabled", true);
          }
        });
        if ("verify_password" in id) {
          $(id).on("input", function () {
            if (this.value === $("#password").value) {
            }
          });
        }
      }
    },

    async get_csrf() {
      await APIService.get_csrf().then((results) => {
        console.log(results);
        this.csrf_token = results.data;
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
      });
    },
  },
  created() {
    this.get_form()
  },
  mounted() {
  },
});
</script>

<!-- Sample of incoming data that populates this.formData -->
<!-- Object { forms: {…}, options: (7) […] }
  forms: Object { "Basic Info": {…} }
    "Basic Info": Object { first_name: {…}, middle_name: {…}, last_name: {…}, … }
        email: Object { label: "E-Mail", type: "email", required: true, … }
        label: "E-Mail"
        required: true
        type: "email"
        value: ""
        <prototype>: Object { … }
      first_name: Object { label: "First Name", type: "input", required: true, … }
      last_name: Object { label: "Last Name", type: "input", required: true, … }
      middle_name: Object { label: "Middle Name", type: "input", required: false, … }
      nickname: Object { label: "Nickname", type: "input", required: false, … }
      phone_number: Object { label: "Phone Number", type: "tel", required: true, … }
      phone_type: Object { label: "Phone Type", type: "select", required: false, … }
      <prototype>: Object { … } -->