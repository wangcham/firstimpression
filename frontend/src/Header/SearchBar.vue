<template>
    <div class="search-container">
        <el-input placeholder="请输入内容" v-model="searchtext" />
        <el-button type="default" @click="checksearch()" class="search-button">搜索</el-button>
    </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import {store} from '../store.js'
    export default{
        data(){
            return{
                searchtext:'',
                store,
            }
        }, 
        methods:{
            checksearch() {
  if (this.searchtext == '') {
    ElMessage.error('搜索栏信息不能为空')
    return
  } else {
    this.store.searchtext = this.searchtext;
    this.searchtext = '';
    if (this.$route.path === '/searchresult') {
      this.$router.replace('/blank').then(() => {
        this.$router.push({path:'/searchresult',query: { searchText: this.store.searchtext }});
      });
    } else {
      this.$router.push({path:'/searchresult',query: { searchText: this.store.searchtext }});
    }
  }
}
        }
    }
</script>
<style>
@media (max-width: 767px) {
.search-container {
    width: 100%;
  }
}
.search-container {
  display: flex;
  width: 400px;
  align-items: center;
  justify-content: space-between;
  margin-right:30px;
}
.search-button {
  border: 0;
}
</style>