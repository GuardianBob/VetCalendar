import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
let HTTP = ''
if (process.env.DEV_ENV == "true") {
  HTTP = `http://${process.env.REST_API_HOST}:${process.env.REST_API_PORT}`
} else {
  HTTP = `https://${process.env.REST_API_LIVE}`
}
let access_control = ''
if (process.env.DEV_ENV == "true") {
  access_control = `http://localhost:9000, http://127.0.0.1:8000*`
} else {
  access_control = `https://vet-cal-dev.jmeyer-dev.com`
}
const api = axios.create({
  // baseURL: 'https://api.example.com'
  // withCredentials: false,
  baseURL: HTTP,
  // baseURL: 'https://vet-cal.jmeyer-dev.com/backend',
  // headers: {
    // "Content-Type": "application/json; charset=utf-8",
    // "Access-Control-Allow-Origin": access_control,
  // },
})

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
})

export { api }
