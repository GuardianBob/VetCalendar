import { defineStore } from 'pinia';
import APIService from "../../services/api"

export const useMainStore = defineStore('main-store', {
  state: () => {
    csrfToken: null
    return {
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

    getCookie(name) {
      var c = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
      return c ? c[2] : null;
    },

    get_csrf(){
      APIService.get_csrf().then((results) => {
        console.log(results)
        this.csrf_token = results.data['token'];
        let token_expire = new Date().setDate(new Date().getDate() + 10)
        let cookieString = 'csrftoken=' + this.csrf_token + '; expires = ' + token_expire + '; path=/';
        document.cookie = cookieString;
        // localStorage.setItem("csrf_token", this.csrf_token)
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
        document.cookie = 'csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        document.cookie = 'd_csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        console.log(this.csrf_token)
        console.log(document.cookie);
      } )
    },

    // getCsrfToken() {
    //   return this.csrfToken;
    // },
    // increment() {
    //   this.counter++;
    // },
  },
});
