// pages/search/index.js
const app=getApp()
const baseUrl=app.globalData.baseUrl

Page({

  /**
   * 页面的初始数据
   */
  data: {
    keyword:'',
    news:[],
    userId:'lsfjds525',
  },

  // 搜索功能实现
  getNews(){
    // console.log(this.data.type)
    // console.log(this.data.userId)
    
    wx.request({
      url:baseUrl+'/article/search',
      
      method:'POST',
      data:{
        keyword:this.data.keyword,
        userid:this.data.userId
      },
      success:(res)=>{

        //console.log(res),
        //转存到news[]
        this.setData({
          news:res.data,
        })
      },
      fail(){
        console.log('获取失败')
        wx.showToast({
          title: '暂无内容',
          icon:null
        })
      },
      complete(){
      }
    })
  },
  //跳转详情 
  goToDetail:function(e){
    //console.log(e.currentTarget.id)
    wx.navigateTo({
      url: '../article/index?id='+e.currentTarget.id
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      keyword:options.keyword,
    });
    console.log( "onload"+this.data.keyword)
    this.getNews()

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