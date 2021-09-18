import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';
import Upload from '../components/Upload.vue';
import Edit from '../components/Edit.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
    },
    {
      path: '/upload',
      name: 'Upload',
      component: Upload,
    },
    {
      path: '/edit',
      name: 'Edit',
      component: Edit,
    },
  ],
});
