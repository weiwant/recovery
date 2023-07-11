// app.js
App({
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })
    wx.cloud.init({
      env:'recovery-1gpfqg1b2321ce8b',
      traceUser:true,
    })
  },
  globalData: {
    userInfo: null,
    baseUrl:'http://261f7ab.r8.cpolar.top/recovery/api'
  }
})
