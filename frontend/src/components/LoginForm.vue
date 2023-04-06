<template>
    <div>
      <el-input v-model="username" placeholder="username" />
      <el-input v-model="password" placeholder="password" type="password" class="passwordmargin" />
      <div class="buttons">
        <el-button @click="login">登录</el-button>
        <span class="spacer"></span>
        <el-button @click="showRegisterForm = true" color="#626aef">注册</el-button>
        <el-dialog v-model="showRegisterForm" title="注册">
          <RegisterForm></RegisterForm>
        </el-dialog>
      </div>
    </div>
  </template>
  
  <script>
  import RegisterForm from './RegisterForm.vue'
  import { Dialog } from 'element-plus'
  import { ElMessage } from 'element-plus'
  import axios from 'axios'
  import common from '../assets/js/common'
  
  export default {
    name: 'loginForm',
    components: {
      RegisterForm,
      'el-dialog': Dialog
    },
    data() {
      return {
        username: '',
        password: '',
        showRegisterForm: false
      }
    },
    methods: {
      login() {
        axios.post(common.backend_prefix + '/login', {
            username: this.username,
            password: this.password
          }, {
            withCredentials: true  // 发送请求时带上session
          })
          .then(response => {
            // handle success
            console.log(response);
            if (response.data.status == 'fail') {
              ElMessage.error(response.data.message)
            } else {
              ElMessage.success(response.data.message)
              this.$emit('login-success', { username: this.username })
            }
          })
          .catch(error => {
            // handle error
            console.log(error);
          });
      },
    }
  }
  </script>
  
  <style>
  .passwordmargin {
    margin-top: 20px;
  }
  
  .buttons {
    margin-top: 20px;
  }
  
  .spacer {
    margin-right: 100px;
  }
  </style>
  


