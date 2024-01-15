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
      {
        path: "",
        component: () => import("pages/IndexPage.vue"),
        alias: ["/:year*", "/:year*/:month*", "/:year*/:month*/:user*"],
      },
      {
        path: "/schedule_import",
        redirect: "/",
        alias: [
          "/schedule_import/:year*",
          "/schedule_import/:year*/:month*",
          "/schedule_import/:year*/:month*/:user*",
        ],
      },
      {
        path: "/login",
        name: "login",
        component: () => import("pages/LoginPage.vue"),
      },
      // {
      //   path: '/login',
      //   component: () => import('pages/FormsPage.vue'),
      //   children: [
      //     { path: '', component: () => import('components/LoginForm.vue') }
      //   ]
      // },
      {
        path: "/register",
        name: "register",
        component: () => import("pages/RegisterPage.vue"),
      },
      {
        path: "/profile",
        name: "profile",
        component: () => import("pages/ProfilePage.vue"),
        beforeEnter: requireAuth,
      },
      {
        path: "/users",
        name: "users",
        component: () => import("pages/Users.vue"),
        beforeEnter: requireAuth,
      },
      {
        path: "/schedule",
        name: "schedule",
        component: () => import("pages/Schedule.vue"),
      },
      {
        path: "/create_user",
        component: () => import("pages/LoginPage.vue"),
        beforeEnter: requireAuth,
      },
      {
        path: "/forms_page",
        component: () => import("pages/FormsPage.vue"),
        // beforeEnter: requireAuth,
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
