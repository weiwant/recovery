// pages/doctor/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    index:0,
    doctorList:[
      {
        name:'赵正平',
        id:'104168891',
        hospital:'中南医院康复科医师',
        imgUrl:'https://s2.loli.net/2023/04/17/mbhk3zOcYalJE1Q.jpg'
      },
      {
        name:'林静',
        id:'105768941',
        hospital:'中南医院康复科副主任',
        imgUrl:'https://s2.loli.net/2023/04/26/a1j2zXPAhdQ7i4D.jpg'
      }
    ]
  },
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
  hideModal1(e) {
    this.setData({
      modalName: null,
      index: 1,
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