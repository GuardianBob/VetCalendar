import { defineStore } from 'pinia';
import dummyData from "../data/dummyData.json"


export const useDummyData = defineStore('dummy-data', {
  state: () => {
    csrfToken: null
    return {
      dummyData,
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
