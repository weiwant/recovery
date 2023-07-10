// pages/doctor/index.js
const app = getApp();
const baseUrl=app.globalData.baseUrl

Page({

  /**
   * 页面的初始数据
   */
  data: {
    userId:'lsfjds525',
    doctorList:[
      // {
      //   name:'赵正平',
      //   id:'104168891',
      //   hospital:'中南医院康复科医师',
      //   imgUrl:'https://s2.loli.net/2023/04/17/mbhk3zOcYalJE1Q.jpg'
      // },
      // {
      //   name:'林静',
      //   id:'105768941',
      //   hospital:'中南医院康复科副主任',
      //   imgUrl:'https://s2.loli.net/2023/04/26/a1j2zXPAhdQ7i4D.jpg'
      // }
    ],
    content:'',
  },
  // 绑定窗口显示
  showModal(e) {
    this.setData({
      modalName: e.currentTarget.dataset.target
    })
  },
  // 绑定窗口关闭
  hideModal(e) {
    this.setData({
      modalName: null
    })
  },
  
  // 输入框监听
  contentInput(e){
    console.log(e.detail.value)
    this.setData({
      content:e.detail.value
    })
  },
  // 绑定医生
  addDoctor:function(){
    wx.request({
      url: baseUrl+'/user/bind',
      method:'POST',
      data:{
        patient:this.data.userId,
        doctor:this.data.content,
      },
      success:(res)=>{
        console.log(res.data)
        this.setData({
          modalName: null
        })
      }
    })
  },

  // 获取医生列表
  getDoctorList:function(){
    const that=this
    wx.request({
      url: baseUrl+'/user/doctor_list',
      method:'POST',
      data:{
        patient:that.data.userId,
      },
      success:(res)=>{
        console.log(res.data)
        this.setData({
          doctorList:res.data,
        })
      }
    })
  },
  // 获取用户信息
  getInfo:function(){
    var that = this;
    // 从用户缓存中获取数据
    wx.getStorage({
      key: 'userInfo',
      success (res) {
        console.log(res.data.userId)
        that.setData({
          userId:res.data.userId,
        });
      },
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      userId:options.userId,
    })
   
    
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
    this.getInfo()
    this.getDoctorList()
    
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