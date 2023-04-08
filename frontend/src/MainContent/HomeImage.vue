<template>
    <div>
        <div id="splash_area">
            <a href="https://www.wikiart.org/zh/ke-lao-de-mo-nai/garden-at-sainte-adresse">
            <img alt="garden-at-sainte-adresse" src="../assets/garden-at-sainte-adresse.jpg" id="splash" target="_blank">
            </a>
        </div>
    </div>
<el-divider/>
</template>
<style>
#splash_area{
  position: relative;
  margin-top: 0px;
  margin-inline: 0px;
  width: 100%;
}
#splash{
  display:block;
  width: 100%;
}
#splash_area::before, #splash_area::after {
  content: "";
  position: absolute;
  left: 0;
  width: 100%;
  height: 50px;
  background: linear-gradient(to top, rgba(255,255,255,0), rgba(255,255,255,1) 70%);
  z-index: 1;
}

#splash_area::after {
  top: calc(100% - 50px);
  background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,1) 70%);
}

</style>