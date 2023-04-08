<template>
    <div v-if="isLoggedIn">
        <el-menu mode="horizontal"  :collapse="isCollapse" router class="el-menu-demo">
                <el-menu-item index="/myprofile">{{ currentUser }}的主页</el-menu-item>
                <el-menu-item index="/myprofile" @click="showUploadImage=true">上传</el-menu-item>
                <el-menu-item index="/homepage" @click="logout()">退出登录</el-menu-item>
        </el-menu>
    </div>
    <el-dialog v-model="showUploadImage" title='上传图片'>
        <UploadImage :currentUser="currentUser" @update-upload="hideUploadImage"></UploadImage>
    </el-dialog>


    <el-button v-if="!isLoggedIn" @click="showLoginForm = true" color="#626aef">登录/注册</el-button>
    
    <el-dialog v-model="showLoginForm" title="登录">
        <LoginForm @login-success="onLoginSuccess"></LoginForm>
    </el-dialog>
</template>

<script>
import UploadImage from '@/components/UploadImage.vue';
import LoginForm from '@/components/LoginForm.vue';
import { ElDialog } from 'element-plus';
import {store} from '../store.js'
export default{
    name:'MenuItem',
    components:{
        LoginForm,
        UploadImage,
        'el-dialog':ElDialog,
    },
    data(){
        return{
            isCollapse:false,
            showLoginForm:false,
            isLoggedIn:false,
            showUploadImage:false,
            currentUser:'',
            store,
        }
    },
    methods:{
        onLoginSuccess(userInfo) {
            this.isLoggedIn = true;
            this.showLoginForm = false;
            this.currentUser = userInfo.username;
            this.store.currentUser = this.currentUser;
        },
        logout() {
            this.isLoggedIn = false;
            this.currentUser = null;
            this.$router.push({path:'/homepage'})
        },
        hideUploadImage(value){
            this.showUploadImage = value;
        },
        handleResize() {
            this.isCollapse = window.innerWidth < 600;
        },
    },
    mounted() {
        this.handleResize();
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
}
</script>
<style>

.el-menu-demo .el-menu-item{
    border-bottom-color:#ffffff!important;
    font-size: 10px;
}
.el-menu-item {
transition: none !important;
}
</style>