import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'popper.js'
import 'jquery'
import 'bootstrap'
import { createRouter, createWebHistory } from 'vue-router'
import MyProfile from './components/MyProfile.vue'
import HomePage from './MainContent/HomePage.vue'
import SearchResult from './components/SearchResult.vue'
import PublicProfile from './components/PublicProfile.vue'
import AboutInfo from './components/AboutInfo.vue'

const app = createApp(App);

const routes = [
    { path: '/', redirect: '/homepage' },
    { path: '/myprofile', name: 'MyProfile', components: { myprofile: MyProfile } },
    { path:'/searchresult',name:'SearchResult',components:{searchresult:SearchResult},props: (route) => ({ searchText: route.query.searchText })},
    { path:'/publicprofile',name:'PublicProfile',components:{publicprofile:PublicProfile}},
    { path:'/about',name:'AboutInfo',components:{aboutinfo:AboutInfo}},
    { path: '/homepage', name: 'HomePage', components: { homepage: HomePage } },
] 

const router = createRouter({
    history: createWebHistory(),
    routes
});
export default router
app.use(ElementPlus);
app.use(router);
app.mount('#app');

