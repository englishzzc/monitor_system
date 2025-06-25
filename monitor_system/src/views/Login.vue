<template>
  <body id = "poster">
    <el-form class="login-container" label-position="left"  label-width="0px">
        <h3 class="login-title">
            系统登陆
            <el-button @click="toRegister()">点我注册</el-button>
        </h3>
        <el-form-item label="">
            <el-input type="text" v-model="loginForm.loginName" autocomplete="off" placeholder="账号"></el-input>
        </el-form-item>
        <el-form-item label="">
            <el-input type="password" v-model="loginForm.password" autocomplete="off" placeholder="密码"></el-input>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" style="width:100%;background-color: #505458; border: none ;" @click="Login()">登录</el-button>
        </el-form-item>
    </el-form>
  </body>
</template>

<script>


export default {
  name: 'Login',
   data() {
      return {
        loginForm: {
          loginName: '',
          password: '',
        }
      }
    },
    methods: {
      Login() {
        console.log('submit!',this.loginForm);
        this.$message({
          message: '成功登录，欢迎来到后台管理系统',
          type: 'success'
        });
        this.$router.push({path:'/Home'})
      },
      toRegister(){
        this.$router.push({path:'/Register'})
      }
    }

}
</script>


<style>
    #poster{
        background-attachment: center;
        height: 100%;
        width: 100%;
        background-size: cover;
        position: fixed;
    }
    body{
        margin: 0px;
        padding: 0px;
    }
    .login-container{
        border-radius: 15px;
        background-clip: padding-box;
        margin: 90px auto;
        width: 350px;
        padding: 35px 35px 15px 35px;
        background-color: #fff;
        border: 1px solid #eaeaee;
        box-shadow: 0 0 25px #cac6c6;
    }
    .login-title{
        margin: 0px auto 40px auto;
        text-align: center;
        color: #505458;
    }
</style>