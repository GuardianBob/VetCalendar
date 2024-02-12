<template>
  <div class="dialog-60 q-ma-sm" ref="form">
    <div class="text-right">
      <q-btn class="q-pt-md" color="primary" flat v-close-popup icon="close"/>
    </div>
    <div class="row justify-center">
      <h1 class="text-h3 text-primary" >Update User</h1>
    </div>
    <q-form @submit="submit" method="POST" id="edit_user">
      <div v-for="(data, title) in formData" :key="title" class="">
        <div class="row justify-center">
          <div class="col-10 col-md-12 col-lg-12">
            <h4 class="text-h5 q-mt-md q-mb-none text-bold">{{ title }}</h4>
          </div>
          <div v-for="(field, key) in data" :key="key" class="col-10 col-sm-6 col-md-6 col-lg-6 q-px-sm f-field">
            <q-input 
              v-if="title === 'Address' && field.type != 'select' && key != 'apt_num' && key != 'street2'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
              :rules="[isRequired ? requiredRule : '']"
            />
            <q-input 
              v-else-if="title === 'Address' && field.label === 'Zip Code'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs q-py-none" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
              mask="#####"
              fill-mask
              hint="Must be a 5-digit whole number"
              :rules="[val => (/^\d{5}$/).test(val) || 'Invalid zipcode']"
              maxlength="5"
              />        
            <q-input 
              v-else-if="field.type === 'input' || field.type === 'email' || field.type === 'number' || field.type === 'url' || field.type === 'time' || field.type === 'date' || field.type === 'datetime-local' || field.type === 'search' || field.type === 'color' || field.type === 'file' || field.type === 'month' || field.type === 'week' || field.type === 'range' || field.type === 'textarea'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs" 
              :id="key"
              :type="field.type"
              outlined
              label-color="primary"
            />
            <q-input 
              v-else-if="field.type === 'tel'"
              v-model="field.value" 
              :label="field.label" 
              class="q-my-xs" 
              :id="key"
              mask="(###) ###-####"
              fill-mask
              outlined
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
              map-options
              :rules="[isRequired ? requiredRule : '']"
            />
            <q-select
              v-else-if="field.type === 'select'"
              :options="options.filter(option => option.field === key).map(option => ({label: option.label, value: option.option}))"
              v-model="field.value"
              :label="field.label"
              :id="key"
              class="q-my-xs"
              outlined
              map-options
            />
          </div>
        </div>
      </div>
      <div class="row justify-center q-my-md">
        <q-btn id="submit_btn" label="Submit" class="q-ma-sm" type="submit" color="primary"/>
        <q-btn id="delete_btn" label="Delete" class="q-ma-sm" color="negative" @click="confirm = true"/>
        <q-btn id="cancel_btn" label="Cancel" class="bg-grey-8 text-white q-ma-sm" v-close-popup/>
      </div>
    </q-form>
    <q-dialog v-model="confirm" persistent>
        <q-card>
          <q-card-section class="row items-center">
            <q-avatar icon="report" color="negative" text-color="white" />
            <span class="q-ml-sm">Are you sure you want to delete this user?</span>
          </q-card-section>
          <q-card-section>
            <q-toggle
              v-model="verify_delete"
              checked-icon="check"
              color="red"
              label="Click to confirm you want to delete this user."
              unchecked-icon="clear"
            />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="Cancel" color="primary" v-close-popup @click="verify_delete = false"/>
            <q-btn flat label="Delete" color="negative" @click="delete_user" />
          </q-card-actions>
        </q-card>
      </q-dialog> 
  </div>
</template>


<script>
import { defineComponent, ref } from 'vue'
import { useQuasar, Notify } from "quasar"
import APIService from "../../services/api"
import statesJson from "components/states.json";

export default defineComponent({
  name: "FormsPage",
  props: [
    "form_data",
    "form_options",
    "user_id",
  ],
  components: {
  },
  data() {
    return {
      formData: ref({}),
      options: ref({}),
      states: ref(statesJson.states),
      isPwd: ref(true),
      confirm: ref(false),
      verify_delete: ref(false),
      isRequired: ref(false),
      requiredRule: value => !!value || 'This field is required'
    }
  },
  setup() {
    
    return {
    };
  },
  watch: {
    'formData.Address': {
      handler(newValue, oldValue) {
        // This function will be called when `formData.Address.address` changes.
        // console.log('Address changed from', oldValue, 'to', newValue.street);
        // console.log(this.formData.Address.street.value.length)
        if (this.formData.Address.street.value.length > 0 || this.formData.Address.city.value.length > 0 || this.formData.Address.state.value.length > 0 || this.formData.Address.zipcode.value.length > 0) {
          // console.log("===========> checking filled", newValue)
          this.isRequired = true;
        } else {
          this.isRequired = false;
        }
        // You can add your logic here.
        // Iterate over the properties of newValue
        // for (const [key, value] of Object.entries(newValue)) {
        //   console.log(`Key: ${key}, Value: ${value}`);
        // }
      },
      deep: true
    }
  },

  computed: {
  },
  methods: {
    isFieldFilled() {
      let filled = false;
      // console.log("checking filled", this.formData.Address)
      for (const entry of Object.entries(this.formData.Address)) {
        // console.log(`Key: ${key}, Value: ${value}`);
        for (const [key, value] of Object.entries(entry)) {
          // console.log(`Key: ${key}, Value: ${value}`);
          if (value.length > 0) {
            filled = true;
            // console.log("===========> Switched to filled", entry)
            return filled;
          }
        }
        // console.log("=======>> ", filled)
        // return filled = true ? value.value > 0 : false;
      }
      return filled;
    },

    async get_form() {
      try {
        APIService.get_user_profile(this.user_id).then((response) => {
          console.log(response.data)
          this.formData = response.data.forms
          this.options = response.data.options
        }); 
      } catch (error) {
        console.error(error);
      }
    },

    generateId(key) {
      return `input-${key}`;
    },

    async submit() {
      try {
        console.log(this.formData)
        this.isFieldFilled()
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
        APIService.update_user_profile(entries).then((res) => {
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
            message: error.response.data.error,
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

    async delete_user() {
      // console.log(this.user_id);
      if (this.verify_delete == false) {
        Notify.create({
          message: "Please confirm you want to delete this user",
          color: "red",
          textColor: "white",
          position: "center",
          timeout: 3000,
          actions: [
            { icon: 'close', color: 'white', round: true, handler: () => { /* ... */ } }
          ]
        });
        return
      }
      APIService.delete_user(this.user_id).then((results) => {
        console.log(results);
        // this.parentFunc02();
        this.$emit("user-updated");
        Notify.create({
          message: results.data.message,
          color: "green",
          textColor: "white",
          position: "center",
          timeout: 3000,
        });
        this.confirm = false;
        this.$emit('close-dialog')
      });
    },
  },

  created() {
    
  },
  
  mounted() {
    this.get_form()
  },

})
</script>
