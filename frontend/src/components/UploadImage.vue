<template>
  <div>
    <div v-if="!fileuploaded">
      <label for="file-input" class="file-input-label">
        <span>选择图片</span>
        <input id="file-input" type="file" accept="image/*" @change="onFileChange">
      </label>
    </div>

    <div v-if="fileuploaded">
      <img :src="fileUrl" style="max-width: 100%; max-height: 400px;">
    </div>
    <p>文本的最大限度为：500字</p>
    <el-input
      type="textarea"
      v-model="text"
      placeholder="请上传关于图片的叙述"
    />
    

    <div>
      <el-button type="button" @click="submitUpload" v-if="fileuploaded">上传</el-button>
      <el-button type="button" @click="cancel" v-if="fileuploaded">清除内容</el-button>
    </div>
  </div>
</template>

<script>
import common from '../assets/js/common';
import axios from 'axios';
import {ElMessage} from 'element-plus'
export default {
  name: 'UploadImage',
  props: ['currentUser'],
  data() {
    return {
      file: null,
      text: '',
      fileUrl: '',
      fileuploaded: false,
    };
  },
  methods: {
    onFileChange(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.file = files[0];
        if (this.file) {
          this.fileUrl = URL.createObjectURL(this.file);
          this.fileuploaded = true;
          console.log(this.file)
        }
        console.log(this.file);
      }
    },
    cancel() {
      this.file = null;
      this.fileUrl = null;
      this.fileuploaded = false;
      this.text = ''
    },
    async submitUpload() {
      let formData = new FormData();
      formData.append('image',this.file);
      formData.append('text', this.text);
      formData.append('user_id', this.currentUser);

      const loadingInstance = this.$loading({
        lock: true,
        text: '上传中...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)',
      });
      try {
        await axios.post(common.backend_prefix + '/upload', formData)
          .then(response => {
            // 处理成功响应
            console.log(response);
            if (response.data.status === 'fail') {
              ElMessage.error(response.data.message)
            } else {
              ElMessage.success(response.data.message)
              this.$emit('update-upload',false)
            }
          })
          .catch(error => {
            // 处理请求错误
            console.log(error);
          })
          .finally(() => {
            // 隐藏 loading 界面
            loadingInstance.close();
          });
      } catch (error) {
        // 处理 try 块中的错误
        console.log(error);
      }
    }
  }
}
</script>
