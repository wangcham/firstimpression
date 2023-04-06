<template>
    <div>
        <h3>头像文件大小不超过1MB</h3>
        <div v-if="!fileuploaded">
            <label for="file-input" class="file-input-label">
                <span>选择头像</span>
                <input id="file-input" type="file" accept="image/*" @change="onFileChange">
            </label>
        </div>
    </div>
    <div v-if="fileuploaded">
        <img :src="fileUrl" style="max-width:100%;max-height:400px">
    </div>
    <div>
      <el-button type="button" @click="submitUpload" v-if="fileuploaded">上传头像</el-button>
      <el-button type="button" @click="cancel" v-if="fileuploaded">清除</el-button>
    </div>
</template>

<script>
    import common from '../assets/js/common';
    import axios from 'axios';
    import { ElMessage } from 'element-plus';
    export default{
        name:'UpdateAvatar',
        props:['currentUser'],
        data(){
            return{
                file:null,
                fileUrl: '',
                fileuploaded:false,
            };
        },
        methods:{
            onFileChange(event){
                const files = event.target.files;
                if(files.length > 0){
                    this.file = files[0];
                    if (this.file.size > 1024 * 1024) {
                        ElMessage.error('图片文件过大，请选择不超过1MB的文件！')
                        return;
                    }
                    if (this.file) {
                        this.fileUrl = URL.createObjectURL(this.file);
                        this.fileuploaded = true;
                        console.log(this.file)
                    }
                    console.log(this.file)
                }
            },
            cancel(){
                this.file = null;
                this.fileUrl = null;
                this.fileuploaded = false;
            },
            async submitUpload(){
                let formData = new FormData();
                formData.append('username',this.currentUser)
                formData.append('image',this.file);

                const loadingInstance = this.$loading({
                    lock:true,
                    text:'上传头像中',
                    spinner:'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)',
                });
                try{
                    await axios.post(common.backend_prefix+'/updateavatar',formData)
                    .then(response =>{
                        console.log(response);
                        if (response.data.status === 'fail') {
                            ElMessage.error(response.data.message)
                        } else {
                            ElMessage.success(response.data.message)
                            this.$emit('update-avatar',false)
                        }
                    })
                    .catch(error =>{
                        console.log(error);
                    })
                    .finally(()=>{
                        loadingInstance.close();
                    })
                }catch(error){
                    console.log(error)
                }
            }
        }
    }
</script>

<style>

</style>