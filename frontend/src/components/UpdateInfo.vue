<template>
    <div>
        <h1>更改密码</h1>
        <el-button type="default" @click="showdesc=true">或者更改账户描述</el-button>
    </div>
    <el-input v-model="oldpassword" placeholder="old password" class="passwordmargin" />
    <el-input v-model="newpassword" placeholder="new password" class="passwordmargin" />
    <el-input v-model="newpasswordagain" placeholder="please type your new password again" class="againmargin"></el-input>
    <el-button color="#626aef" id="submit" @click="checkForm">提交更改</el-button>
    <el-dialog v-model="showdesc" title="更改账户描述">
        <p>最大文本数为255个字符</p>
        <el-input v-model="desc" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" class="margin" style="margin-bottom: 20px;"></el-input>
        <el-button @click="updatedesc(),hideupdatedesc()" type="primary">提交</el-button>
        <el-button @click="hideupdatedesc()">取消</el-button>
    </el-dialog>
</template>
<script>
import { ElMessage } from 'element-plus';
import common from '../assets/js/common';
import axios from 'axios';
    export default{
        name:'UpdateInfo',
        props:['currentUser'],
        data(){
            return{
                username:'',
                oldpassword:'',
                newpassword:'',
                newpasswordagain:'',
                desc:'',
                showdesc:false,
            };
        },
        
        methods:{
            updatedesc(){
                axios.post(common.backend_prefix+'/updatedesc',{
                    username:this.currentUser,
                    desc:this.desc,
                }).then(
                    response =>{
                        if(response.data.status == 'fail'){
                            ElMessage.error(response.data.message)
                        }else{
                            ElMessage.success(response.data.message)
                        }
                    }
                )
            },
            hideupdatedesc(){
                this.showdesc = false;
            },  
            checkForm(){
                if(this.oldpassword == null|| this.newpasswordagain == null||this.newpassword == null){
                    ElMessage.error('请输入密码')
                    return;
                }
                if(this.newpassword == this.oldpassword){
                    ElMessage.error('新旧密码一致')
                    return;
                }
                if(this.newpassword !== this.newpasswordagain){
                    ElMessage.error('两次密码输入不一致')
                }
                this.username = this.currentUser;
                axios.post(common.backend_prefix+'/updateinfo',{
                    username:this.username,
                    newpassword:this.newpassword,
                }).then(response =>{
                    console.log(response);
                    if(response.data.status == 'fail'){
                        ElMessage.error(response.data.message)
                    }else{
                        ElMessage.success(response.data.message)
                        this.$emit('update-info',false)
                    }
                }).catch(error => 
                {
                    console.log(error)
                })
            },
        },
        mounted(){
            axios.post(common.backend_prefix+'/getdesc',{username:this.currentUser})
                .then(
                response =>{
                    console.log(response);
                    if(response.data.status == 'fail'){
                    console.log(response.data.message);
                }else{
                    console.log(response.data.message);
                    this.desc = response.data;
                }
                }
                )
        }
    }
</script>



<style>
    .margin{
        margin-top: 30px;
    }
</style>
