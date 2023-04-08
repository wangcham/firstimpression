<template>
  <el-divider />
  <div class="footer-container">
    <div class="logo-container">
      <img src="../assets/bono2.jpg" alt="logo" class="logo">
      <h2 class="footer-logo">Created by WangCham</h2>
      <a href="https://twitter.com/wagcham" target="_blank">
        <img src="../assets/twitter.svg" alt="Twitter" class="twitter-logo">
      </a>
    </div>
    <div class="about-container">
      <p @click="showAbout()">关于本站</p>
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
.footer-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  width: 30px;
  height: 30px;
  margin-right: 25px;
}

.footer-logo {
  font: 12px/1 Tahoma, Helvetica, Arial, "\5b8b\4f53", sans-serif;
  font-size: 15px;
  margin-right:20px;
}

.about-container {
  display: flex;
  align-items: center;
}

.twitter-logo {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

p {
  text-align: right;
  cursor: pointer;
}
</style>

