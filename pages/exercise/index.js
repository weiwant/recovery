// pages/exercise/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    taskId:0,
    list: ['2023-6-4','2023-6-5', '2023-6-6', '2023-6-8', '2023-6-9', '2023-6-10','2023-6-12','2023-6-13','2023-6-14','2023-6-15','2023-6-16'],
    ddl:'2023年5月5日',
    name:'步行练习',
    diff:'难',
    done:'0',
    all:'30天',
    detail:'侧卧，屈曲下侧腿。伸直上侧腿。将上便腿向外侧抬起至45度,保持1-2秒，徐徐放下。每组15次。该练习可以塌加膝关节侧方稳定性。',
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
    this.setData({
      taskId:options.id,
    });
    console.log(this.data.taskId);
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