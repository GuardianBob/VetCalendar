import { api } from "boot/axios";
import axios from 'axios';
import { useMainStore } from "stores/main-store.js";



class APIService {
  setTokenHeader() {
    const mainStore = useMainStore();
    let cookie = mainStore.getCookie('d_csrfToken')
    // if (cookie) {
    console.log('cookie: ' + cookie)
    api.defaults.headers["X-CSRF-TOKEN"] = cookie;
      // api.defaults.headers['Access-Control-Allow-Credentials'] = true
      // api.defaults.headers["Content-Type"] = 'application/json'; 
    // }
  }

  get_todo() {
    console.log("at api")
    return api.get('/api/todos/');
  }

  get_form() {
    return api.get('/login/');
  }

  get_login_csrf() {
    return api.get('/login/get_csrf');
  }

  get_csrf() {
    return api.get('/get_csrf');
  }

  login(data) {
    console.log(data, data.csrfmiddlewaretoken)    
    // document.cookie = 'csrftoken=' + data.csrfmiddlewaretoken + ';path=/;samesite=strict;secure=false';
    // this.$q.cookies.set('csrftoken', data.csrfmiddlewaretoken, {
    //   path: '/',
    //   sameSite: 'strict',
    //   secure: false
    // });
    // const headers = { 'X-CSRF-TOKEN': data.csrfmiddlewaretoken }
    // return api.post("/login/validate", { data: data.data }, {headers: headers} );
    return api.post("/login/", data);
    // return api({
    //   method: "get",
    //   url: "/login/validate",
    //   data: data.data,
    //   headers: { "Content-Type": "multipart/form-data", 'X-CSRF-TOKEN': data.token },
    // })
  }

  upload_file(formData) {
    console.log("uploading", formData);
    // return api.post("/upload_file", { file })
    let upload_url = ''
    if (process.env.DEV_ENV == "true") {
      upload_url = `http://${process.env.REST_API_HOST}:${process.env.REST_API_PORT}/upload_file`
    } else {
      upload_url = `https://${process.env.REST_API_LIVE}/upload_file`
    }
    // upload_url = `https://${process.env.REST_API_LIVE}/upload_file`
    console.log("url", upload_url);
    return axios({
      method: "post",
      url: upload_url,
      data: formData,
      headers: { "Content-Type": "multipart/form-data" },
    })
  }

  return_shifts(date) {
    return api.post('/return_shifts', {date})
  }

  test_calendar() {
    return api.post('/calendar/test');
  }

  test_event() {
    return api.post('/calendar/test_event');
  }

  // get_user_list(formData) {
  //   let upload_url = ''
  //   if (process.env.DEV_ENV == "true") {
  //     upload_url = `http://${process.env.REST_API_HOST}:${process.env.REST_API_PORT}/return_user_list`
  //   } else {
  //     upload_url = `https://${process.env.REST_API_LIVE}/return_user_list`
  //   }
  //   // upload_url = `https://${process.env.REST_API_LIVE}/return_user_list`
  //   console.log("url", upload_url);
  //   return axios({
  //     method: "post",
  //     url: upload_url,
  //     data: formData,
  //     headers: { "Content-Type": "multipart/form-data" },
  //   })
  // }

  get_user_list() {
    // this.setTokenHeader();
    // const mainStore = useMainStore();
    // let new_api = api
    // let csrfToken = mainStore.getCookie('csrftoken')
    // if (cookie) {
    // console.log('csrfToken: ' + csrfToken)
    // new_api.defaults.xsrfHeaderName = 'x-csrftoken'
    // new_api.defaults.xsrfCookieName = 'csrftoken'
    // new_api.defaults.withCredentials = true
    // new_api.setRequestHeader("X-CSRFToken", csrfToken);
    // new_api.defaults.headers.common["HTTP_X_CSRFTOKEN"] = csrfToken;
    // console.log(new_api.defaults)
    return api.post('/login/get_user_list');
  }

  get_user_profile(id) {
    return api.post('/login/get_user_profile', id);
  }

  // get_user_data() {
  //   return api.post('/get_user_profiles');
  // }

  add_user(data) {
    console.log(JSON.stringify(data))
    return api.post('/login/add_user', data)
  }
}

export default new APIService();