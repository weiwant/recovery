// pages/mine/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
      nickName:'游客',
      userId:'0000000',
      userImg:'https://s2.loli.net/2023/07/04/GawxuWsANhVM71c.png'
  },
  goToDoctor:function(){
    wx.navigateTo({
      url: '../doctor/index?userId='+this.data.userId,
    })
  },
  goToUaerInfo:function(){
    wx.navigateTo({
      url: '../userInfo/index',
    })
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
  onShow(){
    this.tabBar();
    
    var that = this;
    // 从用户缓存中获取数据
    wx.getStorage({
      key: 'userInfo',
      success (res) {
        that.setData({
          nickName:res.data.nickname,
          userImg:res.data.userImg,
          userId:res.data.userId,
        });
      },
    })

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

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

  },
  tabBar() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({
        selected: 3
      })
    }
  },
})