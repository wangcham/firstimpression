<template>
<div class="wrap">
    <div v-for="item in items" :key="item.username">
    <div class="card border-secondary mb-3" style="max-width: 20rem;">
        <div class="card-header">{{ item.username }}</div>
        <div class="card-body text-secondary">
        <el-avatar alt="avatar" :src="getavatar(item)" @click="showPublicProfile(item)" style="cursor:pointer"/>
        <p class="card-text">{{ item.desc }}</p>
        </div>
    </div>
    </div>
</div>
</template>

<script>
import axios from 'axios'
import common from '../assets/js/common'
import { ElMessage } from 'element-plus'
import {store} from '../store.js'
export default{
    name:'ShowHomeUsers',
    mounted(){
        this.search();
    },
    data(){
        return{
            items: [],
            avatarUrls: {},
            store,
        }
    },
    methods:{
        search(){
            axios
            .post(common.backend_prefix + '/get_homepage_users',)
            .then(response => {
            console.log(response)
            if (response.data.status == 'fail') {
                console.log(response.data.message)
            } else {
                console.log(response.data.message)
                this.items = response.data
            }
            })
            .catch(error => {
            console.log(error)
            })
        },
        getavatar(item) {
        const { username } = item
        // 如果缓存中已有该用户的头像 URL，直接返回
        if (this.avatarUrls[username]) {
          return this.avatarUrls[username]
        }
        axios
          .post(common.backend_prefix + '/getavatar', { username }, { responseType: 'blob' })
          .then(response => {
            console.log(response)
            if (response.data.status == 'fail') {
              ElMessage.error(response.data.message)
            } else {
              console.log(response.data.message)
              let blob = new Blob([response.data], { type: response.data.type })
              const url = URL.createObjectURL(blob)
              // 将该用户的头像 URL 缓存到 avatarUrls 中
              this.avatarUrls[username] = url
              return url
            }
          })
          .catch(error => {
            console.log(error)
          })
    },
    showPublicProfile(item){
        this.store.user = item.username
        this.$router.push({path:'/publicprofile'})
    },
},
}
</script>

<style>
.wrap{
  display:flex;
  flex-wrap: wrap;
  justify-content: space-around;
  align-items: flex-start;
}
</style>
