
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/login', component: () => import('pages/LoginPage.vue') },
      { 
        path: '/schedule_import', 
        component: () => import('pages/ScheduleImport.vue') ,
        alias: [
          '/schedule_import/:year*', 
          '/schedule_import/:year*/:month*', 
          '/schedule_import/:year*/:month*/:user*'
        ],
      },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
