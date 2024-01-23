<template>
  <div class="c-dialog q-ma-sm">
    <div class="row justify-center">
      <h1 class="text-h3 text-primary" >Update User</h1>
    </div>
    <q-form>
      <div v-for="(data, title) in formData" :key="title" class="">
        <div class="row justify-center">
          <div class="col-10 col-md-12 col-lg-12">
            <h4 class="text-h5 q-mt-md q-mb-none text-bold">{{ title }}</h4>
          </div>
          <div v-for="(field, key) in data" :key="key" class="col-10 col-sm-6 col-md-6 col-lg-6 q-px-sm f-field">
            <q-input 
              v-if="field.type === 'input' || field.type === 'email' || field.type === 'number' || field.type === 'tel' || field.type === 'url' || field.type === 'time' || field.type === 'date' || field.type === 'datetime-local' || field.type === 'search' || field.type === 'color' || field.type === 'file' || field.type === 'month' || field.type === 'week' || field.type === 'range' || field.type === 'textarea'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
            />
            <q-input 
              v-else-if="field.type === 'password'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs" 
              :id="key"
              :type="isPwd ? 'password' : 'text'"
              outlined
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
              class="q-my-xs"
              outlined
            />
            <q-select
              v-else-if="field.type === 'select'"
              :options="options.filter(option => option.field === key).map(option => ({label: option.label, value: option.option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs"
              outlined
            />
          </div>
        </div>
      </div>
      <div class="row justify-around q-my-md">
        <q-btn @click="submit" color="primary">Submit</q-btn>
      </div>
    </q-form>
  </div>
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import statesJson from "components/states.json";

export default defineComponent({
  name: "FormsPage",
  props: [
    "form_data",
    "form_options",
  ],
  components: {
  },
  data() {
    return {
      formData: ref({}),
      options: ref({}),
      states: ref(statesJson.states),
      isPwd: ref(true),
    }
  },
  setup() {
    
    return {
    };
  },
  watch: {
    
  },
  computed: {
    
  },
  methods: {
    async submit() {
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
            console.log("===> ", value)
            value = Object.entries(item).reduce((acc, [subKey, subItem]) => {
              if (typeof subItem.value === 'object' && subItem !== null) {
                console.log(subItem.value)
                acc[subKey] = subItem.value.value;
                return acc;
              } else {
                acc[subKey] = subItem.value;
                return acc;
              }
            }, {});
          } else {
            value = item;
          }
          console.log(value)
          return { [key]: value };
        });
        console.log(entries);
        APIService.submit_test_form(entries)
      } catch (error) {
        console.error(error);
      }
    },
  },

  created() {
    
  },
  
  mounted() {
    APIService.get_test_form(3).then((response) => {
      console.log(response.data)
      this.formData = response.data.forms
      this.options = response.data.options
    }); 
    // this.formData = {
    //   "Login": {
    //     "email": {
    //       "label": "E-Mail",
    //       "type": "input",
    //       "value": "test"
    //     },
    //     "password": {
    //       "label": "Password",
    //       "type": "password",
    //       "value": ""
    //     }
    //   },
    // }   
  },

})
</script>
