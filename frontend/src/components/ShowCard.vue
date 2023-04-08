<template>
    <div class="carddialog">
        <p>{{ card.created_at }}</p>
        <div id="splash_area">
            <el-image :src="url" alt="detailedimage" style="margin-bottom: 20px; max-width: fit-content;" />
        </div>
        <p>{{ card.text }}</p>
        <el-avatar :size="50" :src="avatar_url" @click="showprofile(card)"/>
        <p>{{ card.username }}</p>
    </div>
</template>

<script>
import common from '../assets/js/common'
import axios from 'axios'
import {ElMessage} from 'element-plus'
import {store} from '../store.js'

export default{
    props:{
        card:{
            type:Object,
            required:true
        },
    },
    data(){
        return{
            avatar_url:'',
            text:'',
            url:'',
            store,
        }
    },
    mounted(){
        console.log('进入到showcard中')
        axios
        .post(common.backend_prefix+'/get_images_from_results',{username:this.card.username,created_at:this.card.created_at},{responseType:'blob'})
        .then(response =>{
            console.log(response)
            if(response.data.status == 'fail'){
                ElMessage.error(response.data.message)
            }else{
                console.log('接收到结果')
                let blob = new Blob([response.data], { type: response.data.type })
                const url = URL.createObjectURL(blob)
                this.url = url
            }
        }).catch(error=>{
            console.log(error)
        })
        const username = this.card.username
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
              this.avatar_url = url            
            }
          })
          .catch(error => {
            console.log(error)
          })
      },
      methods:{
        showprofile(card){
            this.store.user = card.username;
            this.$router.push({path:'/publicprofile'})
        }
      }
}


</script>

<style>
#splash_area{
  position: relative;
  margin-top: 0px;
  margin-inline: 0px;
  width: 100%;
}
</style>