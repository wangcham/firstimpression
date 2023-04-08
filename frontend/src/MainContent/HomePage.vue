<template>
  <div>
    <HomeImage />
    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a class="nav-link" href="#" @click="showtabscontenttrue()">Impressions</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#" @click="showtabscontentfalse()">Users</a>
      </li>
    </ul>
    <div class="tab-content">
      <div class="tab-pane fade" :class="{ 'show active': showtabs }">
        <ShowHomeCards></ShowHomeCards>
      </div>
      <div class="tab-pane fade" :class="{ 'show active': !showtabs }">
        <ShowHomeUsers></ShowHomeUsers>
      </div>
    </div>
  </div>
</template>

<script>
import HomeImage from './HomeImage.vue';
import ShowHomeCards from '@/components/ShowHomeCards.vue';
import ShowHomeUsers from '@/components/ShowHomeUsers.vue';

export default {
  name: 'HomePage',
  components: {
    HomeImage,
    ShowHomeCards,
    ShowHomeUsers,
  },
  data(){
    return{
      showtabs:true,
    }
  },
  methods:{
    showtabscontenttrue(){
      this.showtabs = true;
    },
    showtabscontentfalse(){
      this.showtabs = false;
    }
  }
}
</script>

<style>
.tab-content {
  position: relative;
  z-index: 1;
}
</style>
