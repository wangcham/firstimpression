<template>
    <h1 id="hint">7位&lt;账号长度&lt;13位</h1>
    <el-input v-model="name" placeholder="name"></el-input>
    <el-input v-model="username" placeholder="username" class="usernamemargin"/>
    <el-input v-model="password" placeholder="password" type="password" class="passwordmargin" />
    <el-input v-model="passwordagain" placeholder="please type your password again" type="password" class="againmargin"></el-input>
    <el-button color="#626aef" id="submit" @click="checkForm">提交</el-button>
</template>
<script>
    import axios from 'axios'
    import common from '../assets/js/common'
    import { ElMessage } from 'element-plus'
    export  default{
        data(){
            return {
                name:'',
                username:'',
                password:'',
                passwordagain:''
            }
        },
        methods:{
            checkForm(){
                if(this.username.length <= 6){
                    ElMessage.error('账号长度过短')
                    return ;
                }
                if(this.username.length > 13){
                    ElMessage.error('账号长度过长')
                    return;
                }
                if(this.password == null|| this.passwordagain == null){
                    ElMessage.error('请输入密码')
                    return;
                }
                if (this.password !== this.passwordagain) {
                    ElMessage.error('两次输入的密码不一致，请重新输入')
                    return;
                }
                axios.post(common.backend_prefix+'/register', {
                    name: this.name,
                    username: this.username,
                    password: this.password
      })
      .then(response => {
        console.log(response);
        if(response.data.status == 'fail'){
            ElMessage.error(response.data.message)
        }else{
            ElMessage.success(response.data.message)
        }
      })
      .catch(error => {
        console.log(error);
        
      });
            },
        }
    }
</script>
<style>
.usernamemargin{
    margin-top: 20px;
}
#hint{
    margin-top: 20px;
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}
#submit{
    margin-top: 20px;
}
.againmargin{
    margin-top: 20px;
}
.passwordmargin{
    margin-top:20px;
}
</style>
