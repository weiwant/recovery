// pages/video/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    src: "",        // 上传视频
  },
  chooseVideo: function() {
    var _this = this;
    wx.chooseVideo({
      success: function(res) {
        _this.setData({
          src: res.tempFilePath,
        })
      }
    })
  },
  /**
   * 上传视频 目前后台限制最大100M, 以后如果视频太大可以选择视频的时候进行压缩
   */
  uploadvideo: function() {
    var src = this.data.src;
    console.log(src);
    // wx.uploadFile({
    //   url: '',
    //   methid: 'POST',           // 可用可不用
    //   filePath: src,
    //   name: 'files',              // 服务器定义key字段名称
    //   header: app.globalData.header,
    //   success: function() {
    //     console.log('视频上传成功')
    //   },
    //   fail: function() {
    //     console.log('接口调用失败')
    //   }
    // });
    wx.navigateTo({
      url: '../results/index',
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