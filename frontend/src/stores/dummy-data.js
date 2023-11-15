import { defineStore } from 'pinia';
import dummyData from "../data/dummyData.json"


export const useDummyData = defineStore('dummy-data', {
  state: () => {
    return {
      dummyData,
    }
  },
  getters: {
    // doubleCount: (state) => state.counter * 2,
  },
  actions: {
    // increment() {
    //   this.counter++;
    // },
  },
});
