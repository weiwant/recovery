// pages/circle/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    TabCur: 0,
    scrollLeft:0,
    post:[
      {
        postId:1,
        userImg:'https://s2.loli.net/2023/04/14/boRaWVHMzskLc6B.jpg',
        userName:'疗康院康复师9527',
        isDoctor:1,
        time:'2023年4月3日 14:44',
        content:'今天很荣幸参加了由GZCPT主办的脑卒中康复治疗学习班，“镜”观其变，以“镜”促动--带您走进脑卒中后康复的镜像世界了解到了新镜子疗法。在这里把一些要点分享给大家😊😊😊。镜像疗法是基于镜像神经元理论，利',
        view:1684,
        isGood:0,
        good:883,
        comment:307,
        imgList:[
          {url:'https://s2.loli.net/2023/04/14/nMYUPyKBTxjgqSG.png'},
          {url:'https://s2.loli.net/2023/04/14/VkqXaetJ3cGCnAU.png'},
          {url:'https://s2.loli.net/2023/04/14/ksPzQiIdbVg5rZm.png'},
        ]
      },
      {
        postId:2,
        userImg:'https://s2.loli.net/2023/04/14/SxzmLAo8sNvhGYt.jpg',
        userName:'早日康复',
        isDoctor:0,
        time:'2023年4月2日 15:53',
        content:'最近治疗效果逐渐好转，医生说还有一些注意事项，在这里分享给大家~ ~1. 在病情稳定后，对留有后遗症的患者，3个月内应抓紧时机及早进行康复治疗。2. 良肢位的摆放。（中风偏瘫最有利的肢体摆放）3. 肢体康',
        view:684,
        isGood:1,
        good:124,
        comment:87,
        imgList:[
          {url:'https://s2.loli.net/2023/04/14/7McpjWKHz4YSiJ5.jpg'},
          {url:'https://s2.loli.net/2023/04/14/RnJUVbxtT7Qq6sW.jpg'},
        ]
      },
      {
        postId:2,
        userImg:'https://s2.loli.net/2023/04/14/vZo9rCgjNGIPSb2.jpg',
        userName:'幸福',
        isDoctor:0,
        time:'2023年3月28日 08:31',
        content:'这个月终于完成了本阶段的步行训练！康复师说我离成功又近了一步！步行训练一开始真的很困难，在这里给大家几点经验分享，希望可以帮到大家！1. 刚开始可以先原地踏步，逐渐慢慢练习',
        view:356,
        isGood:0,
        good:77,
        comment:24,
        imgList:[
        ]
      }
  ],
  },
  tabSelect(e) {
    this.setData({
      TabCur: e.currentTarget.dataset.id,
      scrollLeft: (e.currentTarget.dataset.id-1)*60
    })
  },
  change:function(){
    this.setData({
      index: (this.data.item + 1) % 2
    })
  },
  goTo:function(){
    wx.navigateTo({
      url: '../fabu/index',
    })
  },
  goToDetail:function(e){
    // console.log(this.data);
    console.log(e.currentTarget);
    console.log(e.currentTarget.id);
    wx.navigateTo({
      url: '../circleDetail/index?id='+e.currentTarget.id,
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
        selected: 2
      })
    }
  },
})