// pages/addTask/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    pIndex: null,
    patients: ['李淑芬', '王国发', '赵书'],
    dIndex:null,
    difficulty:['易','中','难'],
    date: '2023-7-18',
  },
  DateChange(e) {
    this.setData({
      date: e.detail.value
    })
  },
  PickerChange(e) {
    console.log(e);
    this.setData({
      pIndex: e.detail.value
    })
  },
  PickerChange1(e) {
    console.log(e);
    this.setData({
      dIndex: e.detail.value
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