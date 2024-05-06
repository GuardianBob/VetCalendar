import { defineStore } from 'pinia';
import APIService from "../../services/api"
import { useLocalStorage } from "@vueuse/core"

export const useMainStore = defineStore('main-store', {
  state: () => {
    const user = useLocalStorage('user', null);
    
    return {
      refreshToken: null,
      accessToken: null,
      csrfToken: null,
      loggedIn: false,
      permissions: [],
      access: [],
      user,
      // return {
      //   loggedIn,
      // }
    }
  },
  getters: {
    // doubleCount: (state) => state.counter * 2,
    getCsrfToken: (state) => state.csrfToken,
  },
  actions: {
    setLoggedIn(value) {
      this.loggedIn = value
    },

    setUser(user) {
      this.user = user
    },

    setToken(data) {
      this.refreshToken = data.refreshToken
      this.accessToken = data.accessToken
    },

    setPermissions(access, permissions) {
      console.log('permissions \n', permissions)
      this.access = access
      this.permissions = permissions
    },

    async updatePermissions() {
      try {
        console.log("Updating Permissions...")
        const response = await APIService.validateAccess();
        console.log("permissions response : ",response.data)
        this.access = response.data.access
        this.permissions = response.data.permissions
      } catch (error) {
        console.log(error)
      }
      console.log('permissions \n', this.permissions)
      return [this.access, this.permissions]
    },

    checkAccess(accessLevel = null) {
      console.log('checking access \n', accessLevel, this.access)
      if (Array.isArray(accessLevel)) {
        for (let i = 0; i < accessLevel.length; i++) {
          if (this.access.includes(accessLevel[i]) || this.access.includes("Admin")) {
            console.log('access granted')
            return true
          }
        }
      } else if (this.access.includes(accessLevel) || this.access.includes("Admin")) {
        console.log('access granted')
        return true
      } else {
        console.log('access denied')
        return false
      }
    },

    checkPermissions(permission = null) {
      console.log('checking permissions', this.permissions.length)
      if (Array.isArray(permission)) {
        for (let i = 0; i < permission.length; i++) {
          if (this.permissions.includes(permission[i]) || this.access.includes("Admin")) {
            console.log('Permission allowed')
            return true
          }
        }
      } else if (this.permissions.includes(permission) || this.access.includes("Admin")) {
        console.log('Permission allowed')
        return true
      } else {
        return false
      }
    },

    logout() {
      this.refreshToken = null
      this.accessToken = null
      this.csrfToken = null
      this.loggedIn = false
      this.permissions = []
      this.access = []
      this.user = null
    },

    status() {
      console.log(
        this.refreshToken,
        this.accessToken,
        this.csrfToken,
        this.loggedIn,
        this.permissions,
        this.access,
        this.user
      )
    },

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
