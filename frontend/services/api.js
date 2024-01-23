import { api } from "boot/axios";
import axios from 'axios';
// import { useMainStore } from "stores/main-store.js";


class APIService {  
  constructor() {    
    // Add a response interceptor
    api.interceptors.response.use(undefined, error => {
      // console.log(error)
      if (error.config && error.response && error.response.status === 401) {
        // If the request is for token refresh, reject the promise
        console.log(error.config.url)
        if (error.config.url === '/api/token/refresh/') {
          this.logout();
          return Promise.reject(error);
        }
        // Token expired, try to refresh it
        return this.refreshToken().then(response => {
          // Save new tokens in localStorage
          // console.log(`New access token: ${JSON.stringify(response.data, null, 2)}`)
          localStorage.setItem('access_token', response.data.access);

          // Retry the original request
          const config = error.config;
          config.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;

          return api(config);
        }).catch(error => {
          console.log(error);
          // Refresh failed - logout the user
          // this.logout();
          return Promise.reject(error);
        });
      }

      return Promise.reject(error);
    });
  }

  setTokenHeader() {
    const token = localStorage.getItem('access_token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // console.log(token)
    } 
  }

  refreshToken() {
    console.log("refreshing token")
    const refreshToken = localStorage.getItem('refresh_token');
    // console.log(refreshToken)
    if (refreshToken) {
      return api.post('/api/token/refresh/', { refresh: refreshToken });
    } else {
      return Promise.reject('Refresh token not available.');
    }
  }

  logout() {
    // Clear tokens from localStorage and reload page to logout
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');  
    window.location.replace('/login'); 
    return 
  }

  get_todo() {
    console.log("at api")
    return api.get('/api/todos/');
  }

  get_form() {
    return api.get('/login/');
  }

  create_user(data) {
    if (!data) {
      return api.get('/login/create_user');
    } else {
      return api.post('/login/create_user', data);
    }
  }

  get_login_csrf() {
    return api.get('/login/get_csrf');
  }

  get_csrf() {
    return api.get('/get_csrf');
  }

  login(data) {
    console.log(data)    
    // document.cookie = 'csrftoken=' + data.csrfmiddlewaretoken + ';path=/;samesite=strict;secure=false';
    // this.$q.cookies.set('csrftoken', data.csrfmiddlewaretoken, {
    //   path: '/',
    //   sameSite: 'strict',
    //   secure: false
    // });
    // const headers = { 'X-CSRF-TOKEN': data.csrfmiddlewaretoken }
    // return api.post("/login/validate", { data: data.data }, {headers: headers} );
    if (!data) {
      return api.get("/login/")
    } else {
      api.post("/login/", data).then((response) => {
        console.log(response)
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        return response
      })
      .catch(error => {
        console.log(error);
        return error
      });
    }
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
    this.setTokenHeader();
    return api.get('/login/get_user_list');
  }

  get_user_profile_old(req) {
    this.setTokenHeader();
    return api.post('/login/get_user_profile', req);
  }

  get_user_profile_admin(id) {
    return api.post('/login/get_user_profile_admin', id);
  }

  add_user(data) {
    console.log(JSON.stringify(data))
    return api.post('/login/add_user', data)
  }

  delete_user(data) {
    // console.log(JSON.stringify(data))
    return api.post('/login/delete_user', data)
  }

  get_user_profile(id) {
    return api.get(`/login/get_user_profile/${id}`)
  }

  get_test_form(id) {
    return api.get(`/login/get_user_profile/${id}`)
  }

  submit_test_form(data) {
    return api.post('/login/submit_test_form', data)
  }

  
}

export default new APIService()