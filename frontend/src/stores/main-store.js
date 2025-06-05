import { defineStore } from 'pinia';
import APIService from "../../services/api"
import { useLocalStorage } from "@vueuse/core"

export const useMainStore = defineStore('main-store', {
  state: () => {
    const user = useLocalStorage('user', null);
    const local_dev = process.env.LOCAL_DEV_ENV === "true"
    
    return {
      refreshToken: null,
      accessToken: null,
      csrfToken: null,
      loggedIn: false,
      permissions: [],
      access: [],
      user,
      local_dev, // set to true if running on local dev environment
      // local_dev: false,
      testing: local_dev, // set to true if running on local dev environment

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
      useLocalStorage('user', user);
    },

    setToken(data) {
      this.refreshToken = data.refreshToken
      this.accessToken = data.accessToken
    },

    setTesting(value) {
      this.testing = value
    },

    setPermissions(access, permissions) {
      this.testing && console.log('permissions \n', permissions)
      this.access = access
      this.permissions = permissions
    },

    log(...args) {
      if (this.local_dev) {
        console.trace(...args)
      }
    },

    async updatePermissions() {
      try {
        this.testing && console.log("env setting: ", process.env.LOCAL_DEV_ENV)
        this.testing && console.log("Updating Permissions...")
        const response = await APIService.validateAccess();
        this.testing && console.log("permissions response : ", response.data)
        this.access = response.data.access
        this.permissions = response.data.permissions
      } catch (error) {
        this.testing && console.log(error)
      }
      this.testing && console.log('permissions \n', this.permissions)
      return [this.access, this.permissions]
    },

    checkAccess(accessLevel = null) {
      this.testing && console.log('checking access \n', accessLevel, this.access)
      if (Array.isArray(accessLevel)) {
        for (let i = 0; i < accessLevel.length; i++) {
          if (this.access.includes(accessLevel[i]) || this.access.includes("Admin")) {
            this.testing && console.log('access granted')
            return true
          }
        }
      } else if (this.access.includes(accessLevel) || this.access.includes("Admin")) {
        this.testing && console.log('access granted')
        return true
      } else {
        this.testing && console.log('access denied')
        return false
      }
    },

    checkPermissions(permission = null) {
      this.testing && console.log('checking permissions', this.permissions.length)
      if (Array.isArray(permission)) {
        for (let i = 0; i < permission.length; i++) {
          if (this.permissions.includes(permission[i]) || this.access.includes("Admin")) {
            this.testing && console.log('Permission allowed')
            return true
          }
        }
      } else if (this.permissions.includes(permission) || this.access.includes("Admin")) {
        this.testing && console.log('Permission allowed')
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
      this.testing && console.log( 
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
        this.testing && console.log(results)
        this.csrf_token = results.data['token'];
        let token_expire = new Date().setDate(new Date().getDate() + 10)
        let cookieString = 'csrftoken=' + this.csrf_token + '; expires = ' + token_expire + '; path=/';
        document.cookie = cookieString;
        // localStorage.setItem("csrf_token", this.csrf_token)
        // document.head.querySelector('meta[name="csrf-token"]');
        // window.axios.defaults.headers.common['X-CSRF-TOKEN'] = results.data
        document.cookie = 'csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        document.cookie = 'd_csrfToken =; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
        this.testing && console.log(this.csrf_token)
        this.testing && console.log(document.cookie)
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
