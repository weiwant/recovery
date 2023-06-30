// pages/article/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    newsId:0,
    isArticle:1,
    url:'https://s2.loli.net/2023/04/15/OoIvMjgVNFQGqBW.png',
    // url:'http://47.113.202.168/demo.mp4',
    title:'脑卒中，一种在中国发病率极高的疾病。',
    content:'&emsp;&emsp;脑卒中（stroke），是指突然发生的、由脑血管病变引起的局限的或全脑的功能障碍，持续时间超过24h或引起死亡的临床综合征。我们需要知道的关于脑卒中的一些危险因素。a可调控因素：高血压、糖尿病、心脏病、高脂血症等b.可改变的因素：不良饮食习惯、大量饮酒、吸烟等c.不可变的因素：年龄、性别、家族史等\n&emsp;&emsp;脑卒中，一种在中国发病率极高的疾病。中国人每5人中就会有两人罹患脑卒中，脑卒中也是我国疾病所致寿命损失年的第一病因，每年约190余万人因卒中死亡。卒中的致残率也同样很高，高达70%-80%。那关于脑卒中我们应该知道哪些东西呢？\n&emsp;&emsp;我们需要知道的关于脑卒中的一些危险因素:\n&emsp;&emsp;a可调控因素：高血压、糖尿病、心脏病、高脂血症等\n&emsp;&emsp;b.可改变的因素：不良饮食习惯、大量饮酒、吸烟等\n&emsp;&emsp;c.不可变的因素：年龄、性别、家族史等'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.setData({
      newsId:options.id,
    });
    console.log(this.data.newsId);
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