<template>
  <div>
    <el-divider />
    <h2>查询到的用户：</h2>
    <el-divider />
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
  
    <h2>查询到的印象:</h2>
    <el-divider />
    <div class="wrap">
    <div v-for="card in cards" :key="card.created_at">
        <div class="card" style="width: 18rem;">
          <img class="card-img-top" :src="getimage(card)" alt="image">
          <div class="card-body">
            <h5 class="card-title">{{ card.created_at }}</h5>
            <p class="card-text" style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis;">{{ card.text }}</p>
            <a href="#" class="btn btn-primary" @click="showcard(card)">详细信息</a>
          </div>
        </div>
    </div>
  </div>
  </div>
  <el-dialog v-model="showdialog" title="详细信息">
    <ShowCard :card="card"></ShowCard>
  </el-dialog>
  </template>
  
  <script>
  import axios from 'axios'
  import common from '../assets/js/common'
  import { ElMessage } from 'element-plus'
  import ShowCard from './ShowCard.vue'
  import {store} from '../store.js'
  export default {
    name: 'SearchResult',
    components:{
      ShowCard,
    },
    data() {
      return {
        items: [],
        avatarUrls: {},
        cards:[],
        cardUrls:{},
        showdialog:false,
        store,
      }
    },
    watch:{
      '$route.query.searchText': function (newVal, oldVal) {
     if(newVal!==oldVal){
      this.search()
     }
    }
    },
    created(){
      window.onload = () => {
        window.location.reload()
      }
    },
    mounted() {
      this.search()
    },
    methods: {
      search(){
        axios
        .post(common.backend_prefix + '/get_userinfo_from_results', {
          searchtext: this.$route.query.searchText,
        })
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

        axios
        .post(common.backend_prefix+'/get_cards_from_results',{searchtext:this.$route.query.searchText})
        .then(response =>{
            console.log(response)
            if(response.data.status == 'fail'){
                console.log(response.data.message)
            }else{
                console.log(response.data.message)
                this.cards = response.data;
            }
        })
        .catch(error => {
            console.log(error)
        })
    },
      showcard(card){
        this.card = card;
        this.showdialog = true;
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
      getimage(card){
        const {created_at,username} = card
        if(this.cardUrls[created_at] && this.cardUrls[created_at][username]){
            return this.cardUrls[created_at][username]
        }
        axios
        .post(common.backend_prefix+'/get_images_from_results',{username:card.username,created_at:card.created_at},{responseType:'blob'})
        .then(response =>{
            console.log(response)
            if(response.data.status == 'fail'){
                ElMessage.error(response.data.message)
            }else{
                console.log('接收到搜寻结果中的图片')
                let blob = new Blob([response.data], { type: response.data.type })
                const url = URL.createObjectURL(blob)
                if (!this.cardUrls[created_at]) {
                this.cardUrls[created_at] = {}
                }
                this.cardUrls[created_at][username] = url
                return url
            }
        }).catch(
            error =>{
                console.log(error)
            }
        )
    },
    showPublicProfile(item){
      this.store.user = item.username;
      this.$router.push({path:'/publicprofile'})
    },
  }
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