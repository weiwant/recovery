// pages/news/index.js
const baseUrl="http://1636fb15.r1.cpolar.top/recovery/api"

Page({

  /**
   * 页面的初始数据
   */
  data: {
    class:['科普','训练','药物','其他'],
    TabCur: 0,
    scrollLeft:0,
    index:0,
    news:[],
    userId:'lsfjds525',
    postid:0
  },
  /**
   * 根据tab序号获取内容
   */
  getNameFromTab(num){
    
  },
  /**
   * 获取资讯列表
   */
  getNews(){
    
    // console.log(this.data.type)
    // console.log(this.data.userId)
    
    wx.request({
      url:baseUrl+'/article/get_list',
      
      method:'POST',
      data:{
        class_:this.data.class[this.data.TabCur],
        userid:this.data.userId
      },
      
      
      success:(res)=>{

        console.log(res),
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
  /**
   * 切换tab
   */
  tabSelect(e) {
    //console.log(e.currentTarget.dataset.id)
    this.getNameFromTab(e.currentTarget.dataset.id)
    this.setData({
      
      TabCur: e.currentTarget.dataset.id,
      scrollLeft: (e.currentTarget.dataset.id-1)*60
      
    }),
    //console.log(this.data.class)
    //切换tab时获取资讯
    this.getNews()
  },
  goTo:function(){
    wx.navigateTo({
      url: '../question/index',
    })
  },
  /**
   * 资讯详情 跳转到article/index
   */
  goToDetail:function(e){
    //console.log(e.currentTarget.id)
    wx.navigateTo({
      url: '../article/index?id='+e.currentTarget.id
    })
  },
  goToFood:function(){
    wx.navigateTo({
      url: '../article/food',
    })
  },
  change:function(){
    this.setData({
      index: (this.data.index + 1) % 2
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // //获取userid
    // var that = this;
    // // 从用户缓存中获取数据
    // wx.getStorage({
    //   key: 'userInfo',
    //   success (res) {
    //     console.log(res.data);
    //     that.setData({
          
    //       userId:res.data.userId
    //     });
    //   },
    // })
    
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
  onShow(){
    this.tabBar();
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
        selected: 1
      })
    }
  },
})