<template>
<header>
  <ShowHeader />
</header>
<el-main>
  <MainPage />
</el-main>
<footer>
  <ShowFooter />
</footer>
</template>

<script>
import ShowHeader from './Header/ShowHeader.vue';
import ShowFooter from './footer/ShowFooter.vue';
import MainPage from './MainContent/MainPage.vue';

export default{
  name:'App',
  components:{
    ShowFooter,
    ShowHeader,
    MainPage
}
}
</script>

<style>
footer {
    text-align: center;
}

</style>