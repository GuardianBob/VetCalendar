import { defineStore } from 'pinia';
import formFields from "../components/formFields.json"


export const useFormFields = defineStore('form-fields', {
  state: () => {
    csrfToken: null
    return {
      formFields,
    }
  },
  getters: {
    // doubleCount: (state) => state.counter * 2,
    getCsrfToken: (state) => state.csrfToken,
  },
  actions: {
    setCsrfToken(token) {
      this.csrfToken = token;
    },

    // getCsrfToken() {
    //   return this.csrfToken;
    // },
    // increment() {
    //   this.counter++;
    // },
  },
});
