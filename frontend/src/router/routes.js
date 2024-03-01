import APIService from "../../services/api.js";

function requireAuth(to, from, next) {
  // const token = localStorage.getItem('access_token');
  // APIService.validateToken(token).then((response) => {
  //   console.log(response.data)
  //   next();
  // }).catch((error) => {
  //   console.log(error)
  //   next('/login');
  // })
  // Check if the route requires authentication
  // if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if no token is stored in localStorage
    if (!localStorage.getItem('access_token')) {
      // Redirect to the login page
      next({ name: 'login' });
    } else {
      // Proceed to the route
      next();
    }
  // } else {
  //   // If the route doesn't require authentication, proceed
  //   next();
  // }
}

const routes = [
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      // ============================= MAIN USER PAGES =============================
      {
        path: "",
        component: () => import("pages/IndexPageNew.vue"),
        alias: ["/:year*", "/:year*/:month*", "/:year*/:month*/:user*"],
      },
      
      {
        path: "/login",
        name: "login",
        component: () => import("pages/LoginPage.vue"),
      },
      {
        path: "/register",
        // name: "register",
        // component: () => import("pages/RegisterPage.vue"),
        component: () => import("pages/FormsPage.vue"),
        // beforeEnter: requireAuth,
        props: { 
          page_title: 'Request Access',
          get_form_api: '/login/request_access',
          save_form_api: '/login/request_access',
        }
      },
      // ============================= LOGGED IN USER PAGES =============================
      {
        path: "/profile",
        name: "profile",
        component: () => import("pages/ProfilePage.vue"),
        beforeEnter: requireAuth,
      },
      // ============================= ADMIN USER PAGES =============================
      {
        path: "/users",
        name: "users",
        component: () => import("pages/Users.vue"),
        beforeEnter: requireAuth,
      },
      {
        path: "/manage_schedule",
        name: "manage_schedule",
        component: () => import("pages/ManageSchedule.vue"),
        beforeEnter: requireAuth,
      },
      {
        path: "/schedule_import",
        // redirect: "/",
        component: () => import("pages/UploadSchedule.vue"),
        alias: [
          "/schedule_import/:year*",
          "/schedule_import/:year*/:month*",
          "/schedule_import/:year*/:month*/:user*",
        ],
      },
      {
        path: "/schedule_settings",
        name: "schedule settings",
        component: () => import("pages/SettingsPage.vue"),
        beforeEnter: requireAuth,
        props: { 
          api_route: '/schedule_settings',
          page_title: 'Schedule Settings',
          forms_input: [
            { model: 'ShiftName', form: 'add_shift_info'}, 
            { model: 'ShiftType', form: 'add_shift_type' },
          ],
          get_form_api: '/handle_forms',
          save_form_api: '/handle_forms',
        },
      },
      {
        path: "/master_settings",
        name: "master settings",
        component: () => import("pages/SettingsPage.vue"),
        beforeEnter: requireAuth,
        props: { 
          api_route: '/login/master_settings', 
          page_title: 'Admin Settings',
          forms_input: [
            { model: 'Permission', form: 'permission_settings'}, 
            { model: 'AccessLevel', form: 'access_settings' },
          ],
          get_form_api: '/handle_forms',
          save_form_api: '/handle_forms',
        },
      },
      // {
      //   path: "/create_user",
      //   component: () => import("pages/LoginPage.vue"),
      //   beforeEnter: requireAuth,
      // },
      {
        path: "/blank",
        component: () => import("pages/EmailTest.vue"),
        // beforeEnter: requireAuth,
        props: { 
          page_title: 'Page Test',
          forms: ['test_email'],
          get_form_api: '/handle_forms',
          save_form_api: '/test_email',
        }
      },
      {
        path: "/forms_page",
        component: () => import("pages/FormsPage.vue"),
        // beforeEnter: requireAuth,
        props: { 
          page_title: 'Forms Page Test',
          forms: ['add_shift'],
          get_form_api: '/handle_forms',
          save_form_api: '/handle_forms',
        }
      },
      {
        path: "/form",
        component: () => import("pages/BuildTest.vue"),
        // beforeEnter: requireAuth,
        // props: { 
        //   page_title: 'Add User',
        //   forms: ['add_user'],
        //   get_form_api: '/handle_forms',
        //   save_form_api: '/handle_forms',
        // }
      },
    ],

  },
  
  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
