<template>
  <div class="header">
      <div class="left">
      <img alt="All That You Can't Leave Behind" src="../assets/bono2.jpg" class="headerimage" style="cursor:pointer" @click="showHomePage">
      </div>
      <div class="headlogo" @click="showHomePage" style="cursor:pointer">FirstImpression</div>
      <div class="spacer"></div>
      <div class="searchbarandmenu" style="display: flex;">
          <SearchBar/>
          <MenuItem />
      </div>
  </div>
</template>


<script>
    import SearchBar from './SearchBar.vue'
    import MenuItem from './MenuItem.vue';
    export default{
        name:'ShowHeader',
        components:{
            SearchBar,
            MenuItem,
        },
        methods:{
          showHomePage(){
            this.$router.push({path:'/homepage'});
          }
        }
    }
</script>

<style>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
}
.spacer{
  flex-grow: 1;
}
.left {
  display: flex;
  align-items: center;
}
.headerimage {
  width: 40px;
  height: 40px;
  margin-left:20px;
}
.headlogo {
  font-family: "Lucida Handwriting", cursive;
  margin-left: 20px;
}
@media (max-width: 767px) {
  .header {
    display: flex;
    flex-direction: column;
  }
}
</style>