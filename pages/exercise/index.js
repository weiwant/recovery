// pages/exercise/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    list: ['2023-4-4','2023-4-5', '2023-4-6', '2023-4-8', '2023-4-9', '2023-4-10','2023-4-12','2023-4-13','2023-4-14','2023-4-15','2023-4-16'],
    results:[
      {
        date:'04-16',
        isMorn:1,
        time:'10:00',
        grades:95,
        advice:'本次的练习中，请注意手臂抬起的角度与高度。其中，右臂与右肩的角度可以适当减小，避免过度训练，引起右大臂肌肉群拉伤，影响右大臂肌肉功能恢复。'
      },
      {
        date:'04-15',
        isMorn:0,
        time:'14:00',
        grades:89,
        advice:'在摆臂练习中，要注意手臂抬起的角度与高度。注意不要过度训练，引起肌肉损伤。'
      },
    ]
   
  },
  goTo:function(){
    wx.navigateTo({
      url: '../video/index',
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
  onShow() {

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

  }
})