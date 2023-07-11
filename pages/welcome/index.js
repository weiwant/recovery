// pages/welcome/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    code:'',
    nickName:'',
    avatarUrl:'',
    hasUserInfo:false,
  },

  goTo:function(){
    // 获取code
    wx.login({
      success: (res) => {
        console.log(res);
        this.setData({
         code: res.code,
        });
      },
    })
    // 获取用户名和头像
    if(!this.data.hasUserInfo){
      wx.getUserProfile({
        desc: '用于完善个人资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
        success: (res) => {
          this.setData({
            nickName: res.userInfo.nickName,
            avatarUrl:res.userInfo.avatarUrl,
            hasUserInfo: true
          });
          console.log(res);
          // 将基本信息保存在缓存中
          wx.setStorage({
            key:"userInfo",
            data:{
              nickname:this.data.nickName,
              userImg:this.data.avatarUrl,
              userId:'lsfjds525',
            }
          });
          wx.switchTab({
            url: '../index/index',
          })
        }
      })
    }
     
    
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {
    console.log(this.data)
    

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {
    
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})