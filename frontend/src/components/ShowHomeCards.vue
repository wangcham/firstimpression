<template>
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
<el-dialog v-model="showdialog" title="详细信息" destroy-on-close>
    <ShowCard :card="currentCard"></ShowCard>
</el-dialog>
</template>

<script>
import axios from 'axios'
import common from '../assets/js/common'
import { ElMessage } from 'element-plus'
import ShowCard from './ShowCard.vue'
import {store} from '../store.js'
import { Dialog } from 'element-plus'
export default{
    name:'ShowHomeCards',
    components:{
        ShowCard,
        'el-dialog': Dialog
    },
    data(){
        return{
            cards:[],
            cardUrls:{},
            cardinfo:[],
            showdialog:false,
            store,
        }
    },
    mounted(){
        this.search();
    },
    computed: {
        currentCard() {
            return this.cardinfo;
        }
    },
    methods:{
        search(){
            axios.post(common.backend_prefix+'/get_homepage_cards')
            .then(
                response =>{
                    console.log(response.data);
                    if(response.data.status == 'fail'){
                        console.log(response.data.message);
                    }else{
                        this.cards = response.data;
                        console.log('gethomepagecards中接受和定义成功');
                    }

                }
            ).catch(
                error =>{
                    ElMessage.error(error)
                }
            )
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
            showcard(card){
                this.cardinfo = card;
                this.showdialog = true;
            }
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

