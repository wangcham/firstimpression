<template>
    <div class="carddialog">
        <p>{{ item.created_at }}</p>
        <div id="splash_area">
            <el-image :src="item.imgUrl" alt="detailedimage" style="margin-bottom: 20px; max-width: fit-content;" />
        </div>
        <p>{{ item.text }}</p>
        <el-avatar :size="50" :src="avatar_url" />
        <p>{{ currentUser }}</p>
        <div>
            <el-button type="warning" @click="showdelete=true">删除</el-button>
            <el-button type="default" @click="showupdate=true,gettext()">更改</el-button>
        </div>
    </div>
    <el-dialog v-model="showdelete" tile="是否删除本条印象？">
        <p>是否删除本条印象？</p>
        <el-button type="default" @click="hidedelete()">取消</el-button>
        <el-button type="primary" @click="confirmdelete(),hidedelete()">确定</el-button>
    </el-dialog>
    <el-dialog v-model="showupdate" title="更改印象文本">
        <div class="update">
            <p style="text-align: center;">更改此条印象的描述</p>
            <p style="text-align:center">文本最大长度为500字</p>
        </div>
        <el-input v-model="text" type="textarea" :autosize="{ minRows: 4, maxRows: 6 }" class="margin"></el-input>
        <div>
            <el-button type="default" @click="hideupdate()">取消</el-button>
            <el-button type="primary" @click="submitupdate(),hideupdate()">提交更改</el-button>
        </div>
    </el-dialog>
</template>
<script>
import common from '../assets/js/common'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import {store} from '../store.js'
    export default{
    props:{
        item:{
            type:Object,
            required:true
        },
        currentUser:{
            type:String,
            required:true
        },
    },
    data(){
        return{
            avatar_url:'',
            showdelete:false,
            showupdate:false,
            text:'',
            store,
        }
    },
    methods:{
        gettext(){
            axios.post(common.backend_prefix+'/gettext',{
                username:this.store.currentUser,
                created_at:this.item.created_at,
            }).then(
                response =>{
                    console.log(response)
                    if(response.data.status == 'fail'){
                        console.log(response.data.message)
                    }else{
                        this.text = response.data;
                    }
                }
            ).catch(
                error =>{
                    console.log(error)
                }
            )
        },
        hideupdate(){
            this.showupdate = false
        },
        submitupdate(){
            const username = this.store.currentUser;
            axios.post(common.backend_prefix+'/updateitem',{
                username:username,
                created_at:this.item.created_at,
                text:this.text
            }).then(
                response =>{
                    if(response.data.status == 'success'){
                        ElMessage.success(response.data.message)
                    }else{
                        ElMessage.error(response.data.message)
                    }
                }
            ).catch(
                error =>{
                    console.log(error)
                }
            )
        },
        hidedelete(){
            this.showdelete = false;
        },
        confirmdelete(){
            axios.post(common.backend_prefix+'/deleteitem',{username:this.store.currentUser,created_at:this.item.created_at}).then(
                response =>{
                    console.log(response);
                    if(response.data.status == 'fail'){
                        ElMessage.error(response.data.message);
                    }else{
                        ElMessage.success(response.data.message)
                    }
                }
            ).catch(
                error =>{
                    console.log(error)
                }
            )
        }
    },
    mounted(){
        const username = this.store.currentUser;
        axios.post(common.backend_prefix+'/getavatar',{username:username},{responseType:'blob'})
        .then(
            response => {
                console.log(response)
                if(response.data.status == 'fail'){
                    console.log(response.data.message);
                }else{
                    console.log(response.data.message);
                    let blob = new Blob([response.data], { type: response.data.type});
                    this.avatar_url = URL.createObjectURL(blob);
                }
            }
        ).catch(
            error=>{
                console.log(error)
            }
        )
    }
    }
</script>
<style>
.carddialog{
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: auto;
}
#splash_area{
  position: relative;
  margin-top: 0px;
  margin-inline: 0px;
  width: 100%;
}
</style>