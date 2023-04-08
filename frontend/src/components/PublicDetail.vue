<template>
    <div class="carddialog">
        <p>{{ item.created_at }}</p>
        <div id="splash_area">
            <el-image :src="item.imgUrl" alt="detailedimage" style="margin-bottom: 20px; max-width: fit-content;" />
        </div>
        <p>{{ item.text }}</p>
        <el-avatar :size="50" :src="avatar_url" @click="showPublicProfile()"/>
        <p>{{ store.user }}</p>
    </div>
</template>

<script>
import {store} from '../store.js'
import axios from 'axios'
import common from '../assets/js/common'

export default{
    data(){
        return{
            avatar_url:'',
            showdelete:false,
            showupdate:false,
            text:'',
            store,
        }
    },
    props:{
        item:{
            type:Object,
            required:true
        },
    },
    methods:{
    showPublicProfile(){
      if(this.store.currentUser === this.store.user){
        this.$router.push({path:'/myprofile'});
      }else{
        this.$router.push({path:'/publicprofile'})
      }
    },
    },
    mounted(){
        const username = this.store.user;
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
    },
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
