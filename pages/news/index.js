// pages/news/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    TabCur: 0,
    scrollLeft:0,
    index:0,
    news:[
      {
        title:'脑卒中，一种在中国发病率极高的疾病。',
        imgUrl:'https://s2.loli.net/2023/04/15/OoIvMjgVNFQGqBW.png',
        content:'脑卒中（stroke），又称脑血管意外（CVA），是指突然发生的、由脑血管病变引起的局限的或全脑的功能障碍，持续时间超过24h或引起死亡的临床综合征。我们需要知道的关于脑卒中的一些危险因素。a可调控因素：高血压、糖尿病、心脏病、高脂血症等b.可改变的因素：不良饮食习惯、大量饮酒、吸烟等c.不可变的因素：年龄、性别、家族史等',
        isAcrticle:1,
        tag:'科普读物',
        isCollected:0,
      },
      {
        title:'脑卒中后康复训练1(上肢)',
        imgUrl:'https://s2.loli.net/2023/04/15/Bolacp5h87jxr3P.png',
        content:' 本视频将带领病患依次练习肢体移动、翻身、起坐、站立、上下轮椅、扶物行走、抓握物品等患侧肢体的功能锻炼。',
        isAcrticle:0,
        tag:'肢体训练',
        isCollected:1,
      },
      {
        title:'脑卒中治疗成功后如何进行语言训练与恢复',
        imgUrl:'https://s2.loli.net/2023/04/15/CXzg7H8sv3yNr45.jpg',
        content:' 必须尽早进行发音训练。先诱导发音，然后再说常用单字，如吃、喝、好、行等，或出示卡片，让病人读出上面的字。再依次教双音词、短语、短句、长句等。可结合说、视、听同时进行，如让病人穿衣服，则必须既说“穿衣服”让病人听，又要指着准备好的衣服，并作出穿衣服手势示意让病人看，让病人一边说穿衣服，一边练习自己穿衣服。',
        isAcrticle:1,
        tag:'语言训练',
        isCollected:1,
      },
      {
        title:'脑卒中后康复训练——下肢训练',
        imgUrl:'https://s2.loli.net/2023/04/15/4MQCwatriefmRG8.png',
        content:' 中风是一种缺乏血液流向大脑部分部位的医疗状况，这可能回导致手臂和腿的无力。照顾者可以使用这个视频在家庭环境中对中风患者进行简单的练习。',
        isAcrticle:0,
        tag:'下肢训练',
        isCollected:0,
      },
    ]
  },
  tabSelect(e) {
    this.setData({
      TabCur: e.currentTarget.dataset.id,
      scrollLeft: (e.currentTarget.dataset.id-1)*60
    })
  },
  goTo:function(){
    wx.navigateTo({
      url: '../question/index',
    })
  },
  goToDetail:function(){
    wx.navigateTo({
      url: '../article/index',
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