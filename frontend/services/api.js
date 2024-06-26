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
        // console.log(error.config.url)
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
    // console.log("refreshing token")
    const refreshToken = localStorage.getItem('refresh_token');
    // console.log(refreshToken)
    if (refreshToken) {
      return api.post('/api/token/refresh/', { refresh: refreshToken });
    } else {
      return Promise.reject('Refresh token not available.');
    }
  }

  validateAccess(body) {
    this.setTokenHeader();
    return api.post('/login/validate', body);
  }

  logout() {
    // Clear tokens from localStorage and reload page to logout
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');  
    localStorage.removeItem('user');  
    window.location.replace('/'); 
    return 
  }

  // get_form() {
  //   return api.get('/login/');
  // }

  // create_user(data) {
  //   this.setTokenHeader();
  //   if (!data) {
  //     return api.get('/login/create_user');
  //   } else {
  //     return api.post('/login/create_user', data);
  //   }
  // }

  // admin_settings(data) {
  //   this.setTokenHeader();
  //   if (!data) {
  //     return api.get('/login/admin_settings');
  //   } else {
  //     return api.post('/login/admin_settings', data);
  //   }
  // }

  // get_login_csrf() {
  //   return api.get('/login/get_csrf');
  // }

  // get_csrf() {
  //   return api.get('/get_csrf');
  // }

  login(data) {
    return api.post("/login/", data)
  }

  get_api_keys(keys) {
    this.setTokenHeader();
    return api.post('/get_keys', {"data": keys});
  }

  upload_file(formData) {
    const token = localStorage.getItem('access_token');
    console.log("uploading", formData);
    // return api.post("/upload_file", { file })
    let upload_url = ''
    if (process.env.LOCAL_DEV_ENV == "true") {
      upload_url = `http://${process.env.REST_API_HOST}:${process.env.REST_API_PORT}/upload_file`
    } else if (process.env.LOCAL_DEV_ENV == "false" && process.env.TEST_ENV == "true") {
      upload_url = `https://${process.env.REST_API_TEST}/upload_file`
    } else {
      upload_url = `https://${process.env.REST_API_LIVE}/upload_file`
    }
    // upload_url = `https://${process.env.REST_API_LIVE}/upload_file`
    // console.log("url", upload_url);
    return axios({
      method: "post",
      url: upload_url,
      data: formData,
      headers: { 
        "Content-Type": "multipart/form-data",
        'Authorization': `Bearer ${token}` 
      },
    })
  }

  // return_shifts_old(date) {
  //   return api.post('/return_shifts_old', {date})
  // }

  return_shifts(date) {
    this.setTokenHeader();
    return api.post('/return_shifts', {date})
  }

  // save_schedule_updates(data) {
  //   this.setTokenHeader();
  //   return api.post('/save_schedule_updates', data)
  // }

  // This saves events that are dragged and dropped
  edit_event(data = null, update=false) {
    this.setTokenHeader();
    if (update) {
      return api.post('/edit_event', data)
    } else {
      return api.get(`/edit_event/${data}`)
    }
  }

  delete_event(data) {
    this.setTokenHeader();
    return api.post('/delete_event', data)
  }

  clear_shifts(data) {
    this.setTokenHeader();
    return api.post('/clear_shifts', data)
  }

  // schedule_settings(data) {
  //   this.setTokenHeader();
  //   if (!data) {
  //     return api.get('/schedule_settings');
  //   } else {
  //     return api.post('/schedule_settings', data);
  //   }
  // }

  get_model_form(model) {
    this.setTokenHeader();
    return api.get(`/get_model_form/${model}`);
  }

  // test_calendar() {
  //   return api.post('/calendar/test');
  // }

  // test_event() {
  //   return api.post('/calendar/test_event');
  // }

  // get_user_list(formData) {
  //   let upload_url = ''
  //   if (process.env.LOCAL_DEV_ENV == "true") {
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

  // add_edit_form(data) {
  //   this.setTokenHeader();
  //   if (!data) {
  //     return api.get('/add_edit_form');
  //   }
  //   return api.post('/add_edit_form', data)
  // }

  get_table_fields(data) {
    this.setTokenHeader();
    return api.post('/get_table_fields', data)
  }

  // get_field_options(data) {
  //   this.setTokenHeader();
  //   return api.post('/get_field_options', data)
  // }

  // get_formbuilder_form(form) {
  //   return api.get(`/get_formbuilder_form/${form}`)
  // }

  // submit_formbuilder_form(data) {
  //   return api.post(`/get_formbuilder_form/${data}`)
  // }

  // add_json_form(data) {
  //   this.setTokenHeader();
  //   return api.post('/add_json_form', data)
  // }

  get_user_list() {
    this.setTokenHeader();
    return api.get('/login/get_user_list');
  }

  get_user_profile(email) {
    this.setTokenHeader();
    return api.post('/login/get_user_profile', email);
  }

  // get_user_profile_admin(id) {
  //   this.setTokenHeader();
  //   return api.post('/login/get_user_profile_admin', id);
  // }

  // add_user(data) {
  //   this.setTokenHeader();
  //   // console.log(JSON.stringify(data))
  //   return api.post('/login/add_user', data)
  // }

  delete_user(data) {
    this.setTokenHeader();
    // console.log(JSON.stringify(data))
    return api.post('/login/delete_user', data)
  }

  // get_user_profile(id) {
  //   this.setTokenHeader();
  //   return api.get(`/login/user_profile/${id}`)
  // }

  update_profile(data) {
    this.setTokenHeader();
    return api.post('/login/update_profile', data)
  }

  update_password(data) {
    this.setTokenHeader();
    return api.post('/login/update_password', data)
  }

  reset_password(data) {
    this.setTokenHeader();
    return api.post('/login/reset_password', data)
  }

  
}

export default new APIService();