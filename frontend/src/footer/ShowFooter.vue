<template>
  <el-divider />
    <div style="display: flex; justify-content: center;">
  <div>
    <img src="../assets/bono2.jpg" alt="logo" style="width: 30px; height: 30px; margin-right: 25px;">
  </div>
  <div>
    <h2 class="footer-logo">Created by WangCham</h2>
    <a href="https://twitter.com/wagcham" target="_blank">
      <img src="../assets/twitter.svg" 
          alt="Twitter" width="30" height="30">
    </a>
    <h2 class="footerlogo" @click="showAbout()">关于本站</h2>
  </div>
</div>
</template>


<script>
  export default{
    name:'ShowFooter',
    methods:{
      showAbout(){
        this.$router.push({path:'/about'})
      }
    }
  }
</script>

<style>
.footer-logo{
  font: 12px/1 Tahoma,Helvetica,Arial,"\5b8b\4f53",sans-serif;
  font-size: 15px;
}

</style>
