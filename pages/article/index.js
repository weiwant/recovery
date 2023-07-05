// pages/article/index.js
const baseUrl="http://1636fb15.r1.cpolar.top/recovery/api"

Page({

  /**
   * 页面的初始数据
   */
  data: {
    newsId:0,
    isArticle:0,
    url:'',
    author:'',
    createTime:'',
    title:'',
    content:''

    
  },
  getDetail(){
    
    wx.request({
      url: baseUrl+'/article/get_detail',
      method:'POST',
      data:{
        id:this.data.newsId
      },
      success:(res)=>{
        //console.log(res.data[0])
        this.setData({
          isArticle:res.data[0].type,
          url:res.data[0].url,
          author:res.data[0].author,
          createTime:res.data[0].create_time,
          title:res.data[0].title,
          content:res.data[0].content
        })
      }
    })

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //console.log(options)
    this.setData({
      newsId:options.id,
    });
    this.getDetail()

    
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