<template>
  <div class="row justify-center" >
    <div class="col-12 justify-right text-right" v-if="closeButton">
      <q-btn class="q-pt-md" color="primary" flat v-close-popup icon="close"/>
    </div>
    <div class="col-12 text-center">
      <h1 class="text-h3 text-primary">{{ page_title }}</h1>
    </div>
    <q-form >
      <!-- {{ formData.settings }} -->
        <div v-for="form in formData" :key="form.title">
          <div class="row justify-center">
          <!-- {{ form }} -->
          <div class="col-12 col-md-12 col-lg-12">
            <h4 class="text-h5 q-mt-md q-mb-none text-bold">{{ form.title }}</h4>
          </div>
          <!-- {{ form.fields }} -->
          <div v-for="(field, key) in form.fields" :key="key" :class="cols">
              <!-- {{ data.options }} -->
              <!-- {{ field.label }} -->
              <!-- {{ field }} -->
            <q-input 
              v-if="field.type === 'input' || field.type === 'text' || field.type === 'number' || field.type === 'url' || field.type === 'datetime-local' || field.type === 'search' || field.type === 'file' || field.type === 'month' || field.type === 'week' || field.type === 'range' || field.type === 'textarea'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
            />
            <q-input 
              v-else-if="field.type === 'email'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              outlined
              label-color="primary"
              :rules="field.required ? [rules.required, rules.email] : []"
            /> 
            <q-input 
              v-else-if="field.type === 'tel' || field.type === 'phone'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              mask="(###) ###-####"
              unmasked-value
              fill-mask
              outlined
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
            /> 
            <q-input 
            v-else-if="field.type === 'time'"
            v-model="field.value" 
            mask="time" 
            :label="field.label" 
            class="q-my-xs q-py-none" 
            :id="key"
            unmasked-value
            fill-mask
            outlined
            label-color="primary"
            :rules="field.required ? [rules.required] : []">
              <template v-slot:append>
                <q-icon name="access_time" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-time v-model="field.value">
                      <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-time>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input 
            v-else-if="field.type === 'color'"
            v-model="field.value" 
            :label="field.label" 
            class="q-my-xs q-py-none" 
            :id="key"
            unmasked-value
            fill-mask
            outlined
            label-color="primary"
            :rules="field.required ? [rules.required, rules.color] : []">
              <template v-slot:append>
                <q-icon name="colorize" class="cursor-pointer" color="primary">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-color no-header-tabs default-view="palette" v-model="field.value" />
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input 
              v-else-if="field.type === 'password'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="isPwd ? 'password' : 'text'"
              outlined
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
            > 
              <template v-slot:append>
                <q-icon :name="isPwd ? 'visibility_off' : 'visibility'" @click="isPwd = !isPwd" />
              </template>
            </q-input>
            <q-select
              v-else-if="field.type === 'select' && field.field_name === 'state'"
              v-model="field.value"
              :label="field.label"
              :id="key"
              :options="states.map((state) => ({label: Object.values(state)[0], value: Object.keys(state)[0]}))"
              class="q-my-xs q-py-none"
              outlined
              label-color="primary"
              map-options
              :rules="field.required ? [rules.required] : []"
            />            
            <q-select        
              v-else-if="field.type === 'select' && key == 'model'"        
              :options="form.options.filter(option => option.field === field.field).map(option => ({label: option.model, value: option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              map-options
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
              @update:modelValue="handleModelSelected"
            />
            <q-select        
              v-else-if="field.type === 'select' && key == 'table'"        
              :options="form.options.filter(option => option.field === field.field).map(option => ({label: option.model, value: option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              map-options
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
              @update:modelValue="handleTableSelected"
            />
            <div v-else-if="field.type === 'multi-select' && key == 'fields'">
              <span v-show="fieldChoices">
                <q-select        
                  :options="form.options.filter(option => option.field === field.field_name).map(option => ({label: option.related_model ? '(' + option.related_model + '): ' + option.label : option.label, value: option}))"
                  v-model="field.value"
                  :label="field.label"
                  :id="key"
                  class="q-my-xs q-py-none"
                  outlined
                  multiple
                  use-chips
                  map-options
                  label-color="primary"
                  :rules="field.required ? [rules.required] : []"
                  @update:modelValue="handleFieldSelected"
                >
                  <template v-if="field.value" v-slot:append>
                    <q-icon name="cancel" color="red" @click.stop.prevent="field.value = null" class="cursor-pointer" />
                  </template>
                </q-select>
              </span>
            </div>
            <div v-else-if="field.type === 'multi-select' && key == 'field_options'">
              <span v-show="field.value">
                <q-select        
                :options="form.options.filter(option => option.field === field.field_name).map(option => ({label: option.related_model ? '(' + option.related_model + '): ' + option.label : option.label, value: option}))"
                  v-model="fieldOptions"
                  :label="field.label"
                  :id="key"
                  class="q-my-xs q-py-none"
                  outlined
                  multiple
                  use-chips
                  map-options
                  label-color="primary"
                  :rules="field.required ? [rules.required] : []"
                  @update:modelValue="handleOptionSelected"
                >
                  <template v-if="fieldOptions" v-slot:append>
                    <q-icon name="cancel" color="red" @click.stop.prevent="fieldOptions = null" class="cursor-pointer" />
                  </template>
                </q-select>
              </span>
            </div>
            <q-select
              v-else-if="field.type === 'select'"
              :options="form.options.filter(option => option.field === field.field_name).map(option => ({label: option.label, value: option.option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              map-options
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
              @update:modelValue="handleOptionSelected"
            />
            <q-select
              v-else-if="field.type === 'multi-select'"
              :options="form.options.filter(option => option.field === field.field_name).map(option => ({label: option.related_model ? '(' + option.related_model + '): ' + option.label : option.label, value: option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              multiple
              use-chips
              map-options
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
            >
              <template v-if="field.value" v-slot:append>
                <q-icon name="cancel" color="red" @click.stop.prevent="field.value = null" class="cursor-pointer" />
              </template>
            </q-select>
            <q-input
              v-else-if="field.type === 'date'"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs q-py-none"
              outlined
              label-color="primary"
              :rules="field.required ? [rules.required] : []"
              >
              <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                  <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="field.value" mask="MMM-DD-YYYY" :multiple="multiDateSelect">
                      <div class="row items-center justify-end">
                        <q-btn label="Clear" color="negative" flat dense class="q-mr-sm" @click="field.value = null" /> 
                        <q-btn v-close-popup label="Close" color="primary" flat />
                      </div>
                    </q-date>
                  </q-popup-proxy>
                </q-icon>
              </template>
            </q-input>
            <q-input 
              v-else-if="field.type === 'locked'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              outlined
              disable
            /> 
            <q-select
              v-else-if="field.type == 'multi-text' && key == 'custom_options'"
              v-model="customOptions"
              :label="field.label"
              class="q-my-xs q-py-none"
              outlined
              use-input
              use-chips
              multiple
              input-debounce="0"
              @new-value="createValue"
              :options="field.value"
              map-options
              @update="createValue"
              :rules="field.required ? [rules.required] : []"
            >
              <template v-if="customOptions" v-slot:append>
                <q-icon name="cancel" color="red" @click.stop.prevent="customOptions = []" class="cursor-pointer" />
              </template>
            </q-select>
            <q-select
              v-else-if="field.type == 'multi-text'"
              v-model="field.value"
              :options="form.options.filter(option => option.field === field.field).map(option => ({label: option.label, value: option}))"
              :label="field.label"
              class="q-my-xs q-py-none"
              outlined
              use-input
              use-chips
              multiple
              input-debounce="0"
              map-options
              :rules="field.required ? [rules.required] : []"
            >
              <template v-if="customOptions" v-slot:append>
                <q-icon name="cancel" color="red" @click.stop.prevent="customOptions = []" class="cursor-pointer" />
              </template>
            </q-select>
            <span v-else></span>
          </div>
          </div>
        </div>
      <div class="row justify-around q-my-md">
        <q-btn @click="submit" color="primary" class="q-ma-sm">Save</q-btn>
        <q-btn v-show="cancel_button" id="cancel_btn" label="Cancel" class="bg-grey-8 text-white q-ma-sm" v-close-popup/>
        <q-btn v-show="delete_button" @click="confirm_delete" color="negative" class="q-ma-sm">Delete</q-btn>
      </div>
    </q-form>
    <q-dialog v-model="confirm" persistent>
      <ConfirmDialog 
        :doubleVerify="doubleVerify"
        @confirmed="confirm_choice"
      />
    </q-dialog>
  </div>
</template>

<script>
import { defineComponent, ref, onDeactivated } from "vue";
import { useQuasar, Notify } from "quasar";
import APIService from "../../services/api";
import ValidateService from "../../services/ValidateService";
import { api } from "boot/axios";
import statesJson from "components/states.json";
import ConfirmDialog from "components/ConfirmDialog.vue";

export default defineComponent({
  components: {
    ConfirmDialog,
  },
  props: [
    "page_title",
    "getForm",
    "submitForm",
    "item_id",
    "forms",
    'linked_forms',
    "form_data",
    "form_options",
    "closeButton",
    "editButton",
    "columns",
    'add_to_date',
    'delete_button',
    'cancel_button',
    'delete_api',
    'doubleVerify',
    "multiDateSelect",
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
      formData: ref(),
      loading: false,
      options: ref(),
      fetch_data: ref(),
      filteredTables: ref(),
      fieldChoices: ref(),
      selectedFields: ref(),
      fieldOptions: ref(),
      fieldOptionSettings: ref(),
      customOptions: ref(),
      customOptionSettings: ref(),
      filterOptions: ref(),
      showFields: ref(false),
      verifySubmit: ref(false),
      model: ref(),
      states: ref(statesJson.states),
      isPwd: ref(true),
      isRequired: ref(false),
      rules: ref(ValidateService.validators),
      requiredRule: val => !!val || 'This field is required',
      one: ref('col-12 col-sm-12 col-md-12 col-lg-12 q-px-sm f-field'),
      two: ref('col-10 col-sm-6 col-md-6 col-lg-6 q-px-sm f-field'),
      cols: ref(''),
      add_to_form_date: ref(),
      confirm: ref(false),
    };

    
  },

  watch: {
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
    add_to_date: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          console.log(newValue)
          this.add_to_form_date = newValue;
        }
      }
    },
  },

  computed: {
  
},

  methods: {
    isValidEmail(event) {
      console.log(event);
      const regex = /^[A-Za-z0-9+_.-]+@(.+)$/;
      return regex.test(event);
    },

    getField(form, fieldName) {
      return form.fields.find(field => field.field_name === fieldName);
    },

    add_date(date) {
      let form = Object.values(this.formData)[0];
      let field = this.getField(form, 'shift_date');
      if (field) {
        field.value = [date];
      }
    },

    confirm_delete() {
      this.confirm = true;
    },

    confirm_choice(choice) {
      this.confirm = false;
      console.log(choice);
      if (choice) {
        this.delete_item();
      }
    },

    createValue (val, done) {
      // Calling done(var) when new-value-mode is not set or "add", or done(var, "add") adds "var" content to the model
      // and it resets the input textbox to empty string
      // ----
      // Calling done(var) when new-value-mode is "add-unique", or done(var, "add-unique") adds "var" content to the model
      // only if is not already set
      // and it resets the input textbox to empty string
      // ----
      // Calling done(var) when new-value-mode is "toggle", or done(var, "toggle") toggles the model with "var" content
      // (adds to model if not already in the model, removes from model if already has it)
      // and it resets the input textbox to empty string
      // ----
      // If "var" content is undefined/null, then it doesn't tampers with the model
      // and only resets the input textbox to empty string

      if (val.length > 0) {
        console.log(val)
        if (!this.customOptions.includes(val)) {
          this.customOptions.push(val)
        }
        console.log(this.customOptions)
        done(val, 'add-unique')
      }
    },

    filterFn (val, update) {
      update(() => {
        if (val === '') {
          this.filterOptions.value = this.customOptions
        }
        else {
          const needle = val.toLowerCase()
          this.filterOptions.value = this.customOptions.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          )
        }
      })
    },

    handleTableSelected(event) {
      console.log(event.label, event.value);
      let data = {"app": event.value, "model": event.label}
      console.log(data)
      APIService.get_table_fields(event.value).then((res) => {
        console.log(res.data);
        this.fieldChoices, this.selectedFields = null;
        this.fieldChoices = res.data.fields;
      });
    },

    handleFieldSelected(event) {
      // console.log("field ===> ", event);
    },

    handleOptionSelected(event) {
      // console.log("Option ===> ", event);
    },

    delete_item() {
      console.log("Delete Event");
      // console.log(this.formData)
      let form = Object.values(this.formData)[0];
      // console.log(form.id)
      api.post(this.delete_api, {id: form.id}).then((res) => {
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
    },

    submit(event) {
      try {
        let submitData = JSON.parse(JSON.stringify(this.formData));
        console.log(submitData);
        this.verifySubmit = true;
        submitData.forEach((form) => {
          if (form.options) {
            delete form.options;
          }
          form.fields.forEach((field) => {
            if (field.required && field.value === "" || field.value === null || field.value === undefined) {
              event.preventDefault();
              this.verifySubmit = false;
              Notify.create({
                message: `${field.label} is required.`,
                color: "red",
                textColor: "white",
                position: "center",
                timeout: 3000,
              });
              return;
            }
          })
        })
        console.log(submitData)
        let body = {
          "forms": submitData,
          "save": true,
          'linked': this.linked_forms
        }
        if (this.verifySubmit) {
        api.post(this.submitForm, body).then((res) => {
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
      }
      } catch (error) {
        console.error(error);
      }
    },

    async get_form() {
      console.log(this.getForm); // login/create_user
      let body = {
        "forms": this.forms,
        "save": false,
        "id": this.item_id,
        'linked': this.linked_forms
      }
      await api.post(this.getForm, body).then(async (results) => {
        console.log(results.data);
        this.formData = results.data.forms;
        console.log(this.formData, this.model);
        if (this.add_to_form_date) {
          this.add_date(this.add_to_form_date)
        }
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

    // async get_csrf() {
    //   await APIService.get_csrf().then((results) => {
    //     console.log(results);
    //     this.csrf_token = results.data;
    //   });
    // },
  },
  created() {
    this.get_form()
  },
  mounted() {
  },
  
});
</script>