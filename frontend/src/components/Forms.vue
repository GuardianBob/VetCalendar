<template>
  <!-- <q-page class="q-pt-xl"> -->
      <div class="row align-start justify-center q-mx-sm">
        <div class="column">
          <q-form>
            <div v-for="(field, key) in formData" :key="key" class="col-4 col-md-6 q-px-md q-mx-md">
              <q-input 
                v-if="field.type === 'input' || field.type === 'email' || field.type === 'number' || field.type === 'tel' || field.type === 'url' || field.type === 'time' || field.type === 'date' || field.type === 'datetime-local' || field.type === 'search' || field.type === 'color' || field.type === 'file' || field.type === 'month' || field.type === 'week' || field.type === 'range' || field.type === 'textarea'"
                v-model="field.value" 
                :label="field.label" 
                dense 
                class="q-my-sm" 
                :id="key"
                :type="field.type"
              />
              <q-input 
                v-else-if="field.type === 'password'"
                v-model="field.value" 
                :label="field.label" 
                dense 
                class="q-my-sm" 
                :id="key"
                :type="isPwd ? 'password' : 'text'"
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
                dense
                class="q-my-sm"
              />
              <q-select
                v-else-if="field.type === 'select'"
                :options="options.filter(option => option.field === key).map(option => ({label: option.label, value: option.option}))"
                v-model="field.value"
                :label="field.label"
                :id="key"
                dense
                class="q-my-sm"
              />
            </div>
            <q-btn @click="submit">Submit</q-btn>
          </q-form>
        </div>
      </div>
      <!-- <br> -->
      <!-- <q-spinner v-show="loading" color="primary" size="3em" :thickness="3" /> -->
    <!-- <div class="row align-start justify-center">
    </div> -->
  <!-- </q-page> -->
</template>


<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import MainFunctions from '../../services/MainFunctions'
import { api } from "boot/axios";
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

        // RETURNS KEY VALUE PAIRS AND ACCOUNTS FOR NESTED OBJECTS
        const entries = Object.entries(this.formData).map(([key, item]) => {
          let value;
          if (typeof item.value === 'object' && item.value !== null) {
            value = item.value.value;
          } else {
            value = item.value;
          }
          return { key, value };
        });
        console.log(entries);
      } catch (error) {
        console.error(error);
      }
    },
  },

  created() {
    
  },
  
  mounted() {
    APIService.get_test_form().then((response) => {
      console.log(response.data)
      this.formData = response.data.data
      this.options = response.data.options
    });
    // console.log(this.states)
    // this.formData = {
    //   login: {
    //     label: "Login",
    //     type: "email",
    //     value: "",
    //   },
    //   password: {
    //     label: "Password",
    //     type: "password",
    //     value: "",
    //   },
    // }
    // console.log(this.form_data, this.form_options)
    // this.formData = this.form_data
    // this.options = this.form_options
  },

})
</script>
