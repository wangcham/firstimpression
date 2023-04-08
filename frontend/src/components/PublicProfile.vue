<template>
    <el-divider />
    <div style="margin-bottom: 30px; margin-top: 30px;">
    <div style="display: flex; align-items: center; justify-content: center;">
      <el-avatar :size="70" :src="avatar_url" style="margin-right: 20px ; cursor: pointer;"/>
      <h1 style="text-align: center; font: normal normal normal 12px/1 Tahoma,Helvetica,Arial,'\5b8b\4f53',sans-serif; font-size: 25px;">{{ store.user }}</h1>
    </div>
    <div>
      <p style="text-align: center; font-family: Arial; margin-top: 30px;">{{ this.desc }}</p>
    </div>
 </div>

 <el-divider />
  <div class="wrap">
    <div v-for="item in items" :key="item.created_at">
        <div class="card" style="width: 18rem;">
          <img class="card-img-top" :src="item.imgUrl" alt="image">
          <div class="card-body">
            <h5 class="card-title">{{ item.created_at }}</h5>
            <p class="card-text" style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ item.text }}</p>
            <a href="#" class="btn btn-primary" @click="publicdetail(item)">详细信息</a>
          </div>
        </div>
    </div>
  </div>

  <el-dialog v-model="showdialog" title="详细信息">
    <PublicDetail :item="selectedItem" :user="store.user"></PublicDetail>
  </el-dialog>
</template>

<script>
import {store} from '../store.js'
import PublicDetail from './PublicDetail.vue';
import axios from 'axios'
import common from '../assets/js/common'
    export default{
        name:'ShowProfile',
        data(){
            return{
                items:[],
                store,
                avatar_url:'',
                desc:'',
                showdialog:false,
                selectedItem:[],
            }
        },
        components:{
            PublicDetail,
        },
        created() {
        const username = this.store.user;
        axios.post(common.backend_prefix + '/myprofile', { username: username })
        .then(response => {
          console.log(response);
          if (response.data.status == 'fail') {
            console.log(response.data.message);
          } else {
            console.log(response.data.message);
            this.items = response.data;
            const promises = this.items.map((item, index) => {
              return this.getImage(item, index);
            });
            Promise.all(promises).then(() => {
              console.log('All images loaded!');
            });
          }
        })
        .catch(error => {
          console.log(error);
        });
      },
  mounted(){
    const username = this.store.user;
    axios.post(common.backend_prefix+'/getavatar',{username:username},{responseType:'blob'})
    .then(response =>{
      console.log(response);
      if(response.data.status == 'fail'){
        console.log(response.data.message);
      }else{
        console.log(response.data.message);
        let blob = new Blob([response.data], { type: response.data.type});
        this.avatar_url = URL.createObjectURL(blob);
      }
    })
    .catch(error =>{
      console.log(error)
    })



    axios.post(common.backend_prefix+'/getdesc',{username:username})
    .then(
      response =>{
        console.log(response);
        if(response.data.status == 'fail'){
        console.log(response.data.message);
      }else{
        console.log(response.data);
        this.desc = response.data;
      }
      }
    )
  },
  methods:{
    async getImage(item, n) {
      let username = this.store.user;
      let response = await axios.post(common.backend_prefix+'/getimage',  { username: username, n: n }, { responseType: 'blob' });
      let blob = new Blob([response.data], { type: response.data.type});
      item.imgUrl = URL.createObjectURL(blob);
    },
    publicdetail(item){
      this.showdialog = true;
      this.selectedItem = item;
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
.card {
  width: 300px;
  margin: 10px;
}
hr {
  border: none;
  height: 2px;
  background-color: #333;
}
</style>
