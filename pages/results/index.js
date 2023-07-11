// pages/results/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl

Page({

  /**
   * 页面的初始数据
   */
  data: {
      isSucceed:1,
      grades:null,
      advice:'',
      video:'',
      taskId:0,
  },
  goToExercise:function(){
    wx.navigateTo({
      url: '../exercise/index',
    })
  },
  showModal(name) {
    this.setData({
      modalName: name
    })
  },
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },

  getResult:function(e){ 
    let name= e.currentTarget.dataset.target
    let page = this
    console.log(page.data)
    wx.showLoading({
      title: '分析中',
    })
    wx.request({
      url: baseUrl+'/detail/add',
      method:'POST',
      data:{
        task:page.data.taskId,
        video:page.data.video,
      },
      success:(res)=>{
        wx.hideLoading()
        console.log(res)
        page.setData({
          grades:res.data.score,
          advice:res.data.evaluation,
        })
        page.showModal(name)
      },
      fail:(res)=>{
        wx.hideLoading()
        console.log(res)
        wx.showToast({
          title: '结果获取失败',
          icon:'error',
        })
      },
    })
  } , 

  // 获取用户信息
  getInfo:function(){
    const that=this
    wx.getStorage({
      key: 'taskInfo',
      success (res) {
        //console.log(res)
        that.setData({
          taskId:res.data.taskId,
        });
      },
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    console.log(options)
    this.setData({
      video:options.video
    })
    this.getInfo()
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